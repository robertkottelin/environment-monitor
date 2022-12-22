use gtk::prelude::*;
use std::fs;
use std::error::Error;

fn read_temperature() -> Result<f32, Box<dyn Error>> {
    let w1_slave = "/sys/bus/w1/devices/28-000006ca5bff/w1_slave";

    let contents = fs::read_to_string(w1_slave)?;

    let lines: Vec<&str> = contents.split('\n').collect();
    let data = lines[1].trim();
    let temp_str = &data[29..];
    let temp: f32 = temp_str.parse()?;

    Ok(temp / 1000.0)
}

fn insert_temperature(client: &mut Client, temperature: f32) -> Result<u64, Box<dyn Error>> {
    let sql = "INSERT INTO temperatures (timestamp, temperature) VALUES ($1, $2)";
    let params = &[&chrono::Local::now(), &temperature];
    Ok(client.execute(sql, params)?)
}

fn main() {
    // Connect to the database
    let mut client = Client::connect("host=localhost user=postgres password=mypassword", NoTls)?;

    // Read the temperature from the DS18B20 sensor
    let temperature = read_temperature()?;

    // Insert the temperature and timestamp into the database
    insert_temperature(&mut client, temperature)?;

    if gtk::init().is_err() {
        println!("Failed to initialize GTK.");
        return;
    }

    let window = gtk::Window::new(gtk::WindowType::Toplevel);
    window.set_title("Temperature Data");
    window.set_default_size(400, 300);

    let vbox = gtk::Box::new(gtk::Orientation::Vertical, 10);

    // Create a table to display the temperature data
    let table = gtk::Grid::new();
    table.set_border_width(10);
    table.set_row_spacing(10);
    table.set_column_spacing(10);

    // Add the table to the vertical box
    vbox.pack_start(&table, true, true, 0);

    // Add a label to the table
    let label = gtk::Label::new(None);
    label.set_markup("<b>Temperature (°C)</b>");
    table.attach(&label, 0, 0, 1, 1);

    // Add a text entry to the table to display the temperature
    let temperature_entry = gtk::Entry::new();
    temperature_entry.set_editable(false);
    temperature_entry.set_text(&format!("{}", read_temperature().unwrap()));
    table.attach(&temperature_entry, 1, 0, 1, 1);

    // Create a chart to display the temperature data
    let chart = gtk::DrawingArea::new();
    chart.set_size_request(400, 200);

    // Add the chart to the vertical box
    vbox.pack_start(&chart, true, true, 0);

    // Add the vertical box to the window
    window.add(&vbox);

    // Connect the delete event to the quit function
    window.connect_delete_event(|_, _| {
        gtk::main_quit();
        Inhibit(false)
    });

    // Show the window and start the GTK main loop
    window.show_all();
    gtk::main();
}
