import math
import matplotlib.pyplot as plt

# Constants
DROPLET_MASS = 0.05  # kg
DROPLET_TEMP = 20  # Initial temperature of the droplet (Celsius)
DROPLET_SURFACE_AREA = math.pi * (0.05 / 2)**2 # Surface area of droplet (m^2)
TARGET_TEMP = 30  # Target temperature of the droplet (Celsius)
AMBIENT_TEMP = 20  # Temperature of the environment (Celsius)
LAMP_POWER = 5 # Power of the lamp (Watts)
DISTANCE = 1  # Distance between the droplet and the lamp (m)
LAMP_TEMP = 280 
LAMP_HEAT_TRANSFER_COEFFICIENT = 2 # Heat transfer coefficient between the droplet and the environment (W/m^2 * K)
ENVIRONMENT_HEAT_TRANSFER_COEFFICIENT = 15 # Heat transfer coefficient between the droplet and the environment (W/m^2 * K)

# Simulation parameters
TIME_STEP = 1.0  # Time step (seconds)
SIMULATION_TIME = 60*60  # Total simulation time (seconds)

# Initialize variables
droplet_temp = DROPLET_TEMP
time = 0
lamp_on = True
cycle_time = 0

# Initialize lists to store data for plotting
time_list = []
temp_list = []

# Simulation loop
while time < SIMULATION_TIME:
    # Calculate energy lost from the droplet to the environment
    energy_lost = ENVIRONMENT_HEAT_TRANSFER_COEFFICIENT * DROPLET_SURFACE_AREA * (droplet_temp - AMBIENT_TEMP) * TIME_STEP
    
    if lamp_on:
        # Calculate energy added to the droplet by the lamp using the inverse square law of radiation
        energy_added = LAMP_HEAT_TRANSFER_COEFFICIENT * DROPLET_SURFACE_AREA * (LAMP_TEMP - droplet_temp) * TIME_STEP

        # Calculate the new temperature of the droplet
        droplet_temp += (energy_added - energy_lost) / (DROPLET_MASS * 4186)
        
        if droplet_temp > TARGET_TEMP:
            lamp_on = False
            cycle_time = time
    else:
        # Calculate the new temperature of the droplet
        droplet_temp -= energy_lost / (DROPLET_MASS * 4186)
        
        if droplet_temp < TARGET_TEMP:
            lamp_on = True
            cycle_time = time - cycle_time
    time += TIME_STEP
    
    # Append current time and temperature to lists
    time_list.append(time)
    temp_list.append(droplet_temp)
    # print(droplet_temp, lamp_on)

# Print the result
print("The lamp should have cycle time of ", cycle_time, "seconds.")

# Plot the temperature over time
plt.plot(time_list, temp_list)
plt.xlabel('Time (s)')
plt.ylabel('Temperature (C)')
plt.show()