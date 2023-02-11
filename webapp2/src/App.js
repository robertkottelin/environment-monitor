import React, { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import { Message , Client } from 'paho-mqtt';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    marginTop: theme.spacing(10),
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    marginTop: theme.spacing(3),
  },
  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    width: 200,
  },
  button: {
    marginTop: theme.spacing(2),
  },
}));

const App = () => {
  const classes = useStyles();
  const [temperature, setTemperature] = useState(0.0);
  const [thresholdInputValue, setThresholdInputValue] = useState('');  
  const MQTT_SERVER = '192.168.0.45';
  const MQTT_PORT = 8888;
  const MQTT_TEMPERATURE_TOPIC = 'temperature_channel';
  const MQTT_THRESHOLD_TOPIC = 'threshold_channel';

  useEffect(() => {
    const clientID = "clientID-" + parseInt(Math.random() * 100);
    const client = new Client(MQTT_SERVER, Number(MQTT_PORT), clientID);

    // client.onConnectionLost = (responseObject) => {
    //   console.log('Connection lost:', responseObject.errorMessage);
    // };

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

  const handleThresholdSubmit = (event) => {
    event.preventDefault();
  
    const clientID = "clientID-" + parseInt(Math.random() * 100);
    const client = new Client(MQTT_SERVER, Number(MQTT_PORT), clientID);
  
    client.connect({
      onSuccess: () => {
        console.log('Connected to MQTT broker');
        const message = new Message(thresholdInputValue);
        message.destinationName = MQTT_THRESHOLD_TOPIC;
        client.send(message);
        console.log("Message sent successfully.");
      },
      onFailure: (error) => {
        console.log('Failed to connect to MQTT broker', error);
      },
    });
  };
  
  
  return (
    <div className={classes.root}>
      <Typography variant="h4">Live temperature:</Typography>
      <Typography variant="h2">{temperature}°C</Typography>
  
      <form onSubmit={handleThresholdSubmit}>
        <input
          type="text"
          value={thresholdInputValue}
          onChange={(e) => setThresholdInputValue(e.target.value)}
        />
        <Button type="submit">Submit new temperature</Button>
      </form>
    </div>
  );
};

export default App;