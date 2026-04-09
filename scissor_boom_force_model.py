"""
scissor_boom_quasistatic.py

Quasi-static actuator force model for a scissor boom.

This file estimates the actuator force required to extend a planar scissor
mechanism under a quasi-static assumption.

"Quasi-static" means:
- motion is slow enough that inertia is neglected
- acceleration terms do not matter
- required actuator force comes only from geometric mechanical advantage
and resistance sources such as hinge friction and rail friction

Mechanism assumption used here:
- one end of the system is pinned
- the opposite end is constrained to slide on a rail
- the actuator pushes along that rail direction
- theta is the arm angle used to describe the configuration

Units used internally:
- length: meters
- force: Newtons
- torque: N*m
- angles: radians for trig, degrees for user-facing sweeps/prints
"""

# NumPy is used for array math, linspace, radians conversion, and vectorized trig.
import numpy as np
# Matplotlib is used for plotting force vs length / angle.
import matplotlib.pyplot as plt
# math is imported for standard scalar math utilities if needed.
import math
# dataclass gives us a clean parameter container with defaults.
from dataclasses import dataclass

@dataclass
class Params:
    """
    Container for all model parameters.
    These are the physical and numerical inputs to the quasi-static model.
    """

    # Number of repeated scissor bays in the mechanism.
    n_bays: int = 7

    # Length of one arm in meters.
    # Here 1.524 m = 60 in.
    L: float = 1.524

    # Mass of one radiator panel in kg.
    panel_mass: float = 29.937

    # Number of panels per bay.
    # Also currently unused in the quasi-static friction-only model.
    panels_per_bay: int = 1

    # Constant Coulomb-like friction torque at each hinge, in N*m.
    # This resists motion regardless of speed direction magnitude.
    hinge_friction_torque: float = 0

    # Number of hinges per bay included in the resistance estimate.
    hinges_per_bay: int = 2

    # Constant linear friction force in the rail, in N.
    rail_friction: float = 0

    theta_start = 85
    theta_end = 15

    n = 50000

    tol: float = 1e-8
    
"""
Parameters
----------
theta : float or array
    Scissor angle in radians.
p : Params
    Model parameters.
Returns
-------
float or array
    Horizontal boom extension in meters.
"""
def X(theta, p):
    """
    Return the horizontal projected boom length.
    Kinematics:
        For one bay, horizontal projection = L * cos(theta)
        For n_bays identical bays:
            X(theta) = n_bays * L * cos(theta)
    """
    return p.n_bays * p.L * np.cos(theta)

"""
Parameters
----------
theta : float or array
    Scissor angle in radians.
p : Params
    Model parameters.
Returns
-------
float or array
    Vertical slider position in meters.
"""
def Y(theta, p):
    """
    Return the vertical slider position / scissor height.
    Kinematics:
        For one bay, vertical projection = L * sin(theta)
        For n_bays:
            Y(theta) = n_bays * L * sin(theta)
    In this simplified model, the actuated rail motion is represented by Y.
    """
    return p.n_bays * p.L * np.sin(theta)

"""
Parameters
----------
theta : float or array
    Scissor angle in radians.
p : Params
    Model parameters.
Returns
-------
float or array
    Derivative dY/dtheta with units of m/rad.
"""
def dY_dtheta(theta, p):
    """
    Return the derivative of slider position with respect to theta.
    Since:
        Y(theta) = n_bays * L * sin(theta)
    Then:
        dY/dtheta = n_bays * L * cos(theta)
    Physical meaning:
    - This is the geometric Jacobian term relating a small angular change dtheta
        to a small slider motion dY.
    - It is also the key mechanical-advantage term in the virtual work equation.
    """
    return p.n_bays * p.L * np.cos(theta)

"""
Parameters
----------
p : Params
    Model parameters.
Returns
-------
float
    Total resisting generalized torque from hinges, in N*m.
"""
def hinge_resistance(p):
    return p.n_bays * p.hinges_per_bay * p.hinge_friction_torque

"""
Parameters
----------
theta : float or array
    Scissor angle in radians.
p : Params
    Model parameters.
Returns
-------
float or array
    Rail resistance expressed as generalized torque, in N*m.
"""
def rail_resistance(theta, p):
    """
    Convert rail friction force into generalized resistance in theta-space.
    Rail friction is modeled as a constant linear force opposing slider motion:
        F_rail = rail_friction
    Using virtual work:
        Q_theta * dtheta = F_rail * dY
    Therefore:
        Q_theta = F_rail * (dY/dtheta)
    We use absolute value because we care about magnitude of required force.
    """
    return p.rail_friction * abs(dY_dtheta(theta, p))

"""
Parameters
----------
theta : float or array
    Scissor angle in radians.
p : Params
    Model parameters.
Returns
-------
float or array
    Total generalized resistance in N*m.
"""
def total_generalized_resistance(theta, p):
    """
    Return total generalized resistance.
    This simply adds the resistance contributions from:
    - hinge friction
    - rail friction mapped into theta-space
    """
    return hinge_resistance(p) + rail_resistance(theta, p)

