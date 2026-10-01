"""
Numerical check supporting the quasi-static assumption used in
derivation/main.tex (Section "Quasi-Static Assumption").

Claim being checked: over the deployment timescales in params.py
(t_deploy ~ 1 hr for Phase 1, t2_deploy ~ 11 hr for Phase 2), the inertial
torques in the full equation of motion --

    I_eff(theta) * ddtheta                         (angular-acceleration term)
    M_j * i(i-1) * L^2 * sin(theta)cos(theta) * dtheta^2   (centrifugal-type term)

-- are negligible next to the resisting/driving torques already in the model:

    N_springs * k * theta          (hinge-spring torque)
    N_springs * tau_friction_design (dry-friction resisting torque)
    2 * N_kinks * M_k0              (Phase 2 kink/pressure torque)

Method: order-of-magnitude scaling. Take the angular rate/acceleration scale
implied by sweeping the phase's angular range over its allotted time,
    Omega ~ delta_theta / t_phase,   Alpha ~ delta_theta / t_phase^2,
and evaluate the inertial terms at that scale using the actual I_eff(theta)
and mechanism parameters. This is deliberately crude (no shape assumptions
on theta(t)) -- it only needs to bound the inertial terms from above.
"""

import numpy as np

import Phase1
import Phase2
from params import (
    n_links, link_length, M_j, N_springs, N_kinks,
    tau_friction_design, theta_0, theta_min,
    t_deploy, t2_deploy,
)

I_eff = Phase1.I_eff


def inertial_torque_scale(theta_lo, theta_hi, t_phase):
    """Upper-bound estimate of both inertial terms over [theta_lo, theta_hi]."""
    delta_theta = theta_hi - theta_lo
    Alpha = delta_theta / t_phase**2
    Omega = delta_theta / t_phase

    thetas = np.linspace(theta_lo, theta_hi, 200)
    I_max = np.max(I_eff(thetas))

    tau_ddtheta = I_max * Alpha

    # centrifugal-type term: M_j * i(i-1) * L^2 * sin*cos * dtheta^2,
    # sin*cos <= 1/2, so bound it at that.
    S1 = n_links * (n_links + 1) * (n_links - 1) / 3.0  # sum i(i-1), matches params.S1_link_index
    tau_centrifugal = M_j * S1 * link_length**2 * 0.5 * Omega**2

    return tau_ddtheta, tau_centrifugal


def main():
    theta_1 = Phase1.solve_theta1()
    k = Phase1.required_k(theta_1, t_deploy)
    M_k0 = Phase2.required_Mk0(t2_deploy, theta_1, k)

    print("=== Phase 1 (theta_0 -> theta_1) ===")
    tau_ddth, tau_cent = inertial_torque_scale(theta_1, theta_0, t_deploy)
    tau_spring = N_springs * k * theta_1  # worst case: smallest spring torque in sweep
    tau_fric = N_springs * tau_friction_design
    print(f"  I*ddtheta scale:      {tau_ddth:.3e} N*m")
    print(f"  centrifugal scale:    {tau_cent:.3e} N*m")
    print(f"  spring torque (min):  {tau_spring:.3e} N*m")
    print(f"  friction torque:      {tau_fric:.3e} N*m")
    print(f"  ratio I*ddtheta / friction:   {tau_ddth / tau_fric:.3e}")
    print(f"  ratio centrifugal / friction: {tau_cent / tau_fric:.3e}")
    print(f"  ratio I*ddtheta / spring:     {tau_ddth / tau_spring:.3e}")

    print("\n=== Phase 2 (theta_1 -> theta_min) ===")
    tau_ddth2, tau_cent2 = inertial_torque_scale(theta_min, theta_1, t2_deploy)
    tau_spring2 = N_springs * k * theta_min
    tau_kink = 2 * N_kinks * M_k0
    print(f"  I*ddtheta scale:      {tau_ddth2:.3e} N*m")
    print(f"  centrifugal scale:    {tau_cent2:.3e} N*m")
    print(f"  spring torque (min):  {tau_spring2:.3e} N*m")
    print(f"  friction torque:      {tau_fric:.3e} N*m")
    print(f"  kink torque:          {tau_kink:.3e} N*m")
    print(f"  ratio I*ddtheta / friction: {tau_ddth2 / tau_fric:.3e}")
    print(f"  ratio I*ddtheta / kink:     {tau_ddth2 / tau_kink:.3e}")


if __name__ == "__main__":
    main()
