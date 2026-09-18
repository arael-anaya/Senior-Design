"""
Bench-test design parameters for the small-scale Phase 1 / Phase 2 test article.

Mirrors params.py's variable set so it can be swapped in wholesale via
params.USE_TESTING_PARAMS. Unlike params.py, the link here is not modeled as
a hollow tube -- the test link is a flat aluminum bar with measured mass, so
m_link and I_link come from the bench measurement/geometry directly instead
of a tube-volume calculation.
"""

import numpy as np

IN2M = 0.0254   # in -> m

n_links = 2                     # n, number of scissor links/bays
panels_per_link = 1              # number of radiator panels carried per link

# I_eff(theta) sums the per-link (1/2 - i)^2 velocity-coefficient term over every
# link (Derivation/main.tex eq. Texp), which reduces to sum_{i=1}^{n} i(i-1) once
# the 1/4 constant is folded in.
S1_link_index = n_links * (n_links + 1) * (n_links - 1) / 3.0   # sum_{i=1}^{n} i(i-1)

# Material Density
rho_al = 2810.0                  # kg/m^3, Al 7075-T6

# Radiator Panel (bench-test scale)
panel_overhang = 0.254                     # m, 10 in link overhang beyond the panel
panel_thickness = 0.125 * IN2M             # m, 1/8 in
panel_length = 21.3 * IN2M                 # m, 21.3 in
panel_width = 8.0 * IN2M                   # m, 8 in

m_radiator = rho_al * panel_length * panel_width * panel_thickness   # kg

# LINK -- bench-test link is a flat bar, not a hollow tube, so its mass and
# inertia are built from the measured bar directly rather than tube_OD/tube_wall.
link_length = 10.0 * IN2M          # m, 10 in
link_width = 0.75 * IN2M           # m, 0.75 in
link_thickness = 0.125 * IN2M      # m, 0.125 in
link_hole_dia = 0.25 * IN2M        # m, 1/4 in hinge-pin holes
n_link_holes = 3                   # count of 1/4 in holes in the link

m_link = 0.0404                    # kg, measured mass of the bench-test link

# The friction torque model (below) uses r_o as the hinge-pin moment arm, so
# for this flat-bar link r_o is the hinge-pin hole radius rather than a tube OD.
tube_OD = link_hole_dia            # m, kept for interface parity with params.py
tube_wall = link_thickness         # m, kept for interface parity with params.py
r_o = tube_OD / 2.0
r_i = 0.0                          # not applicable to a solid flat bar

# Inertias
I_panel = (m_radiator / 12.0) * (panel_length**2 + panel_thickness**2)
I_link = (m_link / 12.0) * (link_length**2 + link_thickness**2)   # flat-bar formula
I_j = I_panel + I_link  # kg*m^2, moment of inertia of one link about its own CM

N_springs = n_links               # N, number of hinge-spring joints
N_kinks = n_links                  # Nk, number of tube kink joints

F_friction = 5.0                   # N, hinge friction force per joint (conservative, untested)
tau_friction = F_friction * r_o     # N*m, resisting torque per joint (conservative, untested)

friction_safety_factor = 1.5
tau_friction_design = tau_friction * friction_safety_factor  # N*m, used for spring sizing

spring_margin_over_kmin = 1.5

handoff_margin = 0.5
total_deploy_time = 12.0 * 3600.0      # s, 12 hr total deployment budget
t_deploy = total_deploy_time / 12.0    # s, Phase 1 duration
t2_deploy = total_deploy_time - t_deploy  # s, Phase 2 duration

M_j = 2 * m_link + panels_per_link * m_radiator   # total mass carried by one link

theta_0 = np.pi / 2                            # stowed angle, start of Phase 1

theta_min_deg = 10.0                # deg, fully-deployed target angle              [PLACEHOLDER]
theta_min = np.radians(theta_min_deg)

R_tube = 0.1                       # m, chosen inflated tube radius (design choice) [PLACEHOLDER]
a_kink = 1.0                        # bench-test empirical constant, both closures  [PLACEHOLDER]

N_M_TO_IN_LBF = 8.85074579
