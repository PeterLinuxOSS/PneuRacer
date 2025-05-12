import threading
import time
from inputs import get_gamepad
from piservo import Servo
from cprint import cprint
import RPi.GPIO as GPIO
from variables import SERVO_PIN, SERVO_FREQUENCY,VALVE_1_1, VALVE_1_2, VALVE_2_1, VALVE_2_2

def init_relays():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(VALVE_1_1, GPIO.OUT)  
    GPIO.setup(VALVE_1_2, GPIO.OUT)  
    GPIO.setup(VALVE_2_1, GPIO.OUT)  
    GPIO.setup(VALVE_2_2, GPIO.OUT)  
    
    GPIO.output(VALVE_1_1, GPIO.LOW) 
    GPIO.output(VALVE_1_2, GPIO.LOW)
    GPIO.output(VALVE_2_1, GPIO.LOW)
    GPIO.output(VALVE_2_2, GPIO.LOW)  


# Initialize the servo
myservo = Servo(SERVO_PIN, frequency=SERVO_FREQUENCY)

relay1_delay = 0.5  # Default delay in seconds

def map_range(unscaled, from_min=-1.000030518509476, from_max=1, to_min=0, to_max=180):
    """Map a value from one range to another."""
    return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min

def relay_control():
    """Thread function to control relay 1."""
    global relay1_delay
    while True:
        GPIO.output(VALVE_2_1, GPIO.LOW)
        GPIO.output(VALVE_2_2, GPIO.HIGH)
        
        GPIO.output(VALVE_1_1, GPIO.HIGH) 
        GPIO.output(VALVE_1_2, GPIO.LOW)
        
        time.sleep(relay1_delay)
        
        GPIO.output(VALVE_2_1, GPIO.LOW)
        GPIO.output(VALVE_2_2, GPIO.HIGH)
        
        GPIO.output(VALVE_2_1, GPIO.HIGH)
        GPIO.output(VALVE_2_2, GPIO.LOW)
        
        time.sleep(relay1_delay)

def main():
    """Main function to handle gamepad events and control the servo and relay."""
    init_relays()
    relay_thread = threading.Thread(target=relay_control, daemon=True)
    relay_thread.start()

    global relay1_delay  # Declare relay1_delay as global to modify it within the function
    try:
        while True:
            events = get_gamepad()
            for event in events:
                if event.ev_type == "Absolute" and event.code == "ABS_X":
                    pos = map_range(float(event.state) / 32768.0)  # Normalize state to [-1, 1]
                    cprint.info(f"{pos:.2f} / {event.state}")
                    myservo.write(pos)
                elif event.ev_type == "Key" and event.code == "BTN_TR2":  # R2 button
                    if event.ev_type == "Absolute" and event.code == "ABS_RZ":  # R2 analog input
                        pressure = float(event.state) / 255.0  # Normalize pressure to [0, 1]
                        relay1_delay = 2.0 - (pressure * 1.9)  # Map pressure to delay range [0.1, 2.0]
                        cprint.info(f"Relay 1 delay adjusted to {relay1_delay:.1f} seconds")
                        
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()