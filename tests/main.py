# tests/main.py

import pytest
from unittest.mock import patch, MagicMock
from main import PneuRacer


@patch("main.inputs.devices")
@patch("main.pigpio.pi")
def test_pneuracer_init(mock_pigpio, mock_devices):
    # Mock a connected gamepad and pigpio
    mock_devices.gamepads = ["mock_gamepad"]
    mock_pi_instance = MagicMock()
    mock_pi_instance.connected = True
    mock_pigpio.return_value = mock_pi_instance

    # Create PneuRacer object
    racer = PneuRacer()

    # Assertions
    assert isinstance(racer.pi, MagicMock)
    assert racer.steerserv is not None