""" 
Parameters
----------
theta : float
    Scissor angle in radians.
p : Params
    Model parameters.

Returns
-------
float
    Actuator force in Newtons.
"""
def actuator_force(theta, p):
    """
    Compute actuator force required at a given configuration.
    Core quasi-static virtual-work relation:
        F_act * dY = Q_theta * dtheta
    Rearranging:
        F_act = Q_theta / (dY/dtheta)
    We use absolute value on dY/dtheta because we are calculating required
    force magnitude.

    Singularity:
    - if dY/dtheta is near zero, the actuator has almost no leverage
    - the ideal required force tends to infinity
    - we return np.inf in that case

    """
    # Geometric leverage / Jacobian term.
    lever = abs(dY_dtheta(theta, p))
    # If the leverage is too small, treat configuration as singular.
    if lever < p.tol:
        return np.inf
    # Total generalized resisting load.
    Q = total_generalized_resistance(theta, p)
    # Virtual-work conversion from generalized torque to linear actuator force.
    return Q / lever

"""
Parameters
----------
p : Params
    Model parameters.
theta_start : float
    Starting angle in degrees.
theta_end : float
    Ending angle in degrees.
n : int
    Number of sample points.

Returns
-------
tuple
    theta_deg : array of angles in degrees
    theta     : array of angles in radians
    force     : actuator force array in N
    length    : boom length array in m
    height    : slider height array in m
"""
def sweep(p):
    """
    Evaluate the model over a range of scissor angles.
    """
    # Create evenly spaced angle samples in degrees for easier interpretation.
    theta_deg = np.linspace(p.theta_start, p.theta_end, p.n)

    # Convert to radians because trig functions use radians.
    theta = np.radians(theta_deg)

    # Evaluate actuator force at each configuration.
    force = np.array([actuator_force(t, p) for t in theta])

    # Evaluate horizontal boom length at each configuration.
    length = X(theta, p)

    # Evaluate vertical slider position at each configuration.
    height = Y(theta, p)

    return theta_deg, theta, force, length, height

"""
Parameters
----------
theta_deg : array
    Angle samples in degrees. Not directly used here but kept for consistency.
force : array
    Actuator force in Newtons.
length : array
    Boom length in meters.
"""
def plot_all(theta_deg, force, length):
    length_in = metersToInches(length)
    force_lbf = newtonToLbf(force)

    fig, axs = plt.subplots(1, 2, figsize=(12,5))

    # Force vs length
    axs[0].plot(length_in, force_lbf)
    axs[0].set_title("Force vs Length")
    axs[0].set_xlabel("Length (in)")
    axs[0].set_ylabel("Force (lbf)")
    axs[0].grid()

    # Force vs theta
    axs[1].plot(theta_deg, force_lbf)
    axs[1].set_title("Force vs Theta")
    axs[1].set_xlabel("Theta (deg)")
    axs[1].set_ylabel("Force (lbf)")
    axs[1].grid()

    plt.tight_layout()
    plt.show()
    """
    Plot actuator force versus theta.
    """
    # Create a new figure.
    plt.figure(figsize=(10, 6))

    # Convert force from N to lbf.
    plt.plot(theta_deg, force)

    # Label x-axis.
    plt.xlabel("Theta (deg)")

    # Label y-axis.
    plt.ylabel("Force (lbf)")

    # Give plot a title.
    plt.title("Force vs Angle")

    # Show grid for readability.
    plt.grid()

    # Display figure.
    plt.show()


def metersToInches(length):
    return length*39.37

def newtonToLbf(force):
    return force * 0.224809

def main():
    """
    Main driver function.
    This:
    1. creates the parameter object
    2. sweeps across a range of angles
    3. finds the peak actuator force
    4. prints summary information
    5. plots force vs extension
    """
    # Instantiate the parameter set used by the model.
    p = Params(
        # Number of repeated scissor bays.
        n_bays=7,
        # Arm length in meters (60 in).
        L=1.524,
        # Panel mass in kg.
        # Currently does not affect this quasi-static friction-only model.
        panel_mass=29.937,
        # One panel per bay.
        panels_per_bay=1,
        # Per-hinge friction torque in N*m.
        # This is one of the main quantities to tune to match reality.
        hinge_friction_torque=0.5,
        # Rail friction force in N.
        # This is the other main quantity to tune.
        rail_friction=10
    )
    # Run the model over the default angle sweep.
    theta_deg, theta, force, length, height = sweep(p)
    length_in = metersToInches(length)
    force_lbf = newtonToLbf(force)
    # Find the index of the maximum finite force value.
    # np.isfinite(force) removes infinities from singular configurations.
    idx = np.argmax(force[np.isfinite(force)])
    # Print peak force in Newtons.
    print("Peak Force (N):", force[idx])
    # Print peak force converted to lbf.
    print("Peak Force (lbf):", force_lbf[idx])
    # Print the angle where peak force occurs.
    print("At theta:", theta_deg[idx])
    # Print the boom length at the peak-force location.
    print("At length (in):", length_in[idx])
    # Print the final boom length at the last point in the sweep.
    print("Final length (in):", length_in[-1])

    # Plot actuator force vs boom extension.
    plot_all(theta_deg , force_lbf , length_in)


if __name__ == "__main__":
    main()
    



