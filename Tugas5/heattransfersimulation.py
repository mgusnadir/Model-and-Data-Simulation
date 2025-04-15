import numpy as np
import matplotlib.pyplot as plt

# Parameters
initial_temperature = 25     # Initial object temperature
ambient_temperature = 100    # Room temperature
heating_rate = 0.05          # Rate of heat gain
cooling_rate = 1             # Rate of heat loss
time_steps = 200             # Total simulation time
dt = 0.1                     # Small time step

# Initialize arrays
time = np.arange(0, time_steps * dt, dt)
temperature = np.zeros(len(time))
temperature[0] = initial_temperature

## Euler's Method to Solve dT/dt = -k (T - T_ambient)
# for t in range(1, len(time)):
#     dT = -cooling_rate * (temperature[t-1] - ambient_temperature) * dt
#     temperature[t] = temperature[t-1] + dT
    
for t in range(1, len(time)):
    dT = heating_rate * (ambient_temperature - temperature[t-1]) * dt
    temperature[t] = temperature[t-1] + dT

# Plot results
plt.plot(time, temperature, label="Object Temperature")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
# plt.title("Newton's Law of Cooling Simulation")
plt.title("Newton's Law of Heating Simulation")
plt.legend()
plt.grid()
plt.show()