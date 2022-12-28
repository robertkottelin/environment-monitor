mod ds18b20;
mod w1_errors;
mod control_lamp;
use rand::{thread_rng, Rng};

static USE_RANDOM_DATA: bool = true;
static RUN_PROGRAM: bool = true;
static SET_TEMPERATURE: f64 = 22.0;

// Use random temperature for testing when sensor is disconnected
fn random_int() -> f64 {
    let mut rng = thread_rng();
    rng.gen_range(20.0..26.0)
}

fn main() {
    while RUN_PROGRAM == true {
        let temp_random: f64;
        if USE_RANDOM_DATA {
            temp_random = random_int() as f64;
            println!("Temperature: {:?}", temp_random);

            if temp_random > SET_TEMPERATURE {
                match control_lamp::control_lamp(false) {
                    Ok(()) => println!("Lamp control succeeded, lamp off."),
                    Err(e) => println!("Lamp control failed: {}", e),
                }
            } else {
                match control_lamp::control_lamp(true) {
                    Ok(()) => println!("Lamp control succeeded, lamp on."),
                    Err(e) => println!("Lamp control failed: {}", e),
                }
            }
        } else {
            match ds18b20::DS18B20::new() {
                Ok(sensor) => {
                    match sensor.read_temp() {
                        Ok(temp) => {
                            println!("Temperature: {:?}", temp);

                            if temp.to_celsius() > SET_TEMPERATURE {
                                match control_lamp::control_lamp(false) {
                                    Ok(()) => println!("Lamp control succeeded, lamp off."),
                                    Err(e) => println!("Lamp control failed: {}", e),
                                }
                            } else {
                                match control_lamp::control_lamp(true) {
                                    Ok(()) => println!("Lamp control succeeded, lamp on."),
                                    Err(e) => println!("Lamp control failed: {}", e),
                                }
                            }
                        }
                        Err(e) => println!("Failed to read temperature: {}", e),
                    }
                }
                Err(e) => println!("Failed to create DS18B20 sensor: {}", e),
            }
        }
    }
}


