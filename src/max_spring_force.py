"""
Rough maximum spring load estimate for the hinge torsion springs.

Uses the existing model (params.py, Phase1.py, friction_sweep.py). The
spring torque model in the derivation is tau_spring = k * theta (zero preload
at theta = 0; see the energy bracket k*(theta_0^2 - theta^2) in Phase1.py), so
the peak load occurs at stow (theta = theta_0) and falls as the mechanism opens.

Reported, per spring and for the whole system:
  - peak torque k*theta_0 (the model's true maximum)
  - torque at the Phase 1 handoff (theta_1) and the McMaster-style
    k*(theta_0 - theta_1) figure that Phase1.py prints, for comparison
  - equivalent forces: torque / link_length (tip force) and torque / r_o
    (load at the hinge-pin radius, the friction moment arm)
  - the same numbers across the friction sweep, since friction is the
    dominant untested assumption and sets k
  - a 2x "rough max" bound to cover unmodeled effects

Which parameter set is active depends on params.USE_TESTING_PARAMS.
"""

import numpy as np

import Phase1
import friction_sweep
import params
from params import (
    theta_0, link_length, r_o, N_springs, N_M_TO_IN_LBF, t_deploy,
    friction_safety_factor, F_friction,
)

UNMODELED_FACTOR = 2.0   # rough allowance for unmodeled effects (dynamic, misalignment, etc.)
N_TO_LBF = 0.224809


def loads(k, theta_1):
    """Peak spring loads for spring rate k (N*m/rad)."""
    tau_stow = k * theta_0
    return {
        "k": k,
        "tau_stow_Nm": tau_stow,
        "tau_stow_inlbf": tau_stow * N_M_TO_IN_LBF,
        "tau_handoff_Nm": k * theta_1,
        "tau_mcmaster_Nm": k * (theta_0 - theta_1),
        "F_tip_N": tau_stow / link_length,
        "F_pin_N": tau_stow / r_o,
        "tau_total_Nm": N_springs * tau_stow,
    }


def main():
    theta_1 = Phase1.solve_theta1()
    set_name = "TESTING (bench)" if params.USE_TESTING_PARAMS else "PRODUCTION"
    print(f"Parameter set: {set_name}")
    print(f"n_links={params.n_links}, link_length={link_length:.4f} m, r_o={r_o:.5f} m, "
          f"F_friction={F_friction} N (x{friction_safety_factor} safety)")
    print(f"theta_0={np.degrees(theta_0):.1f} deg, theta_1={np.degrees(theta_1):.2f} deg\n")

    # ---- Nominal design point ----
    k = Phase1.required_k(theta_1, t_deploy)
    L = loads(k, theta_1)
    print("=== Nominal design point ===")
    print(f"Spring rate k:                     {k:.5f} N*m/rad")
    print(f"Peak torque per spring (at stow):  {L['tau_stow_Nm']:.5f} N*m = {L['tau_stow_inlbf']:.4f} in-lbf")
    print(f"  torque at handoff theta_1:       {L['tau_handoff_Nm']:.5f} N*m")
    print(f"  k*(theta_0-theta_1) (Phase1.py): {L['tau_mcmaster_Nm']:.5f} N*m "
          f"(understates peak by {(1 - L['tau_mcmaster_Nm'] / L['tau_stow_Nm']) * 100:.0f}%)")
    print(f"Equivalent force at link tip:      {L['F_tip_N']:.4f} N = {L['F_tip_N'] * N_TO_LBF:.4f} lbf")
    print(f"Equivalent force at pin radius:    {L['F_pin_N']:.3f} N = {L['F_pin_N'] * N_TO_LBF:.3f} lbf")
    print(f"Total torque, all {N_springs} springs at stow: {L['tau_total_Nm']:.5f} N*m")
    print(f"Rough max (x{UNMODELED_FACTOR:g}): {UNMODELED_FACTOR * L['tau_stow_Nm']:.5f} N*m per spring, "
          f"tip force {UNMODELED_FACTOR * L['F_tip_N']:.4f} N, pin-radius force {UNMODELED_FACTOR * L['F_pin_N']:.3f} N\n")

    # ---- Friction sweep ----
    print("=== Friction sweep (peak spring load vs. assumed hinge friction) ===")
    print(f"{'F_fric[N]':>10} {'k[Nm/rad]':>11} {'tau_stow[Nm]':>13} {'tau_stow[in-lbf]':>17} "
          f"{'F_tip[N]':>10} {'F_pin[N]':>10}")
    for F in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]:
        tau_design = F * r_o * friction_safety_factor
        k_f, _ = friction_sweep.required_k(t_deploy, tau_design)
        Lf = loads(k_f, theta_1)
        print(f"{F:>10.1f} {k_f:>11.5f} {Lf['tau_stow_Nm']:>13.5f} {Lf['tau_stow_inlbf']:>17.4f} "
              f"{Lf['F_tip_N']:>10.4f} {Lf['F_pin_N']:>10.3f}")


if __name__ == "__main__":
    main()
