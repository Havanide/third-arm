"""
third_arm.adapters.hardware.arm_driver
─────────────────────────────────────────────────────────────────────────────
Real arm hardware driver — STUB / PLACEHOLDER.

Implement this class in Stage 1.5 when physical hardware is connected.
It must satisfy the ArmDriverABC contract.

TODO (Stage 1.5):
  - Determine communication protocol (serial / CAN / Ethernet)
  - Implement joint command serialisation
  - Implement position feedback parsing
  - Add watchdog / heartbeat to detect loss of communication
  - Wire to e-stop GPIO (see estop.py)
"""

from __future__ import annotations

from third_arm.domain.contracts import ArmDriverABC


class HardwareArmDriver(ArmDriverABC):
    """Real hardware arm driver.

    Args:
        port: Serial port or network address (e.g. '/dev/ttyUSB0').

    TODO: implement all methods below.
    """

    def __init__(self, port: str) -> None:
        self._port = port
        # TODO: open serial/CAN connection here
        raise NotImplementedError("HardwareArmDriver not implemented — use MockArmDriver")

    async def home(self) -> None:
        """TODO: send HOME command and await position confirmation."""
        raise NotImplementedError

    async def start_handover(self, slot_id: str, object_id: str) -> None:
        """TODO: execute pick-and-present sequence using slot coordinates."""
        raise NotImplementedError

    async def safe_stop(self) -> None:
        """TODO: send SAFE_STOP command — must be interrupt-safe."""
        raise NotImplementedError

    async def get_telemetry(self) -> dict:
        """TODO: read joint angles, EE position, gripper state from hardware."""
        raise NotImplementedError
