# -*- coding: utf-8 -*-
"""
Upgraded Fan Curve Analysis Tool
Original Author: bmusammartanoV
"""

import matplotlib.pyplot as plt
import numpy as np


def eq_fit(name, x, y, subplot_index, degree=4):
    """Fit polynomial to data and plot results."""
    coeff = np.polyfit(x, y, degree)
    poly = np.poly1d(coeff)

    axs[subplot_index].plot(x, poly(x), "ob", label="Polynomial Fit")
    axs[subplot_index].plot(x, y, "--r", label="Original Data")
    axs[subplot_index].set_title(name)
    axs[subplot_index].legend()
    
    RMS_error = np.sqrt(np.mean((y - poly(x))**2))
    
    # Build readable equation string
    terms = [f"{round(c,3)}*V^{i}" for i, c in zip(range(degree, -1, -1), coeff)]
    eq_str = " + ".join(terms)
    
    print(f"\nEquation for {name}:\n{eq_str}")
    print(f"Root Mean Square Error: {RMS_error:.5f}")
    
    return poly, eq_str, RMS_error

def estimate_velocity_from_pressure(poly, target_pressure):
    """Estimate velocity(s) given a pressure using the fitted polynomial."""
    adjusted_poly = poly - target_pressure
    roots = adjusted_poly.r
    real_velocities = sorted([v.real for v in roots if np.isreal(v) and v.real >= 0])

    if real_velocities:
        formatted = ", ".join([f"{v:.2f} m/s" for v in real_velocities])
        print(f"\nEstimated normal velocity and flow rate at {target_pressure} Pa:\nVn = {formatted} m/s")
    else:
        print("\nNo real positive velocity found for that pressure.")
    return real_velocities


def estimate_flow_rate_for_pressure(poly, target_pressure, area):
    """Estimate flow rate(s) for a specific pressure and area."""
    velocities = estimate_velocity_from_pressure(poly, target_pressure)
    if velocities:
        flow_rates = [area * v for v in velocities]
        flow_rates_h = [area * v *3600 for v in velocities]
        formatted = ", ".join([f"{q:.3f} m³/s" for q in flow_rates])
        formatted_h = ", ".join([f"{q:.3f} m³/h" for q in flow_rates_h])
        print(f"Flow rate = {formatted}")

        print(f"Flow rate = {formatted_h}")

        return flow_rates
    return []


# === Data Acquisition ===
filename = "fan_FR451.txt"
velocity = []
dp = []

with open(filename, "r") as fid:
    next(fid)  # skip header
    for line in fid:
        vals = line.strip().split("\t")
        velocity.append(float(vals[0]))
        dp.append(float(vals[1]))

# Convert to numpy arrays
Vel = np.array(velocity)
DP = np.array(dp)

# === Plot and Fit ===
fig, axs = plt.subplots(2, figsize=(10, 10))
fig.subplots_adjust(hspace=0.5)

if __name__ == '__main__':
    poly, eq_str, rms = eq_fit("Fan Curve FR451", Vel, DP, 0, degree=3)
    
    try:
        target_dp = float(input("Enter Pressure (Pa): "))
        area = float(input("Enter Cross-sectional Area (m²): "))
        estimate_flow_rate_for_pressure(poly, target_dp, area)
    except ValueError:
        print("Invalid input. Please enter numeric values.")
    
    #plt.show()
