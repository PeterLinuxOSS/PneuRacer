"""This module contains the variables for pneuracer."""
VALVE_1_1 = 14
VALVE_1_2 = 15
VALVE_2_1 = 23
VALVE_2_2 = 24
SERVO_PIN = 18
SERVO_FREQUENCY = 333


def map_range(unscaled, from_min=0, from_max=255, to_min=0, to_max=180):
    """Map a value from one range to another."""
    return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min