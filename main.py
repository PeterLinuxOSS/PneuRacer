import time
from inputs import get_gamepad
from servo import Servo
import pigpio
from cprint import cprint
from variables import SERVO_PIN, SERVO_FREQUENCY, VALVE_1_1, VALVE_1_2, VALVE_2_1, VALVE_2_2, map_range
from relays import relay_control
from multiprocessing import Process, Value
import ctypes

pi = pigpio.pi()  # Initialize pigpio instance
if not pi.connected:
    raise Exception("Could not connect to pigpiod. Is it running?")

def init_relays():
    pi.set_mode(VALVE_1_1, pigpio.OUTPUT)
    pi.set_mode(VALVE_1_2, pigpio.OUTPUT)
    pi.set_mode(VALVE_2_1, pigpio.OUTPUT)
    pi.set_mode(VALVE_2_2, pigpio.OUTPUT)
    pi.write(VALVE_1_1, 1)
    pi.write(VALVE_1_2, 1)
    pi.write(VALVE_2_1, 1)
    pi.write(VALVE_2_2, 1)
    time.sleep(2)  # Wait for the GPIO to be set up
    pi.write(VALVE_1_1, 0)
    pi.write(VALVE_1_2, 0)
    pi.write(VALVE_2_1, 0)
    pi.write(VALVE_2_2, 0)  
        
    
    

# Initialize the servo
myservo = Servo(SERVO_PIN, frequency=SERVO_FREQUENCY,pigp=pi)

# Shared variables for multiprocessing
relay1_delay = Value(ctypes.c_double, 5.0)  # Default delay in seconds






def main():
    """Main function to handle gamepad events and control the servo and relay."""
    init_relays()
    cprint.info("Relays initialized.")
    

    # Start relay control process
    relay_process = Process(target=relay_control, args=(pi, relay1_delay), daemon=True)
    relay_process.start()

    try:
        while True:
            events = get_gamepad()
            for event in events:
                if event.ev_type == "Absolute" and event.code == "ABS_X":
                    pos = map_range(float(event.state))  # Normalize state to [-1, 1]
                    cprint.info(f"{pos:.2f} / {event.state}")
                    myservo.write(pos)
                elif event.ev_type == "Absolute" and event.code == "ABS_GAS":  # R2 analog input
                    pressure = float(event.state)
                    print(f"Pressure: {pressure}")
                    with relay1_delay.get_lock():
                        if event.state == 0:
                            relay1_delay.value = 99
                        else:    
                            relay1_delay.value = map_range(pressure, to_min=0.6, to_max=0.2) # type: ignore
                    cprint.info(f"Relay 1 delay adjusted to {relay1_delay.value:.1f} seconds")

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        relay_process.terminate()  
        pi.stop()  

if __name__ == "__main__":
    main()