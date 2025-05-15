"""This module contains the relay control process for the pigpio library."""
import time
from multiprocessing.sharedctypes import Synchronized

import pigpio

from variables import VALVE_1_1, VALVE_1_2, VALVE_2_1, VALVE_2_2


def relay_control(pi:pigpio.pi, relay1_delay:Synchronized):
    """Process function to control relay 1."""
    while True:
        
        
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