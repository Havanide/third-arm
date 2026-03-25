"""
third_arm.adapters.hardware.gpio_trigger
─────────────────────────────────────────────────────────────────────────────
GPIO-based operator trigger — STUB / PLACEHOLDER.

Stage 1 uses REST-only operator commands.
This adapter is intended for Stage 1.5 physical button / pedal trigger.

TODO (Stage 1.5):
  - Choose GPIO library (RPi.GPIO / gpiozero / libgpiod)
  - Map to correct pin number
  - Add debounce logic
  - Register callback with the state machine
"""

from __future__ import annotations


class GpioTrigger:
    """Physical operator trigger via GPIO.

    TODO: implement this class for Stage 1.5.
    """

    def __init__(self, pin: int) -> None:
        self._pin = pin
        raise NotImplementedError("GpioTrigger not implemented — operator uses REST in Stage 1")

    def start_listening(self, callback) -> None:  # noqa: ANN001
        """TODO: start GPIO interrupt listener; call *callback* on trigger press."""
        raise NotImplementedError

    def stop_listening(self) -> None:
        """TODO: unregister GPIO interrupt."""
        raise NotImplementedError
