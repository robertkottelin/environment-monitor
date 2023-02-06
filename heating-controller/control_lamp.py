import RPi.GPIO as GPIO

def control_lamp(state: str):
    """Controls a lamp.

    Args:
        state: The state to set the lamp to. Valid values are 'on' and 'off'.
    """
    # Set up the GPIO pin for the relay
    relay_pin = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_pin, GPIO.OUT)
    
    

    if state == 'on':
        # Turn the relay on
        GPIO.output(relay_pin, GPIO.HIGH)
    elif state == 'off':
        # Turn the relay off
        GPIO.output(relay_pin, GPIO.LOW)
    else:
        raise ValueError(f'Invalid state: {state}')