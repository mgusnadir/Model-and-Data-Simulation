import numpy as np
import matplotlib.pyplot as plt

# Parameters
initial_temperature = 25     # Initial object temperature
ambient_temperature = 100    # Room temperature
heating_rate = 0.05          # Rate of heat gain
time_steps = 200             # Total simulation time
dt = 0.1                     # Small time step
event_interval = 10          # Interval for discrete events (DES)

# Initialize arrays
time = np.arange(0, time_steps * dt, dt)
temperature_ces = np.zeros(len(time))  # CES temperature array
temperature_des = []  # DES temperature array (only stores temperatures at event points)

temperature_ces[0] = initial_temperature
temperature_des.append(initial_temperature)

# Continuous Event Simulation (CES) - Euler's method for continuous changes
for t in range(1, len(time)):
    dT = heating_rate * (ambient_temperature - temperature_ces[t-1]) * dt
    temperature_ces[t] = temperature_ces[t-1] + dT

# Discrete Event Simulation (DES) - Only update temperature at event intervals
for t in range(1, time_steps):
    if t % event_interval == 0:  # Update temperature every event_interval time steps
        dT = heating_rate * (ambient_temperature - temperature_des[-1]) * (event_interval * dt)
        temperature_des.append(temperature_des[-1] + dT)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(time, temperature_ces, label="CES - Continuous Event Simulation", color='b')
plt.plot(np.arange(0, time_steps * dt, event_interval * dt), temperature_des, label="DES - Discrete Event Simulation", color='r', marker='o')
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.title("Comparison of CES and DES for Heat Transfer Simulation")
plt.legend()
plt.grid()
plt.show()

