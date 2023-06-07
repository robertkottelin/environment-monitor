use std::process::Command;
use std::fs::read_to_string;
use std::thread::sleep;
use std::time::Duration;

extern crate paho_mqtt as mqtt;

const DEVICE_FOLDER: &str = "/sys/bus/w1/devices/28-xxxxxxxxxxxx";  

fn read_temp_raw() -> Result<String, std::io::Error> {
    Command::new("modprobe")
        .args(&["w1-gpio", "w1-therm"])
        .output()
        .expect("Failed to load modules");
    let device_file = format!("{}/w1_slave", DEVICE_FOLDER);
    read_to_string(device_file)
}

fn read_temperature() -> Result<f64, std::io::Error> {
    loop {
        let lines = read_temp_raw()?;
        if lines.lines().next().unwrap().ends_with("YES") {
            let temp_line = lines.lines().nth(1).unwrap();
            let equals_pos = temp_line.find("t=").unwrap();
            let temp_string = &temp_line[(equals_pos+2)..];
            let temperature = temp_string.parse::<f64>().unwrap() / 1000.0;
            return Ok(temperature);
        } else {
            sleep(Duration::from_millis(200));
        }
    }
}

fn main() {
    let client = mqtt::Client::new("tcp://192.168.0.45:1883").unwrap();

    loop {
        let temperature = read_temperature().unwrap();
        println!("Sending temperature data to 192.168.0.45: {:?}", temperature);

        let msg = mqtt::MessageBuilder::new()
            .topic("temperature_channel")
            .payload(format!("{}", temperature))
            .qos(1)
            .finalize();

        if let Err(e) = client.publish(msg) {
            eprintln!("Error sending message: {:?}", e);
        }
        sleep(Duration::from_secs(5)); 
    }
}
