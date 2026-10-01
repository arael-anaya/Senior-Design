"""
Outward (x-direction) force the deploying array pushes with, vs. deployment
angle -- the load a stowed-envelope locking mechanism must hold.

Kinematics (derivation/main.tex, eq. ri): each of the n links advances the
array end by L*cos(theta), so the end position is
    x_end(theta) = n * L * cos(theta),   dx/dtheta = -n * L * sin(theta).

Virtual work (V = 1/2 * N * k * theta^2, generalized spring torque N*k*theta):
    F_x(theta) * n * L * sin(theta) = N * k * theta
    F_x(theta) = N * k * theta / (n * L * sin(theta))
With N = n this is k*theta / (L*sin(theta)). theta/sin(theta) is increasing in
theta, so the peak outward force is at stow (theta_0 = 90 deg): k*theta_0 / L.
That is the number to design the lock for; a locked stowed array sees no
friction relief, so friction is NOT subtracted (friction only helps the lock).

Optional Phase 2 kink term (pressurized tube, generalized torque 2*N_k*M_k0,
matching quasi_static_check.py) is reported separately -- it is ~0 at stow
(sin 2theta closure) so it does not drive the stowed lock load.

Reports nominal, and the friction-sweep upper bound, since k is set by the
still-untested hinge friction (params.F_friction).
"""

import numpy as np

import Phase1
import friction_sweep
import params
from params import (
    n_links, N_springs, link_length, r_o, theta_0, t_deploy,
    friction_safety_factor, F_friction,
)

UNMODELED_FACTOR = 2.0   # placeholder allowance for unmodeled effects
N_TO_LBF = 0.224809


def F_out(theta, k, c=None):
    """Outward x-force (N) from the hinge springs at angle theta (rad).

    c is the x-velocity coefficient of the point the lock acts on, in units of
    L*sin(theta): n for the far end node (default), k for the k-th joint,
    (i - 1/2) for the CoM of link i. Smaller c -> larger force."""
    if c is None:
        c = n_links
    return N_springs * k * theta / (c * link_length * np.sin(theta))


def main():
    theta_1 = Phase1.solve_theta1()
    k = Phase1.required_k(theta_1, t_deploy)
    set_name = "TESTING (bench)" if params.USE_TESTING_PARAMS else "PRODUCTION"
    print(f"Parameter set: {set_name}   n={n_links}, L={link_length:.4f} m, "
          f"k={k:.5f} N*m/rad (F_friction={F_friction} N)")
    print(f"Stowed length envelope: end x = n*L*cos(theta) = 0 at 90 deg; "
          f"fully open at 10 deg = {n_links * link_length * np.cos(params.theta_min):.3f} m\n")

    print("=== Outward force vs angle (nominal k) ===")
    print(f"{'theta[deg]':>10} {'x_end[m]':>10} {'F_out[N]':>10} {'F_out[lbf]':>11}")
    for deg in [90, 85, 80, 75, 60, 45, 30, 20, 10]:
        th = np.radians(deg)
        F = F_out(th, k)
        print(f"{deg:>10} {n_links * link_length * np.cos(th):>10.3f} {F:>10.4f} {F * N_TO_LBF:>11.4f}")

    F_stow = F_out(theta_0, k)
    print(f"\nPEAK (stowed, 90 deg): {F_stow:.4f} N = {F_stow * N_TO_LBF:.4f} lbf")
    print(f"Lock design load (x{UNMODELED_FACTOR:g}): {UNMODELED_FACTOR * F_stow:.4f} N "
          f"= {UNMODELED_FACTOR * F_stow * N_TO_LBF:.4f} lbf\n")

    print("=== Stowed lock load vs lock location (nominal k) ===")
    print(f"{'location':>28} {'c':>6} {'F_out[N]':>10} {'F_out[lbf]':>11}")
    locations = [("link 1 CoM (upper bound)", 0.5), ("joint 1 (1 bay from pin)", 1.0)]
    if n_links >= 3:
        locations.append((f"mid joint ({n_links // 2})", float(n_links // 2)))
    locations += [(f"last link CoM (n-1/2)", n_links - 0.5), ("far end node (n)", float(n_links))]
    for name, c in locations:
        Fc = F_out(theta_0, k, c)
        print(f"{name:>28} {c:>6.1f} {Fc:>10.4f} {Fc * N_TO_LBF:>11.4f}")
    print()

    print("=== Stowed lock load vs assumed hinge friction (sets k) ===")
    print(f"{'F_fric[N]':>10} {'k[Nm/rad]':>11} {'F_out_stow[N]':>14} {'F_out_stow[lbf]':>16}")
    for F in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]:
        tau_design = F * r_o * friction_safety_factor
        k_f, _ = friction_sweep.required_k(t_deploy, tau_design)
        Ff = F_out(theta_0, k_f)
        print(f"{F:>10.1f} {k_f:>11.5f} {Ff:>14.4f} {Ff * N_TO_LBF:>16.4f}")


if __name__ == "__main__":
    main()
