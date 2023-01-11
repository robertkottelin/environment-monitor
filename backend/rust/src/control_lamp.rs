extern crate rppal;

use rppal::gpio::{Gpio};

pub fn control_lamp(state: bool) -> Result<(), rppal::gpio::Error> {
    // Set up the GPIO pin connected to the relay module as an output pin
    let mut relay_pin = Gpio::new()?.get(17)?.into_output();

    if state {
        // Set the GPIO pin to high (on)
        relay_pin.set_high();
        println!("Lamp turned on");
    } else {
        // Set the GPIO pin to low (off)
        relay_pin.set_low();
        println!("Lamp turned off");
    }

    Ok(())
}
