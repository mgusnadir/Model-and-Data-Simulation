import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/mgusn/OneDrive/Documents/alay sat/Semester 8/Pemodelan dan Simulasi Data/Tugas5/london_weather.csv")
mean_temps = df['mean_temp'].dropna().values  # ambil suhu lingkungan harian

initial_temperature = 20  # Suhu awal benda
heating_rate = 0.05

time = np.arange(len(mean_temps))  # Hari ke-i
object_temperature = np.zeros(len(time))
object_temperature[0] = initial_temperature

for t in range(1, len(time)):
    dT = heating_rate * (mean_temps[t] - object_temperature[t-1])
    object_temperature[t] = object_temperature[t-1] + dT

plt.plot(time, mean_temps, label="Ambient Temperature (London)", color='blue')
plt.plot(time, object_temperature, label="Simulated Object Temperature", color='red')
plt.xlabel("Time (days)")
plt.ylabel("Temperature (°C)")
plt.title("Simulasi Pemanasan Berdasarkan Data Cuaca Nyata")
plt.legend()
plt.grid()
plt.show()


