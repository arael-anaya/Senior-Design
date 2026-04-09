import numpy as np
import matplotlib.pyplot as plt

def simulate_xrad_deployment():
    # --- 1. USER SPECIFIED DIMENSIONS ---
    n_panels = 7
    panel_mass_kg = 66 * 0.453592   # 66 lbm to kg (~29.9 kg)
    bar_length_m = 48 * 0.0254      # 48 inches to meters (~1.22 m)
    
    # Structural Params
    bar_mass_kg = 5.0               # Estimated mass for aluminum 6061-T6 bars per stage
    total_mass_per_stage = panel_mass_kg + (2 * bar_mass_kg)
    total_system_mass = total_mass_per_stage * n_panels
    total_deployed_length = n_panels * bar_length_m
    
    # --- 2. ACTUATION PARAMETERS ---
    p_initial = 405300              # 4.0 atm (higher pressure for 7 stages)
    v_dead_space = 0.002            # m^3 (larger reservoir for more stages)
    b_radius = 0.06                 # 60mm bellows (increased for higher torque)
    b_arm = 0.07                    # meters (larger hinge offset)
    gamma = 1.4                     # Nitrogen adiabatic index
    
    # Resistance
    k_stiffness = 0.8               # N-m/rad (stiffer fluid lines for 7 panels)
    f_latch_click = 40.0            # Newtons (sturdier latch for heavy panels)
    h_radius = 0.035                # Hinge radius
    mu = 0.2                        # Friction
    
    # --- 3. KINEMATICS ---
    theta_deg = np.linspace(5, 90, 200)
    theta_rad = np.radians(theta_deg)
    
    # Moment of Inertia for the whole wing rotating about base hinge
    # I = 1/3 * M * L^2
    I_total = (1/3) * total_system_mass * (total_deployed_length)**2
    
    # --- 4. CALCULATIONS ---
    # Expansion volume (Cumulative across all 7 stages)
    # Each stage has a bellows; they all expand together.
    delta_v_per_hinge = (np.pi * b_radius**2) * (b_radius * theta_rad)
    total_delta_v = delta_v_per_hinge * n_panels
    
    v_total = v_dead_space + total_delta_v
    p_current = p_initial * (v_dead_space / v_total)**gamma
    
    # Torque per hinge
    t_nitrogen = p_current * (np.pi * b_radius**2) * b_arm
    t_latch_req = f_latch_click * mu * h_radius
    
    # Net Energy (Work Done)
    t_resistive = k_stiffness * theta_rad
    t_net = t_nitrogen - t_resistive
    work_done = np.trapz(t_net, theta_rad)
    
    # Final Velocity
    omega_final = np.sqrt(2 * work_done / I_total)
    v_tip = omega_final * total_deployed_length

    # --- 5. OUTPUTS ---
    print("--- xRAD Deployment Analysis (7 Panels) ---")
    print(f"Total Deployed Length: {total_deployed_length:.2f} m ({total_deployed_length*3.28:.1f} ft)")
    print(f"Total System Mass:     {total_system_mass:.2f} kg")
    print(f"End-of-Stroke Torque:  {t_nitrogen[-1]:.2f} N-m")
    print(f"Tip Velocity:          {v_tip:.2f} m/s")
    print(f"Impact Energy:         {work_done:.2f} Joules")
    print("-" * 43)

    # Simple plot
    plt.figure(figsize=(8, 4))
    plt.plot(theta_deg, t_nitrogen, label='Nitrogen Torque')
    plt.axhline(y=t_latch_req, color='r', linestyle='--', label='Latch Threshold')
    plt.title('7-Panel Radiator Deployment Torque')
    plt.xlabel('Hinge Angle (deg)')
    plt.ylabel('Torque (N-m)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    simulate_xrad_deployment()