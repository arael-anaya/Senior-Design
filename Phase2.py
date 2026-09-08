"""
Phase 2 model: hinge-spring + inflatable-kink deployment.

Covers the swing from theta_1 (Phase 1 handoff angle) down to theta_min
(fully deployed), with a constant kink moment M_k0 added by the
pressurized tube ((C1) closure, M_k0 = a_kink * Delta_P * R_tube^3).

Given a desired Phase 2 duration t2, root-finds the constant kink moment
M_k0 needed, then converts M_k0 into the required pressure Delta_P for a
chosen tube radius R_tube.

theta_1 and k come from Phase1.solve_theta1()/required_k(), so the functions
below take them as arguments rather than assuming one fixed value. Running
this file directly does a single pass using Phase 1's defaults, as a sanity
check -- solve_design.py chains Phase 1 into Phase 2 end to end.

Derivation: Derivation/main.tex, Section "PHASE 2".
Reuses I_eff(theta), N_springs, N_kinks, and a_kink from Phase1.py.
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

import Phase1
from params import (
    theta_min_deg, theta_min, total_deploy_time, t2_deploy, R_tube,
    N_springs, N_kinks, theta_0, a_kink, F_friction, tau_friction_design,
)

I_eff = Phase1.I_eff


def t2_of_Mk0(M_k0, theta_1, k):
    """Phase 2 duration produced by a given constant kink moment M_k0, at handoff (theta_1, k)."""
    theta_dot_1_sq = N_springs * (k * (theta_0**2 - theta_1**2) - 2 * tau_friction_design * (theta_0 - theta_1)) / I_eff(theta_1)

    def energy_bracket(theta):
        """RHS bracket under the sqrt in the Phase 2 integrand."""
        return (I_eff(theta_1) * theta_dot_1_sq
                + N_springs * k * (theta_1**2 - theta**2)
                - N_springs * 2 * tau_friction_design * (theta_1 - theta)
                - 4 * N_kinks * M_k0 * (theta - theta_1))

    if energy_bracket(theta_min) <= 0:
        return np.inf

    def integrand(theta):
        return np.sqrt(I_eff(theta) / energy_bracket(theta))

    integral, _ = quad(integrand, theta_min, theta_1)
    return integral


def required_Mk0(t2, theta_1, k, Mk0_max_guess=1.0):
    """Root-find the constant kink moment M_k0 that produces duration t2, at handoff (theta_1, k)."""
    def residual(M_k0):
        return t2_of_Mk0(M_k0, theta_1, k) - t2

    if residual(0.0) <= 0:
        raise ValueError(
            "Springs alone already clear Phase 2 faster than the requested t2_deploy "
            f"({t2_of_Mk0(0.0, theta_1, k):.4f} s <= {t2} s). A kink moment only speeds "
            "deployment up further, so t2_deploy must be shorter than the spring-only baseline."
        )

    upper = Mk0_max_guess
    while residual(upper) > 0:
        upper *= 2
    return brentq(residual, 0.0, upper)


if __name__ == "__main__":
    theta_1 = Phase1.solve_theta1()
    k = Phase1.required_k(theta_1, Phase1.t_deploy)

    M_k0 = required_Mk0(t2_deploy, theta_1, k)
    Delta_P_required = M_k0 / (a_kink * R_tube**3)

    print(f"Phase 1/2 handoff angle theta_1: {np.degrees(theta_1):.2f} deg")
    print(f"Spring constant k (from Phase 1): {k:.4f} N*m/rad")
    print(f"Required kink moment M_k0: {M_k0:.6f} N*m")
    print(f"Tube radius R_tube (chosen): {R_tube:.4f} m")
    print(f"Required pressure Delta_P: {Delta_P_required:.2f} Pa")
