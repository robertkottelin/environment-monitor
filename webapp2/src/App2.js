import React, { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import { Client } from 'paho-mqtt';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    marginTop: theme.spacing(10),
  },
}));

const App = () => {
  const classes = useStyles();
  const [temperature, setTemperature] = useState(0.0);
  const MQTT_SERVER = '192.168.0.45';
  const MQTT_PORT = 8888;
  const MQTT_TEMPERATURE_TOPIC = 'temperature_channel';

  useEffect(() => {
    const clientID = "clientID-" + parseInt(Math.random() * 100);
    const client = new Client(MQTT_SERVER, Number(MQTT_PORT), clientID);

    client.onConnectionLost = (responseObject) => {
      console.log('Connection lost:', responseObject.errorMessage);
    };

    client.onMessageArrived = (message) => {
      if (message.destinationName === MQTT_TEMPERATURE_TOPIC) {
        setTemperature(parseFloat(message.payloadString));
      }
    };

    client.connect({
      onSuccess: () => {
        console.log('Connected to MQTT broker');
        client.subscribe(MQTT_TEMPERATURE_TOPIC);
      },
      onFailure: (error) => {
        console.log('Failed to connect to MQTT broker', error);
      },
    });

    return () => {
      client.disconnect();
    };
  }, []);

  return (
    <div className={classes.root}>
      <Typography variant="h4">Temperature:</Typography>
      <Typography variant="h2">{temperature}°C</Typography>
    </div>
  );
};

export default App;
