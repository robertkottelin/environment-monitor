struct WaterDroplet {
    temperature: f32,
    starting_temperature: f32,
    temperature_capacity: f32,
    heat_transfer_coefficient: f32,
    surface_area: f32,
}

struct HeatSource {
    heat_output: f32,
    efficiency: f32,
    temperature: f32,
}

fn main() {
    // Create an instance of the water droplet struct with a starting temperature slightly lower than the target temperature, a temperature capacity of 4.2 J/degree, and a heat transfer coefficient of 100 W/m^2K
    let mut droplet = WaterDroplet {
        temperature: 22.0,
        starting_temperature: 22.0,
        temperature_capacity: 4.2,
        heat_transfer_coefficient: 75.0,
        surface_area: 0.0005,
    };

    // Create an instance of the heat source struct with a heat output of 10 and an efficiency of 0.5
    let heat_source = HeatSource {
        heat_output: 10.0,
        efficiency: 0.5,
        temperature: 50.0, 
    };

    // Set the target temperature
    let target_temperature = 30.0;

    // Initialize a counter to track the number of times the heat source is turned on
    let mut heat_source_on_count = 0;

    // Initialize a variable to track the elapsed time between firings of the heat source
    let mut elapsed_time_between_firings = 0.0;

    // Initialize a flag to track whether the heat source is currently on
    let mut heat_source_on = false;

    // Initialize a flag to track the previous heat source on status
    let mut heat_source_on_previous = false;

    // Run the simulation in a loop
    loop {
        
        /*
        Q = h * A * (T1 - T2) * t

            where:

            Q is the heat transfer (in Joules)

            h is the heat transfer coefficient (in W/m^2*K)

            A is the surface area of the water droplet (in m^2)

            T1 is the temperature of the lamp (in K)

            T2 is the initial temperature of the water droplet (in K)

            t is the duration of the heat transfer (in seconds)
                
        */

        // Calculate the rate of temperature change of the water droplet based on the heat transfer coefficient, the surface area of the water droplet, the temperature difference between the heat source and the water droplet, and the elapsed time between firings
        let rate_of_temperature_change = droplet.heat_transfer_coefficient * droplet.surface_area * (heat_source.temperature - droplet.temperature) * elapsed_time_between_firings;
    
        // Update the temperature of the water droplet based on the rate of temperature change of the water droplet and the heat output of the lamp
        if heat_source_on {
            droplet.temperature += heat_source.heat_output * heat_source.efficiency - rate_of_temperature_change;
        } else {
            droplet.temperature -= rate_of_temperature_change;
        }
    
        // Check if the temperature of the water droplet has reached or exceeded the target temperature
        if droplet.temperature >= target_temperature {
            // If the temperature has reached or exceeded the target temperature, turn off the heat source
            heat_source_on = false;
        } else if droplet.temperature < target_temperature {
            // If the temperature has not reached the target temperature, turn on the heat source
            heat_source_on = true;
        }
    
        // If the heat source has just been turned on, reset the elapsed time between firings
        if heat_source_on && !heat_source_on_previous {
            elapsed_time_between_firings = 0.0;
        }
    
        // If the heat source is currently on, increment the elapsed time between firings
        if heat_source_on {
            elapsed_time_between_firings += 1.0;
        }
    
        // Calculate the average time between firings of the heat source
        let average_time_between_firings = elapsed_time_between_firings / (heat_source_on_count as f32);

        // Print the current temperature, the heat source on flag, and the average time between firings
        println!("Temperature: {}, Heat source on: {}, Average time between firings: {}", droplet.temperature, heat_source_on, average_time_between_firings);
    
        // Sleep for 1 second to allow the temperature to update
        std::thread::sleep(std::time::Duration::from_secs(1));
    
        // Update the previous heat source on flag
        heat_source_on_previous = heat_source_on;
    
        // // If the temperature of the water droplet has fallen below the starting temperature, break out of the loop to end the simulation
        // if droplet.temperature < droplet.starting_temperature {
        //     break;
        // }
    }
    
}
