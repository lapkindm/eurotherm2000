"""
registers/series2000.py

Register definitions for Eurotherm 2400 series controllers.

Currently implemented and verified on:

    * Eurotherm 2408
    * Issue 3 firmware

    * Eurotherm 3508
    * Issue 3.5 firmware

Only commonly used operating registers are included.
"""

from __future__ import annotations

from ..enums import Mode
from ..register import RegisterDefinition


# =============================================================================
# Process values
# =============================================================================

PV = RegisterDefinition(
    address=1,
    decimals=1,
    units="°C",
    description="Process value",
)

TARGET_SP = RegisterDefinition(
    address=2,
    decimals=1,
    writable=True,
    units="°C",
    description="Target setpoint",
)

OUTPUT_LEVEL = RegisterDefinition(
    address=3,
    decimals=1,
    units="%",
    description="Control output",
)

WORKING_SP = RegisterDefinition(
    address=5,
    decimals=1,
    units="°C",
    description="Working setpoint",
)


# =============================================================================
# Controller mode
# =============================================================================

AUTO_MANUAL = RegisterDefinition(
    address=273,
    writable=True,
    decoder=Mode,
    encoder=int,
    description="Automatic / Manual mode",
)


# =============================================================================
# Manual mode
# =============================================================================

MANUAL_OUTPUT = RegisterDefinition(
    address=276,
    decimals=1,
    writable=True,
    units="%",
    minimum=-100.0,
    maximum=100.0,
    description="Manual output level",
)


# =============================================================================
# PID parameters
# =============================================================================

PROPORTIONAL_BAND = RegisterDefinition(
    address=6,
    decimals=1,
    writable=True,
    units="°C",
    minimum=0.1,
    description="Proportional band",
)

INTEGRAL_TIME = RegisterDefinition(
    address=8,
    decimals=0,
    writable=True,
    units="s",
    minimum=0,
    description="Integral time",
)

DERIVATIVE_TIME = RegisterDefinition(
    address=9,
    decimals=0,
    writable=True,
    units="s",
    minimum=0,
    description="Derivative time",
)