// Import the `ds18b20` and `w1_errors` modules, which provide functions and types
// for interacting with a DS18B20 temperature sensor
mod ds18b20;
mod w1_errors;

// Import the `thread_rng` and `Rng` types from the `rand` crate, which provide
// functions for generating random numbers
use rand::{thread_rng, Rng};

// Import the `thread` module from the standard library, which provides functions
// for creating and working with threads in Rust
use std::thread;

// Define a function that generates a random integer in the range [20, 26)
fn random_int() -> i32 {
    // Create a thread-local random number generator
    let mut rng = thread_rng();

    // Use the random number generator to generate a random integer in the specified range
    rng.gen_range(20..26)
}

// Define a constant that controls whether the program should use random data or real data
// from the temperature sensor. Set it to `true` to use random data, or `false` to use real data.
static USE_RANDOM_DATA: bool = true;

// Define a constant that controls whether the program should continue running or not.
// Set it to `true` to run the program, or `false` to stop the program.
static RUN_PROGRAM: bool = true;

fn main() {
    // Create a vector to hold the spawned threads
    let mut threads = Vec::new();

    // Spawn four threads
    for _ in 0..8 {
        // Push a new thread onto the vector
        threads.push(thread::spawn(|| {
            // Run the loop until the `RUN_PROGRAM` constant is set to `false`
            while RUN_PROGRAM == true {
                // Declare a variable to hold the temperature data
                let temp_random: f32;

                // Check whether to use random data or real data
                if USE_RANDOM_DATA {
                    // Generate a random temperature value
                    temp_random = random_int() as f32;

                    // Print the temperature value to the console
                    println!("Temperature: {:?}", temp_random)
                } else {
                    // Create a new instance of the `DS18B20` type from the `ds18b20` module
                    let sensor = ds18b20::DS18B20::new().unwrap();

                    // Read the temperature from the sensor
                    let temp = sensor.read_temp().unwrap();

                    // Print the temperature value to the console
                    println!("Temperature: {:?}", temp)
                }
            }
        }));
    }

    // Wait for all of the spawned threads to complete
    for thread in threads {
        thread.join().unwrap();
    }
}
