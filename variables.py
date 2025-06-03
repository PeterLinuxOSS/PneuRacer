"""This module contains the variables for pneuracer."""
VALVE_2_1 = 14
VALVE_2_2 = 15
VALVE_1_2 = 8
VALVE_1_1 = 23
SERVO_PIN = 18
SERVO_FREQUENCY = 333

LONG_RANGE_DELAY = 0.4 # def 0.4 

DRAG_START = 0.6 # def 0.6
DRAG_MAX = 0.2 # def 0.2
DRAG_STEP = 0.05 # def 0.05
DRAG_STEP_DELAY = 0.1 # def 0.1

BASIC_MIN = 1 # def 1
BASIC_MAX = 0.25 # def 0.25


def map_range(unscaled, from_min=0, from_max=255, to_min=0, to_max=180):
    """Map a value from one range to another."""
    return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min