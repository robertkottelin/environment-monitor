mod ds18b20;
mod w1_errors;
mod control_lamp;
use rand::{thread_rng, Rng};
use std::thread;

fn random_int() -> f64 {
    let mut rng = thread_rng();
    rng.gen_range(20.0..26.0)
}

static USE_RANDOM_DATA: bool = true;
static RUN_PROGRAM: bool = true;
static SET_TEMPERATURE: f64 = 22.0;

fn main() {
    while RUN_PROGRAM == true {
        let temp_random: f64;
        if USE_RANDOM_DATA {
            temp_random = random_int() as f64;
            println!("Temperature: {:?}", temp_random);

            if temp_random > SET_TEMPERATURE {
                control_lamp::control_lamp(false);
            } else {
                control_lamp::control_lamp(true);
            }

        } else {
            let sensor = ds18b20::DS18B20::new().unwrap();
            let temp = sensor.read_temp().unwrap();
            println!("Temperature: {:?}", temp);

            if temp.to_celsius() > SET_TEMPERATURE {
                control_lamp::control_lamp(false);
            } else {
                control_lamp::control_lamp(true);
            }
        }
    }
}
