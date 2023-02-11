import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
 
# PIN connected to IN1
relay_pin = 23
 
# Set mode BCM
GPIO.setmode(GPIO.BCM)
 
#Type of PIN - output
GPIO.setup(relay_pin,GPIO.OUT)

 
MQTT_SERVER = "localhost"
MQTT_TEMPERATURE_TOPIC = "temperature_channel"
MQTT_THRESHOLD_TOPIC = "threshold_channel"

# Initialize the temperature and threshold temperature variables
temp = 0.0
threshold_temp = 25.0
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing to the temperature and threshold temperature topics
    client.subscribe(MQTT_TEMPERATURE_TOPIC)
    client.subscribe(MQTT_THRESHOLD_TOPIC)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global temp, threshold_temp
    if msg.topic == MQTT_TEMPERATURE_TOPIC:
        # Decode the received temperature payload and convert it to a float
        temp = float(msg.payload.decode())
        print(f"Temperature updated to: {temp}")
    elif msg.topic == MQTT_THRESHOLD_TOPIC:
        # Decode the received threshold temperature payload and convert it to a float
        threshold_temp = float(msg.payload.decode())
        print(f"Threshold temperature updated to: {threshold_temp}")
    
    if temp < threshold_temp:
        print ("Setting low - LAMP ON")
        GPIO.output (relay_pin,GPIO.LOW)
    else:
        print ("Setting high - LAMP OFF")
        GPIO.output (relay_pin, GPIO.HIGH)
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
