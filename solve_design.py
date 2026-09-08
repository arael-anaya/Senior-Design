"""
Full design chain: Phase 1 -> Phase 2, run in one pass.

theta_1 (Phase 1) is now a chosen geometric handoff margin, independent of
Delta_P and R_tube (see Phase1.solve_theta1), so there's no cycle left to
solve for: theta_1 and k come out of Phase 1 alone, then feed forward into
Phase 2, which solves for the kink moment -- and the pressure it implies
for a chosen R_tube -- needed to hit the Phase 2 duration target.

Derivation: Derivation/main.tex.
"""

import numpy as np

import Phase1
import Phase2

R_tube = Phase2.R_tube   # design choice, m


def solve():
    theta_1 = Phase1.solve_theta1()
    k = Phase1.required_k(theta_1, Phase1.t_deploy)
    M_k0 = Phase2.required_Mk0(Phase2.t2_deploy, theta_1, k)
    Delta_P = M_k0 / (Phase2.a_kink * R_tube**3)

    return {"theta_1": theta_1, "k": k, "M_k0": M_k0, "Delta_P": Delta_P, "R_tube": R_tube}


if __name__ == "__main__":
    result = solve()
    print(f"Phase 1/2 handoff angle theta_1: {np.degrees(result['theta_1']):.2f} deg")
    print(f"Spring constant k: {result['k']:.4f} N*m/rad")
    print(f"Required kink moment M_k0: {result['M_k0']:.6f} N*m")
    print(f"Tube radius R_tube (chosen): {result['R_tube']:.4f} m")
    print(f"Required pressure Delta_P: {result['Delta_P']:.2f} Pa")
