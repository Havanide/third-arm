"""
third_arm.adapters.hardware.power_monitor
─────────────────────────────────────────────────────────────────────────────
Arm power / battery monitor — STUB / PLACEHOLDER.

TODO (Stage 1.5):
  - Choose power monitoring IC / ADC
  - Read voltage + current
  - Expose as telemetry field
  - Trigger safe_stop on low-voltage fault
"""

from __future__ import annotations


class PowerMonitor:
    """Reads arm power supply voltage and current.

    TODO: implement for Stage 1.5.
    """

    def get_voltage_v(self) -> float:
        """TODO: return real supply voltage. Stub returns nominal 24 V."""
        return 24.0

    def get_current_a(self) -> float:
        """TODO: return real supply current. Stub returns 0."""
        return 0.0

    def is_healthy(self) -> bool:
        """TODO: return False if voltage is out of spec."""
        return True
