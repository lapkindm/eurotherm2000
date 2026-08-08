"""
transport.py

Low-level Modbus transport for Eurotherm controllers.
"""

from __future__ import annotations

import logging

import minimalmodbus
import serial

from .exceptions import (
    CommunicationError,
    ConfigurationError,
    TimeoutError,
)

logger = logging.getLogger(__name__)


class ModbusTransport:
    """
    Thin wrapper around MinimalModbus.

    Parameters
    ----------
    port
        Serial port (e.g. '/dev/ttyUSB0').
    address
        Modbus slave address.
    baudrate
        Serial baud rate.
    parity
        "N", "E" or "O".
    timeout
        Serial timeout in seconds.
    close_after_each_call
        Close the serial port after every Modbus transaction.
    """

    def __init__(
        self,
        port: str,
        address: int,
        baudrate: int = 9600,
        parity: str = "N",
        timeout: float = 1.0,
        close_after_each_call: bool = True,
    ):

        self.instrument: minimalmodbus.Instrument = (
            minimalmodbus.Instrument(port, address)
        )

        self.instrument.mode = minimalmodbus.MODE_RTU

        self.instrument.serial.baudrate = baudrate
        self.instrument.serial.bytesize = 8
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout = timeout

        parity = parity.upper()

        if parity == "N":
            self.instrument.serial.parity = serial.PARITY_NONE

        elif parity == "E":
            self.instrument.serial.parity = serial.PARITY_EVEN

        elif parity == "O":
            self.instrument.serial.parity = serial.PARITY_ODD

        else:
            raise ConfigurationError(
                f"Unsupported parity '{parity}'. "
                "Use 'N', 'E' or 'O'."
            )

        self.instrument.close_port_after_each_call = (
            close_after_each_call
        )

        self.instrument.debug = False


    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self):
        self.instrument.serial.open()
    
    def close(self):
        self.instrument.serial.close()
    
    # ------------------------------------------------------------------
    # Internal helper
    # ------------------------------------------------------------------

    def _execute(self, operation, *args, **kwargs):
        """
        Execute a MinimalModbus operation and translate exceptions.
        """

        try:
            return operation(*args, **kwargs)

        except minimalmodbus.NoResponseError as exc:

            logger.error(
                "No response from controller on '%s'.",
                self.port,
            )

            raise TimeoutError(str(exc)) from exc

        except minimalmodbus.InvalidResponseError as exc:

            logger.exception("Invalid response received.")

            raise CommunicationError(str(exc)) from exc

        except minimalmodbus.SlaveReportedException as exc:

            logger.exception("Controller reported an exception.")

            raise CommunicationError(str(exc)) from exc

        except serial.SerialException as exc:

            logger.exception("Serial communication error.")

            raise CommunicationError(str(exc)) from exc

    # ------------------------------------------------------------------
    # Register access
    # ------------------------------------------------------------------

    def read_register(
        self,
        address: int,
        decimals: int = 0,
        signed: bool = False,
    ):

        return self._execute(
            self.instrument.read_register,
            address,
            number_of_decimals=decimals,
            signed=signed,
        )

    def write_register(
        self,
        address: int,
        value: int | float,
        decimals: int = 0,
        signed: bool = False,
    ):

        self._execute(
            self.instrument.write_register,
            address,
            value,
            number_of_decimals=decimals,
            signed=signed,
        )

    def read_registers(
        self,
        start: int,
        count: int,
    ):

        return self._execute(
            self.instrument.read_registers,
            start,
            count,
        )

    # ------------------------------------------------------------------
    # Bit access
    # ------------------------------------------------------------------

    def read_bit(self, address: int):

        return self._execute(
            self.instrument.read_bit,
            address,
        )

    def write_bit(
        self,
        address: int,
        value: bool,
    ):

        self._execute(
            self.instrument.write_bit,
            address,
            value,
        )

    # ------------------------------------------------------------------
    # 32-bit integers
    # ------------------------------------------------------------------

    def read_long(
        self,
        address: int,
        signed: bool = False,
    ):

        return self._execute(
            self.instrument.read_long,
            address,
            signed=signed,
        )

    def write_long(
        self,
        address: int,
        value: int,
        signed: bool = False,
    ):

        self._execute(
            self.instrument.write_long,
            address,
            value,
            signed=signed,
        )

    # ------------------------------------------------------------------
    # Floating-point values
    # ------------------------------------------------------------------

    def read_float(
        self,
        address: int,
    ):

        return self._execute(
            self.instrument.read_float,
            address,
        )

    def write_float(
        self,
        address: int,
        value: float,
    ):

        self._execute(
            self.instrument.write_float,
            address,
            value,
        )

    # ------------------------------------------------------------------
    # Resource management
    # ------------------------------------------------------------------

    def close(self):
        """
        Close the serial port.
        """

        if self.instrument.serial.is_open:
            self.instrument.serial.close()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def address(self) -> int:
        return self.instrument.address

    @property
    def port(self) -> str:
        return self.instrument.serial.port

    @property
    def debug(self) -> bool:
        return self.instrument.debug

    @debug.setter
    def debug(self, value: bool):
        self.instrument.debug = value

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self):

        return (
            f"{self.__class__.__name__}("
            f"port='{self.port}', "
            f"address={self.address})"
        )