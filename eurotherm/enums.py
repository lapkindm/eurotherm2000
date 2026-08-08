"""
enums.py

Enumerations used by the Eurotherm package.
"""

from __future__ import annotations

from enum import IntEnum


class Mode(IntEnum):
    """
    Controller operating mode.
    """

    AUTO = 0
    MANUAL = 1


class AlarmState(IntEnum):
    """
    Alarm output state.
    """

    OFF = 0
    ON = 1


class ProgramState(IntEnum):
    """
    Ramp/soak programmer state.

    Not all controllers support all states.
    """

    RESET = 0
    RUN = 1
    HOLD = 2
    COMPLETE = 3


class OutputMode(IntEnum):
    """
    Output operating mode.
    """

    OFF = 0
    HEAT = 1
    COOL = 2
    HEAT_COOL = 3