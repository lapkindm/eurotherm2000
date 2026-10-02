"""
base.py

Base class for Eurotherm Modbus controllers.
"""

from __future__ import annotations

import logging

from abc import ABC

from .transport import ModbusTransport
from .register import Register

logger = logging.getLogger(__name__)


class EurothermBase(ABC):
    """
    Base class for Eurotherm Modbus controllers.
    """

    #: RegisterDefinition used by ping()
    PING_REGISTER = None

    def __init__(
        self,
        port: str,
        address: int = 1,
        baudrate: int = 9600,
        parity: str = "N",
        timeout: float = 1.0,
        keep_open: bool = False,
    ):

        self.keep_open = keep_open

        self.transport = ModbusTransport(
            port=port,
            address=address,
            baudrate=baudrate,
            parity=parity,
            timeout=timeout,
            close_after_each_call=not keep_open,
        )

    # ------------------------------------------------------------------
    # Connection information
    # ------------------------------------------------------------------

    @property
    def port(self) -> str:
        return self.transport.port

    @property
    def address(self) -> int:
        return self.transport.address

    @property
    def debug(self) -> bool:
        return self.transport.debug

    @debug.setter
    def debug(self, value: bool):
        self.transport.debug = value

    # ------------------------------------------------------------------
    # Low-level register access
    # ------------------------------------------------------------------

    def read_register(
        self,
        address: int,
        decimals: int = 0,
        signed: bool = False,
    ):
        """
        Read an arbitrary Modbus register.
        """
        return self.transport.read_register(
            address=address,
            decimals=decimals,
            signed=signed,
        )

    def write_register(
        self,
        address: int,
        value,
        decimals: int = 0,
        signed: bool = False,
    ):
        """
        Write an arbitrary Modbus register.
        """
        self.transport.write_register(
            address=address,
            value=value,
            decimals=decimals,
            signed=signed,
        )

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def ping(self) -> bool:
        """
        Check whether the controller responds.
        """

        if self.PING_REGISTER is None:
            raise NotImplementedError(
                "PING_REGISTER not defined."
            )

        try:
            self.read_register(
                address=self.PING_REGISTER.address,
                decimals=self.PING_REGISTER.decimals,
                signed=self.PING_REGISTER.signed,
            )
            return True

        except Exception:
            logger.exception("Ping failed.")
            return False

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    @classmethod
    def registers(cls) -> list[str]:
        """
        Return all register properties defined by the controller.
        """

        names = []

        for name, obj in vars(cls).items():

            if isinstance(obj, Register):
                names.append(name)

        return sorted(names)

    def read_all(self) -> dict[str, object]:
        """
        Read all exposed registers.

        Returns
        -------
        dict
            Mapping of register name to value.
        """

        values = {}

        for name in self.registers():
            values[name] = getattr(self, name)

        return values

    def describe(self, name: str):
        """
        Return the RegisterDefinition for a register.

        Example
        -------
        >>> controller.describe("temperature")
        """

        descriptor = getattr(type(self), name)

        if not isinstance(descriptor, Register):
            raise AttributeError(
                f"'{name}' is not a register."
            )

        return descriptor.definition

    # ------------------------------------------------------------------
    # Resource management
    # ------------------------------------------------------------------

    def open(self):
        """
        Open the serial port and keep it open until close() is called.
        """

        self.transport.close_after_each_call = False
        self.transport.open()

    def close(self):
        """
        Close the serial port.

        Unless the controller was created with ``keep_open=True``, the
        port is again opened and closed for each Modbus transaction.
        """

        self.transport.close()
        self.transport.close_after_each_call = not self.keep_open

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self):

        return (
            f"{self.__class__.__name__}("
            f"port='{self.port}', "
            f"address={self.address})"
        )