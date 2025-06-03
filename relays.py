"""This module contains the relay control process for the pigpio library."""
import time
from multiprocessing.sharedctypes import Synchronized

import pigpio

from variables import VALVE_1_1, VALVE_1_2, VALVE_2_1, VALVE_2_2


def relay_control(pi: pigpio.pi, relay_delay: Synchronized):
    """Process function to control two pistons (VALVE_1 and VALVE_2) 90 degrees out of phase."""
    try:
        while True:
            
            while relay_delay.value == 99:
                time.sleep(0.1)
            # Start: Both pistons open (VALVE_X_1 True, VALVE_X_2 False)
            pi.write(VALVE_1_1, 1)
            pi.write(VALVE_1_2, 0)
            pi.write(VALVE_2_1, 1)
            pi.write(VALVE_2_2, 0)
            while relay_delay.value == 99:
                time.sleep(0.1)
            time.sleep(relay_delay.value)

            # Step 2: VALVE_1 closes, VALVE_2 stays open (90 degree phase difference)
            pi.write(VALVE_1_1, 0)
            pi.write(VALVE_1_2, 1)
            pi.write(VALVE_2_1, 1)
            pi.write(VALVE_2_2, 0)
            while relay_delay.value == 99:
                time.sleep(0.1)
            time.sleep(relay_delay.value)

            # Step 3: VALVE_1 stays closed, VALVE_2 closes
            pi.write(VALVE_1_1, 0)
            pi.write(VALVE_1_2, 1)
            pi.write(VALVE_2_1, 0)
            pi.write(VALVE_2_2, 1)
            while relay_delay.value == 99:
                time.sleep(0.1)
            time.sleep(relay_delay.value)

            # Step 4: VALVE_1 opens, VALVE_2 stays closed
            pi.write(VALVE_1_1, 1)
            pi.write(VALVE_1_2, 0)
            pi.write(VALVE_2_1, 0)
            pi.write(VALVE_2_2, 1)
            while relay_delay.value == 99:
                time.sleep(0.1)
            time.sleep(relay_delay.value)

            # Loop repeats
    except Exception as e:
        print(f"[relay_control] Error: {e}")
        raise