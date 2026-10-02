"""
Eurotherm 3500 Series Controller
"""

from __future__ import annotations

from ..base import EurothermBase
from ..register import Register
from ..enums import Mode

from ..registers.series2000 import (
    PV,
    TARGET_SP,
    WORKING_SP,
    OUTPUT_LEVEL,
    AUTO_MANUAL,
    MANUAL_OUTPUT,
    PROPORTIONAL_BAND,
    INTEGRAL_TIME,
    DERIVATIVE_TIME,
)


class Eurotherm3508(EurothermBase):

    """
    Eurotherm 3508 temperature controller.
    """

    def __init__(
        self,
        port,
        address=1,
        baudrate=19200,
        parity="N",
        timeout=1.0,
        keep_open=False,
    ):
        super().__init__(
            port=port,
            address=address,
            baudrate=baudrate,
            parity=parity,
            timeout=timeout,
            keep_open=keep_open,
        )
    

    PING_REGISTER = PV

    # ------------------------------------------------------------------
    # Process
    # ------------------------------------------------------------------

    temperature = Register(PV)

    output_level = Register(OUTPUT_LEVEL)

    # ------------------------------------------------------------------
    # Setpoints
    # ------------------------------------------------------------------

    target_setpoint = Register(TARGET_SP)

    working_setpoint = Register(WORKING_SP)

    # ------------------------------------------------------------------
    # Control
    # ------------------------------------------------------------------

    mode = Register(AUTO_MANUAL)

    manual_output = Register(MANUAL_OUTPUT)

    # ------------------------------------------------------------------
    # PID
    # ------------------------------------------------------------------

    proportional_band = Register(PROPORTIONAL_BAND)

    integral_time = Register(INTEGRAL_TIME)

    derivative_time = Register(DERIVATIVE_TIME)

    # ------------------------------------------------------------------
    # Convenience properties
    # ------------------------------------------------------------------

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"T={self.temperature:.1f} °C, "
            f"SP={self.target_setpoint:.1f} °C, "
            f"OUT={self.output_level:.1f} %)"
        )

    def snapshot(self):
        return self.read_all()

    def identify(self):
        return {
            "model": "Eurotherm 3508",
            "port": self.port,
            "address": self.address,
        }
