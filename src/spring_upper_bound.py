"""
Upper bound on the hinge spring rate k, so the stowed-envelope latch can be
sized once and stay safe whatever spring we end up buying.

Why an upper bound needs assumptions: the model only gives a LOWER bound on k
(friction floor, k_min, and the t_deploy budget; finishing early is fine, so
stiffer springs never violate the time budget). Nothing in the physics caps k
from above, so the cap is a purchasing spec built from:

  1. A credible worst-case hinge friction F_HI (the friction is untested and
     sets k). k_design(F_HI) is the largest k we would ever *need*.
  2. Spring-rate tolerance / catalog rounding: we can only buy what exists,
     so allow the bought spring to be up to SPRING_RATE_MARGIN above the ideal.

  k_max = SPRING_RATE_MARGIN * k_design(F_HI)

Latch load is linear in k (Q = N*k*theta_0, F = Q / (c*L)), so the same
relation is also inverted: given a latch capacity, the largest k that may be
purchased.

ASSUMPTIONS TO CONFIRM (placeholders, not from the project files):
  F_HI = 20 N (4x the 5 N design value), SPRING_RATE_MARGIN = 1.25.
Also assumes zero spring preload at theta = 0 (torque = k*theta, as in the
derivation). A spring preloaded past theta = 0 carries extra stowed torque
k*theta_pre that this bound does not include.
"""

import numpy as np

import Phase1
import friction_sweep
import params
from params import (
    n_links, N_springs, link_length, r_o, theta_0, t_deploy,
    friction_safety_factor, N_M_TO_IN_LBF,
)

F_HI = 20.0                 # N, worst-case credible hinge friction (assumption)
SPRING_RATE_MARGIN = 1.25   # bought spring may exceed the ideal k by this factor (assumption)
N_TO_LBF = 0.224809


def latch_force(k, c):
    """Stowed outward force at a point with velocity coefficient c (units of L)."""
    return N_springs * k * theta_0 / (c * link_length)


def k_for_latch_capacity(F_cap, c):
    """Largest k (N*m/rad) whose stowed load at coefficient c stays within F_cap (N)."""
    return F_cap * c * link_length / (N_springs * theta_0)


def main():
    set_name = "TESTING (bench)" if params.USE_TESTING_PARAMS else "PRODUCTION"
    print(f"Parameter set: {set_name}   n={n_links}, L={link_length:.4f} m")
    print(f"Assumptions: F_HI={F_HI} N, SPRING_RATE_MARGIN={SPRING_RATE_MARGIN}\n")

    k_nom = Phase1.required_k(Phase1.solve_theta1(), t_deploy)
    k_design, _ = friction_sweep.required_k(t_deploy, F_HI * r_o * friction_safety_factor)
    k_max = SPRING_RATE_MARGIN * k_design

    print(f"Nominal k (F=5 N):        {k_nom:.5f} N*m/rad")
    print(f"k_design at F_HI:         {k_design:.5f} N*m/rad")
    print(f"UPPER BOUND k_max:        {k_max:.5f} N*m/rad "
          f"= {k_max * N_M_TO_IN_LBF / 57.29577951:.5f} in-lbf/deg")
    print(f"Max torque per spring at stow (k_max*theta_0): {k_max * theta_0:.5f} N*m "
          f"= {k_max * theta_0 * N_M_TO_IN_LBF:.4f} in-lbf")
    print(f"k_max / nominal k: {k_max / k_nom:.2f}\n")

    print("=== Latch design load at k_max (stowed) ===")
    print(f"{'location':>28} {'c':>6} {'F[N]':>10} {'F[lbf]':>10}")
    for name, c in [("link 1 CoM (upper bound)", 0.5), ("joint 1 (1 bay from pin)", 1.0),
                    ("far end node (n)", float(n_links))]:
        F = latch_force(k_max, c)
        print(f"{name:>28} {c:>6.1f} {F:>10.4f} {F * N_TO_LBF:>10.4f}")

    print("\n=== Inverse: latch capacity -> max purchasable k (far end node) ===")
    print(f"{'F_cap[N]':>9} {'k_max[N*m/rad]':>15} {'k_max[in-lbf/deg]':>18}")
    for F_cap in [0.5, 1, 2, 5, 10, 20]:
        kc = k_for_latch_capacity(F_cap, n_links)
        print(f"{F_cap:>9} {kc:>15.5f} {kc * N_M_TO_IN_LBF / 57.29577951:>18.5f}")


if __name__ == "__main__":
    main()
