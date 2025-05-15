from variables import VALVE_1_1, VALVE_1_2, VALVE_2_1, VALVE_2_2
from cprint import cprint
import time
import pigpio
from multiprocessing.sharedctypes import Synchronized

def relay_control(pi:pigpio.pi, relay1_delay:Synchronized[float]):
    """Process function to control relay 1."""
    while True:
        
        cprint.info("Activating VALVE_2_1 LOW and VALVE_2_2 HIGH")
        pi.write(VALVE_2_1, 0)
        pi.write(VALVE_2_2, 1)
        pi.write(VALVE_1_1, 1)
        pi.write(VALVE_1_2, 0)
        if relay1_delay.value == 99:
            continue
        time.sleep(relay1_delay.value)
        pi.write(VALVE_1_1, 0)
        pi.write(VALVE_1_2, 1)
        
        pi.write(VALVE_2_1, 1)
        pi.write(VALVE_2_2, 0)
        if relay1_delay.value == 99:
            continue
        time.sleep(relay1_delay.value)