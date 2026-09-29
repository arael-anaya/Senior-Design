"""
Friction budget for the scissor-boom deployable radiator.

Backs every number in friction_table.tex. Each resistive source is turned into
a generalized torque Q about the model coordinate theta (the same slot as
Q_F = N_s * tau_f in Derivation/main.tex), so the sources can be summed and
compared directly with the spring. The total is then converted back into the
params.py convention (tau_f per spring, F_friction = tau_f / r_o) so it drops
straight into the existing Phase 1 / Phase 2 scripts.

Which parameter set is used follows params.USE_TESTING_PARAMS, like every
other script in the parent folder:
  True  -> bench test article in 1 g (pin loads = weight)
  False -> production array on orbit (pin loads = spring-induced internal loads)

Joint kinematics (n bays, one X per bay, pinned at the root, root top node on
a guide): 3n revolute joints. The ground pin and the guide-carriage pin turn
d(theta) per d(theta); the n centre pivots and 2(n-1) inter-bay nodes join a
+theta rod to a -theta rod, so they turn 2 d(theta). Summing the virtual work,
a per-joint friction torque tau_j costs Q = (6n - 2) * tau_j.

Coefficients and their sources are listed next to each constant; [n] matches
the bibliography numbering in friction_table.tex.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Phase1          # noqa: E402
import friction_sweep  # noqa: E402
import params          # noqa: E402

IN2M = 0.0254
INLBF_TO_NM = 0.112984829
G = 9.80665
BENCH = params.USE_TESTING_PARAMS

n = params.n_links
L = params.link_length
N_s = params.N_springs
r_o = params.r_o
theta_0 = params.theta_0
theta_1 = Phase1.solve_theta1()

# Hinge pin radius: bench uses the measured 1/4 in holes; production has no
# pin size yet, so a 1/2 in pin is ASSUMED.
r_pin = params.link_hole_dia / 2.0 if BENCH else 0.5 * IN2M / 2.0

n_joints = 3 * n
joint_mult = 6 * n - 2          # sum of relative-rotation ratios over all joints

# Cases are (low, nominal, high).
CASES = ("low", "nom", "high")

# Pin-joint friction coefficient.
#   low/nom: bench = iglide J dry vs steel 0.06-0.18 [igus];
#            orbit = sputtered MoS2 in vacuum 0.01-0.04 [Spalvins]
#   high:    bare Al vs mild steel, static 0.61 [EngTB]
MU_PIN = (0.06, 0.18, 0.61) if BENCH else (0.01, 0.04, 0.61)

# Guide at the root top node.
#   low/nom: recirculating-ball guide 0.002-0.003 [THK]
#   high:    plain Al-on-steel slot, kinetic 0.47 [EngTB]
MU_GUIDE = (0.002, 0.003, 0.47)

# Torsion-spring coil/arbor friction as a fraction of spring torque.
#   nom: 10.8/10.2 - 1 = 5.9 % rate correction for coil-arbor friction [EngEdge]
#   low/high: 0.5x / 2x nominal (judgement; spaced coils lower it [LeeSpring])
SPRING_HY = (0.5 * (10.8 / 10.2 - 1), 10.8 / 10.2 - 1, 2 * (10.8 / 10.2 - 1))

# Harness / flex-line resistive torque per hinge-line crossing, N*m.
#   S-NPP solar array [Helfrich]: 0.5 in-lb predicted, 3.2 in-lb measured,
#   20 in-lb worst "zero-neutral" value.
T_HARNESS = tuple(v * INLBF_TO_NM for v in (0.5, 3.2, 20.0))
# Production: one gas-feed line at the root + one coolant jumper per bay
# (ASSUMED routing). Bench: gas-feed line only.
n_crossings = 1 if BENCH else n + 1

# Vacuum adhesion (breakaway) force per contact, N [STM-279]:
#   low: hard-anodised Al7075 vs SS15-5PH, no adhesion measured
#   nom: Alodine-coated Al7075 vs Al7075, 336 mN
#   high: bare Al7075 vs Al7075, 1744 mN
# Cold welding is a vacuum effect, so the bench (in air) carries none.
F_ADHESION = (0.0, 0.0, 0.0) if BENCH else (0.0, 0.336, 1.744)

# Deployed-position latch: ONE latch locks the 1-DOF mechanism.
# ASSUMED spring plunger 5 N, 30 deg ramp, 25 mm from a centre pivot.
# Ramp friction: steel-steel kinetic 0.42 (nom), static 0.8 (high) [EngTB].
F_PLUNGER, RAMP, R_LATCH = 5.0, np.radians(30.0), 0.025
MU_LATCH = (0.2, 0.42, 0.8)

# ECSS-E-ST-33-01C Rev.2 Table 4-2 theoretical uncertainty factors, and the
# overall factor of 2 in its Tmin equation [ECSS].
ECSS = {"FR": 3.0, "HY": 3.0, "HA": 3.0, "HD": 3.0}
ECSS_OVERALL = 2.0


def spring_k(tau_design):
    """Spring rate the existing pipeline would pick for a per-spring design torque."""
    return friction_sweep.required_k(params.t_deploy, tau_design)[0]


def pin_normal_load(k):
    """Radial load per pin joint, N."""
    if BENCH:
        return params.M_j * G            # conservative: every joint carries one bay in 1 g
    return 2.0 * k * theta_0 / L         # spring torque reacted over a half-link


def budget(k):
    """Generalized resistive torque Q (N*m about theta) per source, per case."""
    N_pin = pin_normal_load(k)
    rows = {}
    rows["Hinge pin joints"] = ("FR", [mu * N_pin * r_pin * joint_mult for mu in MU_PIN])
    rows["Root guide / carriage"] = ("FR", [mu * N_pin * L for mu in MU_GUIDE])
    rows["Torsion-spring coil/arbor"] = ("HY", [f * N_s * k * theta_0 for f in SPRING_HY])
    rows["Harness / flex lines"] = ("HA", [T * n_crossings for T in T_HARNESS])
    rows["Vacuum adhesion (breakaway)"] = ("HD", [F * r_pin * joint_mult for F in F_ADHESION])
    latch = []
    for mu in MU_LATCH:
        F_t = F_PLUNGER * (np.tan(RAMP) + mu) / (1 - mu * np.tan(RAMP))
        latch.append(2.0 * F_t * R_LATCH)   # centre pivot turns 2 d(theta)
    rows["Deployed latch (end of travel)"] = ("FR", latch)
    return rows, N_pin


# Sources that resist over the whole stroke; adhesion only acts at breakaway
# (theta_0) and the latch only at the end of travel (theta_min).
TRAVEL = ("Hinge pin joints", "Root guide / carriage", "Torsion-spring coil/arbor",
          "Harness / flex lines")
PHASES = {
    "start (theta_0)": TRAVEL + ("Vacuum adhesion (breakaway)",),
    "travel": TRAVEL,
    "end (theta_min)": TRAVEL + ("Deployed latch (end of travel)",),
}


def totals(rows, names):
    raw = np.sum([rows[k][1] for k in names], axis=0)
    fac = np.sum([ECSS[rows[k][0]] * np.array(rows[k][1]) for k in names], axis=0) * ECSS_OVERALL
    return raw, fac


def report(k, label):
    rows, N_pin = budget(k)
    print(f"--- {label}: k = {k:.5g} N*m/rad, stow spring torque (all springs) "
          f"N_s*k*theta_0 = {N_s * k * theta_0:.5g} N*m, pin load = {N_pin:.4g} N ---")
    print(f"{'source':<32}{'cls':>4}" + "".join(f"{c:>12}" for c in CASES))
    for name, (cls, v) in rows.items():
        print(f"{name:<32}{cls:>4}" + "".join(f"{x:>12.4g}" for x in v))
    for phase, names in PHASES.items():
        raw, fac = totals(rows, names)
        tau_eq = raw / N_s
        print(f"  [{phase}]")
        print(f"{'    raw Q, N*m':<36}" + "".join(f"{x:>12.4g}" for x in raw))
        print(f"{'    ECSS-factored Q, N*m':<36}" + "".join(f"{x:>12.4g}" for x in fac))
        print(f"{'    equiv. tau_f per spring, N*m':<36}" + "".join(f"{x:>12.4g}" for x in tau_eq))
        print(f"{'    equiv. F_friction (raw), N':<36}" + "".join(f"{x:>12.4g}" for x in tau_eq / r_o))
        print(f"{'    equiv. F_friction (ECSS), N':<36}" + "".join(f"{x:>12.4g}" for x in fac / N_s / r_o))
        # Same Q seen as an axial push at the boom tip: x_end = n L cos(theta)
        print(f"{'    tip force at theta_1 (raw), N':<36}"
              + "".join(f"{x:>12.4g}" for x in raw / (n * L * np.sin(theta_1))))
    print(f"  Spring torque available (all springs): at theta_0 {N_s * k * theta_0:.4g} N*m, "
          f"at theta_1 {N_s * k * theta_1:.4g} N*m")
    return rows


def main():
    print(f"Parameter set: {'BENCH (1 g)' if BENCH else 'PRODUCTION (orbit)'}")
    print(f"n={n}, L={L:.4f} m, M_j={params.M_j:.4g} kg, r_o={r_o:.5f} m, r_pin={r_pin:.5f} m, "
          f"joints={n_joints}, joint multiplier={joint_mult}, harness crossings={n_crossings}")
    print(f"theta_0={np.degrees(theta_0):.1f} deg, theta_1={np.degrees(theta_1):.2f} deg")
    print(f"Current params.py: F_friction={params.F_friction} N -> tau_f={params.tau_friction:.4g} N*m, "
          f"design tau_f={params.tau_friction_design:.4g} N*m, "
          f"Q_F=N_s*tau_f_design={N_s * params.tau_friction_design:.4g} N*m\n")

    k_now = spring_k(params.tau_friction_design)
    report(k_now, "At the spring rate the current 5 N assumption produces")

    # Self-consistent: size the spring the same way (x friction_safety_factor)
    # against the nominal budget, recompute the spring-dependent terms, repeat.
    k = k_now
    for _ in range(50):
        rows, _ = budget(k)
        raw, _ = totals(rows, PHASES["start (theta_0)"])
        k_new = spring_k(raw[1] / N_s * params.friction_safety_factor)
        if abs(k_new - k) < 1e-9 * max(k, 1e-12):
            break
        k = k_new
    print()
    report(k, "Self-consistent (spring re-sized to the nominal budget x1.5)")

    # Thermal clearance loss: Al 23e-6/K vs carbon steel 10.8e-6/K [EngTB-CTE]
    for dT in (50.0, 100.0, 150.0):
        dc = (23e-6 - 10.8e-6) * 2 * r_pin * dT
        print(f"Cold clearance loss, dT = -{dT:.0f} K: {dc * 1e6:.1f} um on a {2 * r_pin * 1e3:.2f} mm pin")


if __name__ == "__main__":
    main()
