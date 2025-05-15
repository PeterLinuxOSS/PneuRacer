"""This module contains the main logic for src."""

import ctypes
import time
from multiprocessing import Process, Value

import pigpio
from cprint import cprint
from inputs import get_gamepad

from relays import relay_control
from servo import Servo
from variables import (
    SERVO_FREQUENCY,
    SERVO_PIN,
    VALVE_1_1,
    VALVE_1_2,
    VALVE_2_1,
    VALVE_2_2,
    map_range,
)




class PneuRacer:
    """Main class for the PneuRacer project."""
    def __init__(self):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise ConnectionError("Could not connect to pigpiod. Is it running?")
        self.steerserv = Servo(SERVO_PIN, frequency=SERVO_FREQUENCY, pigp=self.pi)
        self.relay1_delay = Value(ctypes.c_double, 1.0)
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
        self.pi.write(VALVE_1_1, 1)
        self.pi.write(VALVE_1_2, 1)
        self.pi.write(VALVE_2_1, 1)
        self.pi.write(VALVE_2_2, 1)
        time.sleep(2)  # Wait for the GPIO to be set up
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
                    pressure = float(event.state)
                    print(f"Pressure: {pressure}")
                    with self.relay1_delay.get_lock():
                        if event.state == 0:
                            self.relay1_delay.value = 99
                        else:
                            self.relay1_delay.value = map_range(
                                pressure, to_min=0.6, to_max=0.2 # type: ignore
                            )  
                    cprint.info(
                        f"Relay 1 delay adjusted to {self.relay1_delay.value:.1f} seconds"
                    )

        



if __name__ == "__main__":
    racer = PneuRacer()
    try:
        racer.main()
    except (KeyboardInterrupt, ConnectionError, OSError) as e:
        cprint.err(f"An error occurred: {e}")
        racer.relay_process.terminate()
        racer.pi.stop()