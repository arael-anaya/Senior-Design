"""
Sweep F_friction (per-joint hinge friction force, N) across a wide range of
extremes to characterize how the required torsion-spring rate/torque scales
with the still-untested friction assumption in params.py.

Reimplements Phase1.required_k / t1_of_k and Phase2.t2_of_Mk0 / required_Mk0
with tau_friction_design passed explicitly (instead of read from the params
module at import time), so each sweep point can use its own friction value
without monkeypatching module state.

Output: a table (printed + CSV) of, for each F_friction:
  - tau_friction, tau_friction_design
  - k_min (nominal, bare friction) and k_min_design (vs inflated friction)
  - required spring rate k (N*m/rad and in-lbf/deg)
  - per-spring max torque at full deflection (in-lbf)
  - actual Phase 1 duration at that k
  - Phase 2: required kink moment M_k0 and implied Delta_P for the chosen R_tube
"""

import csv
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

import Phase1
from params import (
    r_o, theta_0, friction_safety_factor, spring_margin_over_kmin,
    t_deploy, t2_deploy, N_springs, N_kinks, theta_min, R_tube, a_kink,
    N_M_TO_IN_LBF,
)

I_eff = Phase1.I_eff
theta_1 = Phase1.solve_theta1()


def energy_bracket(theta, k, tau):
    return N_springs * (k * (theta_0**2 - theta**2) - 2 * tau * (theta_0 - theta))


def t1_of_k(k, tau):
    def integrand(theta):
        return np.sqrt(I_eff(theta) / energy_bracket(theta, k, tau))
    integral, _ = quad(integrand, theta_1, theta_0, args=())
    return integral


def required_k(t, tau):
    def residual(k):
        return t1_of_k(k, tau) - t

    k_min = 2 * tau / (theta_0 + theta_1)
    lo = k_min * 1.001
    if residual(lo) <= 0:
        return k_min * spring_margin_over_kmin, k_min

    hi = max(lo * 2, 1.0)
    while residual(hi) > 0:
        hi *= 2
    return brentq(residual, lo, hi), k_min


def t2_of_Mk0(M_k0, k, tau):
    theta_dot_1_sq = N_springs * (k * (theta_0**2 - theta_1**2) - 2 * tau * (theta_0 - theta_1)) / I_eff(theta_1)

    def energy_bracket2(theta):
        return (I_eff(theta_1) * theta_dot_1_sq
                + N_springs * k * (theta_1**2 - theta**2)
                - N_springs * 2 * tau * (theta_1 - theta)
                - 4 * N_kinks * M_k0 * (theta - theta_1))

    if energy_bracket2(theta_min) <= 0:
        return np.inf

    def integrand(theta):
        return np.sqrt(I_eff(theta) / energy_bracket2(theta))

    integral, _ = quad(integrand, theta_min, theta_1)
    return integral


def required_Mk0(t2, k, tau, Mk0_max_guess=1.0):
    def residual(M_k0):
        return t2_of_Mk0(M_k0, k, tau) - t2

    if residual(0.0) <= 0:
        return None  # springs alone already clear Phase 2 faster than t2

    upper = Mk0_max_guess
    while residual(upper) > 0:
        upper *= 2
    return brentq(residual, 0.0, upper)


def main():
    # Extremes: from well below the old flat 0.5 N guess (pre-10x-inflation)
    # up to well above the current 5.0 N design value.
    F_frictions = [0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]

    rows = []
    for F in F_frictions:
        tau = F * r_o                              # nominal per-joint torque, N*m
        tau_design = tau * friction_safety_factor  # inflated design torque, N*m

        k, k_min_design = required_k(t_deploy, tau_design)
        k_min_nominal = 2 * tau / (theta_0 + theta_1)

        t1_actual = t1_of_k(k, tau_design)
        deflection_rad = theta_0 - theta_1
        max_torque_Nm = k * deflection_rad
        max_torque_inlbf = max_torque_Nm * N_M_TO_IN_LBF
        k_in_lbf_per_deg = k * N_M_TO_IN_LBF / 57.29577951

        M_k0 = required_Mk0(t2_deploy, k, tau_design)
        if M_k0 is None:
            Delta_P = None
        else:
            Delta_P = M_k0 / (a_kink * R_tube**3)

        rows.append({
            "F_friction_N": F,
            "tau_friction_Nm": tau,
            "tau_friction_design_Nm": tau_design,
            "k_min_nominal_Nm_per_rad": k_min_nominal,
            "k_min_design_Nm_per_rad": k_min_design,
            "k_required_Nm_per_rad": k,
            "k_required_inlbf_per_deg": k_in_lbf_per_deg,
            "max_torque_per_spring_inlbf": max_torque_inlbf,
            "deflection_deg": np.degrees(deflection_rad),
            "t1_actual_s": t1_actual,
            "t1_budget_s": t_deploy,
            "margin_over_nominal_friction_pct": (k / k_min_nominal - 1.0) * 100.0,
            "M_k0_required_Nm": M_k0,
            "Delta_P_required_Pa": Delta_P,
            "N_springs": N_springs,
        })

    header = list(rows[0].keys())
    print(",".join(header))
    for r in rows:
        print(",".join(f"{r[h]:.6g}" if isinstance(r[h], (int, float)) else str(r[h]) for h in header))

    out_path = "friction_sweep.csv"
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
