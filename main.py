"""This module contains the main logic for src."""

import ctypes
import time
from multiprocessing import Process, Value

import pigpio
from cprint import cprint
from inputs import get_gamepad
import inputs

from relays import relay_control
from servo import Servo
from variables import (
    SERVO_FREQUENCY,
    SERVO_PIN,
    VALVE_1_1,
    VALVE_1_2,
    VALVE_2_1,
    VALVE_2_2,
    LONG_RANGE_DELAY,
    map_range,
)


class PneuRacer:
    """Main class for the PneuRacer project."""

    def wait_for_gamepad(self):
        """Wait until a gamepad is connected."""
        
        cprint.info("Waiting for gamepad connection...")
        
        while True:
            if len(inputs.devices.gamepads) > 0:
                cprint.info("Gamepad detected!")
                return
                
            else:
                cprint.warn(f"No gamepad detected")
                time.sleep(2)  # Wait before retrying

    def __init__(self):
        self.wait_for_gamepad()
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise ConnectionError("Could not connect to pigpiod. Is it running?")
        self.steerserv = Servo(SERVO_PIN, frequency=SERVO_FREQUENCY, pigp=self.pi)
        self.relay1_delay = Value(ctypes.c_double, 99)
        self.init_relays()
        self.relay_process = Process(target=relay_control, args=(self.pi, self.relay1_delay), daemon=True)

    def __del__(self):
        self.steerserv.stop()
        self.pi.stop()
        
    def init_relays(self):
        self.pi.set_mode(VALVE_1_1, pigpio.OUTPUT)
        self.pi.set_mode(VALVE_1_2, pigpio.OUTPUT)
        self.pi.set_mode(VALVE_2_1, pigpio.OUTPUT)
        self.pi.set_mode(VALVE_2_2, pigpio.OUTPUT)
        self.pi.write(VALVE_1_1, 0)
        self.pi.write(VALVE_1_2, 0)
        self.pi.write(VALVE_2_1, 0)
        self.pi.write(VALVE_2_2, 0)


    def main(self):
        """Main function to handle gamepad events and control the servo and relay."""
        
        cprint.info("Relays initialized.")
        self.relay_process.start()

        
        while True:
            events = get_gamepad()
            for event in events:
                if event.ev_type == "Absolute" and event.code == "ABS_X":
                    pos = map_range(float(event.state))
                    cprint.info(f"{pos:.2f} / {event.state}")
                    self.steerserv.write(pos)
                    
                elif event.ev_type == "Absolute" and event.code == "ABS_GAS":
                    print(f"ABS_GAS: {event.state}")
                    pressure = float(event.state)
                    
                    with self.relay1_delay.get_lock():
                        if event.state == 0:
                            self.relay1_delay.value = 99
                        else:
                            self.relay1_delay.value = map_range(
                                pressure, to_min=1, to_max=0.25 # type: ignore
                            )  
                    #cprint.info(
                    #    f"Relay 1 delay adjusted to {self.relay1_delay.value:.1f} seconds"
                    #)
                elif event.ev_type == "Key" and event.code == "BTN_START" and event.state == 1:
                    cprint.info("release air")
                    self.pi.write(VALVE_1_1, 0)
                    self.pi.write(VALVE_1_2, 0)
                    self.pi.write(VALVE_2_1, 0)
                    self.pi.write(VALVE_2_2, 0)
                    time.sleep(1)
                    self.pi.write(VALVE_1_1, 1)
                    self.pi.write(VALVE_1_2, 1)
                    self.pi.write(VALVE_2_1, 1)
                    self.pi.write(VALVE_2_2, 1)
                    time.sleep(1)
                    self.pi.write(VALVE_2_2, 0)
                    self.pi.write(VALVE_1_1, 0)
                    self.pi.write(VALVE_1_2, 0)
                    self.pi.write(VALVE_2_1, 0)
                    
                    
                    with self.relay1_delay.get_lock():
                        self.relay1_delay.value = 99
                        
                elif event.ev_type == "Key" and event.code == "BTN_WEST" : # Button 1
                     
                    if event.state == 1:
                        cprint.info("drag race mode activated")
                        i = 0.5
                        while i >= 0.2:
                            with self.relay1_delay.get_lock():
                                self.relay1_delay.value = i
                            time.sleep(0.5)
                            i -= 0.1
                        with self.relay1_delay.get_lock():
                            self.relay1_delay.value 
                    else:
                        with self.relay1_delay.get_lock():
                            self.relay1_delay.value = 99
                    
                elif event.ev_type == "Key" and event.code == "BTN_TR":   # Long range mode
                    if event.state == 1:
                        cprint.info("Long range mode activated")
                        with self.relay1_delay.get_lock():
                            self.relay1_delay.value = LONG_RANGE_DELAY
                    else:
                        with self.relay1_delay.get_lock():
                            self.relay1_delay.value = 99
                else:
                    cprint.warn(f"Unhandled event: {event.ev_type} {event.code} {event.state}")

if __name__ == "__main__":
    racer = PneuRacer()
    try:
        racer.main()
    except (KeyboardInterrupt, ConnectionError, OSError) as e:
        cprint.err(f"An error occurred: {e}")
        racer.relay_process.terminate()
        racer.pi.stop()