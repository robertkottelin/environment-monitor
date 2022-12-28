mod ds18b20;
mod w1_errors;
use rand::{thread_rng, Rng};
use std::thread;

fn random_int() -> i32 {
    let mut rng = thread_rng();

    rng.gen_range(20..26)
}

static USE_RANDOM_DATA: bool = true;
static RUN_PROGRAM: bool = true;

fn main() {
    while RUN_PROGRAM == true {
        let temp_random: f32;
        if USE_RANDOM_DATA {
            temp_random = random_int() as f32;
            println!("Temperature: {:?}", temp_random)
        } else {
            let sensor = ds18b20::DS18B20::new().unwrap();
            let temp = sensor.read_temp().unwrap();
            println!("Temperature: {:?}", temp)
        }
    }
}
