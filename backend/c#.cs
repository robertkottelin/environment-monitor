using System;
using System.Threading;
using OWNet;

namespace DS18B20Example
{
    class Program
    {
        static void Main(string[] args)
        {
            // Create a new OWNet connection to the 1-Wire network
            OWNet.OWNetConnection connection = new OWNetConnection();

            // Search for all temperature sensors on the 1-Wire network
            OWNet.Device[] devices = connection.GetDevices(OWNet.DeviceType.Temperature);

            // Loop through the found devices
            foreach (OWNet.Device device in devices)
            {
                // Read the temperature from the DS18B20 sensor
                double temperature = connection.GetTemperature(device);
                Console.WriteLine("Temperature: " + temperature + "°C");
            }

            // Disconnect from the 1-Wire network
            connection.Dispose();
        }
    }
}