"""
Shared design parameters for Phase 1 / Phase 2 deployment models.
"""

import numpy as np

n_links = 7                     # n, number of scissor links/bays
panels_per_link = 1              # number of radiator panels carried per link

# I_eff(theta) sums the per-link (1/2 - i)^2 velocity-coefficient term over every
# link (Derivation/main.tex eq. Texp), which reduces to sum_{i=1}^{n} i(i-1) once
# the 1/4 constant is folded in. The old code used a single placeholder link index
# instead of this sum, understating the mechanism's total effective inertia.
S1_link_index = n_links * (n_links + 1) * (n_links - 1) / 3.0   # sum_{i=1}^{n} i(i-1)

# Material Density
rho_al = 2810.0                  # kg/m^3, Al 7075-T6

# Radiator Panel
panel_overhang = 0.254            # m, 10 in link overhang beyond the panel
panel_thickness = 0.043180        # m, 1.7 in nominal panel assembly thickness (PDR Sec. 2b)
panel_length = 3.2512         # m, 128 in max manufacturable panel length (PDR Sec. 2b)
panel_width = 1.2192  # m, 48 in max manufacturable panel length (PDR Sec. 2b)

m_radiator = rho_al * panel_length * panel_width * panel_thickness   # kg

# LINK
link_length = panel_length + panel_overhang        # m, link length
tube_OD = 0.1016                  # m, 4 in outer diameter
tube_wall = 0.00635                # m, 0.25 in wall thickness
r_o = tube_OD / 2.0
r_i = r_o - tube_wall
m_link = rho_al * np.pi * (r_o**2 - r_i**2) * link_length    # kg, hollow-tube link mass

# Inertias
I_panel = (m_radiator / 12.0) * (panel_length**2 + panel_thickness**2)
I_link = (m_link / 12.0) * (3.0 * (r_o**2 + r_i**2) + link_length**2)
I_j = I_panel + I_link  # kg*m^2, moment of inertia of one link about its own CM

N_springs = n_links               # N, number of hinge-spring joints
N_kinks = n_links                  # Nk, number of tube kink joints

# No bench test of hinge friction was feasible before the spring buy, so rather
# than trust the earlier flat 0.5 N guess, F_friction is set an order of
# magnitude above it (10x) as a deliberate no-data worst case for an untested,
# multi-joint (n_links=7) mechanism with harnessing/thermal drag that a simple
# estimate easily misses. This makes k_min (Phase1.py) large enough that Phase 1
# now finishes *faster* than t_deploy under any feasible spring -- that's fine,
# finishing early carries no penalty; only finishing late (stalling) does.
F_friction = 5.0                   # N, hinge friction force per joint (conservative, untested)
tau_friction = F_friction * r_o     # N*m, resisting torque per joint (conservative, untested)

# Sizing the spring against the bare nominal friction estimate left ~1% margin
# over the minimum k that can overcome friction at all (k_min in Phase1.py) --
# any unmodeled friction (stiction, thermal effects, harness drag, tolerance)
# would stall deployment before reaching theta_1. Size the spring against an
# inflated friction budget instead, so the built spring has real margin against
# the nominal estimate above.
friction_safety_factor = 1.5
tau_friction_design = tau_friction * friction_safety_factor  # N*m, used for spring sizing

# With F_friction this conservative, k_min already clears t_deploy faster than
# budgeted (see required_k's fallback in Phase1.py), so the time-match no longer
# binds. Size the spring with this much torque margin over k_min instead, so it
# has real reserve against friction the same 5.0 N design value still underrates.
spring_margin_over_kmin = 1.5

handoff_margin = 0.5
total_deploy_time = 12.0 * 3600.0      # s, 12 hr total deployment budget
t_deploy = total_deploy_time / 12.0    # s, Phase 1 duration = (1/4) of (1/3) of total -> 1 hr
t2_deploy = total_deploy_time - t_deploy  # s, Phase 2 duration = remainder after Phase 1 -> 11 hr

M_j = 2 * m_link + panels_per_link * m_radiator   # total mass carried by one link

theta_0 = np.pi / 2                            # stowed angle, start of Phase 1

theta_min_deg = 10.0                # deg, fully-deployed target angle              [PLACEHOLDER]
theta_min = np.radians(theta_min_deg)

R_tube = 0.1                       # m, chosen inflated tube radius (design choice) [PLACEHOLDER]
a_kink = 1.0                        # bench-test empirical constant, both closures  [PLACEHOLDER]

N_M_TO_IN_LBF = 8.85074579
