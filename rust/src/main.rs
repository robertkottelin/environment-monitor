use gtk::prelude::*;
use gtk::{Application, ApplicationWindow, Button, Label};

mod ds18b20;
mod w1_errors;

const APP_ID: &str = "org.gtk_rs.TemperatureMonitor";

fn main() {
    // Create a new application
    let app = Application::builder().application_id(APP_ID).build();

    // Connect to "activate" signal of `app`
    app.connect_activate(build_ui);

    // Run the application
    app.run();
}

fn build_ui(app: &Application) {
    // Create a label to display the temperature
    let label = Label::new(None);
    label.set_text("Temperature: N/A");

    // Create a button with label and margins
    let button = Button::builder()
        .label("Refresh temperature")
        .margin_top(12)
        .margin_bottom(12)
        .margin_start(12)
        .margin_end(12)
        .build();

    // Connect to "clicked" signal of `button`
    button.connect_clicked(move |_| {
        // Read the temperature from the sensor
        let sensor = ds18b20::DS18B20::new().unwrap();
        let temp = sensor.read_temp().unwrap();
    
        *label.set_text(&format!("Temperature: {}°C", temp.to_celsius()));
    });
    
    

    // Create a window
    let window = ApplicationWindow::builder()
        .application(app)
        .title("Temperature monitor")
        .child(&label)
        .child(&button)
        .build();

    // Present window
    window.present();
}
