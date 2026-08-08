"""
register.py

Descriptor classes exposing Modbus registers as normal Python attributes.

Example
-------
>>> class Controller(EurothermBase):
...     temperature = Register(PV)
...     target_setpoint = Register(TARGET_SP)

>>> controller.temperature
27.5

>>> controller.target_setpoint = 100.0
"""

from __future__ import annotations

import logging

from dataclasses import dataclass
from typing import Any, Callable

from .exceptions import ReadOnlyRegisterError

logger = logging.getLogger(__name__)


# =============================================================================
# Register definition
# =============================================================================


@dataclass(frozen=True, slots=True)
class RegisterDefinition:
    """
    Description of a Modbus register.

    This class contains only metadata.

    Parameters
    ----------
    address
        Modbus register address.

    decimals
        Number of decimal places used by the controller.

    signed
        Whether the register should be interpreted as signed.

    writable
        Whether the register can be written.

    units
        Engineering units.

    minimum
        Minimum allowed value.

    maximum
        Maximum allowed value.

    description
        Human-readable description.

    decoder
        Optional callable converting raw Modbus values into Python objects.

    encoder
        Optional callable converting Python objects into Modbus values.
    """

    
    address: int

    decimals: int = 0
    
    parameter: int | None = None

    signed: bool = False

    writable: bool = False

    units: str | None = None

    minimum: float | None = None

    maximum: float | None = None

    description: str = ""

    decoder: Callable[[Any], Any] | None = None

    encoder: Callable[[Any], Any] | None = None


# =============================================================================
# Register descriptor
# =============================================================================


class Register:
    """
    Descriptor implementing transparent Modbus register access.

    Reading::

        controller.temperature

    Writing::

        controller.target_setpoint = 150
    """

    def __init__(self, definition: RegisterDefinition):

        self.definition = definition

        self.name = ""

    def __set_name__(self, owner, name):

        self.name = name

    def __repr__(self):

        return (
            f"<Register "
            f"name='{self.name}' "
            f"address={self.definition.address}>"
        )

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    def _read(self, transport):

        value = transport.read_register(
            address=self.definition.address,
            decimals=self.definition.decimals,
            signed=self.definition.signed,
        )

        if self.definition.decoder is not None:
            value = self.definition.decoder(value)

        logger.debug(
            "Read %-20s reg=%4d value=%s%s",
            self.name,
            self.definition.address,
            value,
            f" {self.definition.units}"
            if self.definition.units
            else "",
        )

        return value

    def _write(self, transport, value):

        if not self.definition.writable:
            raise AttributeError(
                f"Register '{self.name}' is read-only."
            )

        if self.definition.encoder is not None:
            value = self.definition.encoder(value)

        if self.definition.minimum is not None:
            if value < self.definition.minimum:
                raise ValueError(
                    f"{self.name}: "
                    f"{value} < minimum ({self.definition.minimum})"
                )

        if self.definition.maximum is not None:
            if value > self.definition.maximum:
                raise ValueError(
                    f"{self.name}: "
                    f"{value} > maximum ({self.definition.maximum})"
                )

        logger.debug(
            "Write %-19s reg=%4d value=%s%s",
            self.name,
            self.definition.address,
            value,
            f" {self.definition.units}"
            if self.definition.units
            else "",
        )

        transport.write_register(
            address=self.definition.address,
            value=value,
            decimals=self.definition.decimals,
            signed=self.definition.signed,
        )

    # -------------------------------------------------------------------------
    # Descriptor interface
    # -------------------------------------------------------------------------

    def __get__(self, instance, owner):

        if instance is None:
            return self

        return self._read(instance.transport)

    def __set__(self, instance, value):

        self._write(instance.transport, value)