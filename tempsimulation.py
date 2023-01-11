import math

# Constants
DROPLET_MASS = 0.05  # kg
DROPLET_TEMP = 20  # Initial temperature of the droplet (Celsius)
DROPLET_SURFACE_AREA = math.pi * (0.05 / 2)**2 # Surface area of droplet (m^2)
TARGET_TEMP = 30  # Target temperature of the droplet (Celsius)
AMBIENT_TEMP = 20  # Temperature of the environment (Celsius)
LAMP_TEMP = 300  # Temperature of the lamp (Kelvin)
LAMP_HEAT_TRANSFER_COEFFICIENT = 2 # Heat transfer coefficient between the droplet and the lamp (W/m^2 * K)
ENVIRONMENT_HEAT_TRANSFER_COEFFICIENT = 15 # Heat transfer coefficient between the droplet and the environment (W/m^2 * K)

# Simulation parameters
TIME_STEP = 0.1  # Time step (seconds)
SIMULATION_TIME = 3600  # Total simulation time (seconds)

# Initialize variables
droplet_temp = DROPLET_TEMP
time = 0
lamp_on = True
cycle_time = 0


# Simulation loop
while time < SIMULATION_TIME:
    # Calculate energy lost from the droplet to the environment
    energy_lost = ENVIRONMENT_HEAT_TRANSFER_COEFFICIENT * DROPLET_SURFACE_AREA * (droplet_temp - AMBIENT_TEMP) * TIME_STEP
    
    if lamp_on:
        # Calculate energy added to the droplet by the lamp
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
    print(lamp_on, droplet_temp, time)

# Print the result
print("The lamp should have cycle time of ", cycle_time, "seconds.")