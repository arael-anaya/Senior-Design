"""
Phase 1 model: hinge-spring-only deployment.

Covers the swing from stowed (theta = pi/2) down to theta_1, the angle at
which the inflatable tube's kink stops being singular and can start
contributing real actuation torque (Q_p = Q_F = 0 in this phase).

theta_1 is a chosen design margin, not a derived quantity: the (C2) closure
Mk = a_kink * Delta_P * R_tube^3 * sin(2*theta) is zero at stow (the
singularity, sin(pi) = 0) and rises to its peak at theta = pi/4. theta_1 is
the angle at which sin(2*theta) has recovered to `handoff_margin` of that
peak. Delta_P, R_tube, and a_kink are just an overall scale on the closure,
so they cancel out of this ratio -- theta_1 depends only on handoff_margin.
(An earlier version tried to derive theta_1 from an instantaneous
torque-balance against the spring, but that comparison is degenerate: both
torques vanish at theta=0 and theta=pi/2, so one just dominates the other
everywhere in between rather than crossing at an interior point.)

I_eff(theta) sums the per-link inertia/velocity-coefficient terms over all
n_links (eq. Texp in the derivation) rather than using a single link's index --
using only one link understated the mechanism's total effective inertia by
~2.7x for the current n_links=7.

The spring is sized against tau_friction_design (tau_friction inflated by
params.friction_safety_factor), not the bare nominal friction estimate.
Sizing against the nominal value alone left only ~1% margin over the minimum
k that can overcome friction at all -- any unmodeled friction source would
have stalled deployment before reaching theta_1.

Derivation: Derivation/main.tex, Section "PHASE 1" and "Closure forms".
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

from params import (
    n_links, S1_link_index, panels_per_link, rho_al,
    panel_overhang, panel_thickness, panel_length, panel_width, m_radiator,
    link_length, tube_OD, tube_wall, r_o, r_i, m_link,
    I_panel, I_link, I_j,
    N_springs, N_kinks, F_friction, tau_friction, tau_friction_design,
    handoff_margin, total_deploy_time, t_deploy,
    M_j, theta_0, N_M_TO_IN_LBF, spring_margin_over_kmin,
)


def I_eff(theta):
    """Effective inertia I_eff(theta), summed over all n_links (eq. Texp in the
    derivation), not just a single link's contribution."""
    return (M_j * S1_link_index * link_length**2 * np.sin(theta)**2
            + n_links * I_j + 0.5 * n_links * M_j * link_length**2)


def _energy_bracket(theta, k, tau=tau_friction_design):
    return N_springs * (k * (theta_0**2 - theta**2) - 2 * tau * (theta_0 - theta))


def _integrand(theta, k):
    return np.sqrt(I_eff(theta) / _energy_bracket(theta, k))


def t1_of_k(k, theta1):
    """Phase 1 duration produced by a given spring constant k."""
    integral, _ = quad(_integrand, theta1, theta_0, args=(k,))
    return integral


def required_k(theta1, t):
    """Spring constant needed to swing theta_0 -> theta1 in time t, against friction.

    If the bare friction floor (k_min) already clears the target time on its
    own, time-matching has no solution (any k >= k_min only deploys faster) --
    finishing early is acceptable, so fall back to sizing k as
    spring_margin_over_kmin times k_min instead, and let Phase 1 finish faster
    than t.
    """
    def residual(k):
        return t1_of_k(k, theta1) - t

    k_min = 2 * tau_friction_design / (theta_0 + theta1)
    lo = k_min * 1.001
    if residual(lo) <= 0:
        return k_min * spring_margin_over_kmin

    hi = max(lo * 2, 1.0)
    while residual(hi) > 0:
        hi *= 2
    return brentq(residual, lo, hi)



def solve_theta1(handoff_margin=handoff_margin):
    """theta_1 where the (C2) closure's sin(2*theta) shape has recovered to `handoff_margin`
    of its peak, coming down from stow (theta_0 = pi/2) toward the peak at pi/4."""
    if not 0 < handoff_margin <= 1:
        raise ValueError("handoff_margin must be in (0, 1].")
    return (np.pi - np.arcsin(handoff_margin)) / 2.0


if __name__ == "__main__":
    theta_1 = solve_theta1()
    k = required_k(theta_1, t_deploy)

    deflection_angle_deg = np.degrees(theta_0 - theta_1)
    k_in_lbf_per_deg = k * N_M_TO_IN_LBF / 57.29577951
    max_torque_in_lbf = k * (theta_0 - theta_1) * N_M_TO_IN_LBF

    k_min_nominal = 2 * tau_friction / (theta_0 + theta_1)
    margin_over_nominal_friction_pct = (k / k_min_nominal - 1.0) * 100.0

    t1_actual = t1_of_k(k, theta_1)

    print(f"Minimum theta to leave singularity (theta_1): {np.degrees(theta_1):.2f} deg  ({theta_1:.4f} rad)")
    print(f"Required hinge spring constant k: {k:.4f} N*m/rad")
    print(f"Margin over nominal-friction floor: {margin_over_nominal_friction_pct:.1f}%")
    print(f"Actual Phase 1 duration at this k: {t1_actual:.1f} s (budget: {t_deploy:.1f} s)")
    print()
    print("--- McMaster torsion spring shopping parameters ---")
    print(f"Deflection Angle: {deflection_angle_deg:.1f} deg")
    print(f"Max Torque @ Max Torque: {max_torque_in_lbf:.3f} in-lbf")
    print(f"(equivalent spring rate: {k_in_lbf_per_deg:.4f} in-lbf/deg)")
