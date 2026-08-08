"""
exceptions.py

Exception hierarchy for the Eurotherm package.
"""

from __future__ import annotations


class EurothermError(Exception):
    """
    Base class for all Eurotherm exceptions.
    """

    pass


# =============================================================================
# Communication
# =============================================================================

class CommunicationError(EurothermError):
    """
    Communication with the controller failed.
    """

    pass


class TimeoutError(CommunicationError):
    """
    The controller did not respond before the timeout expired.
    """

    pass


class CRCError(CommunicationError):
    """
    A received Modbus frame has an invalid CRC.
    """

    pass


class InvalidResponseError(CommunicationError):
    """
    The controller returned an unexpected or malformed response.
    """

    pass


# =============================================================================
# Register access
# =============================================================================

class RegisterError(EurothermError):
    """
    Base class for register-related exceptions.
    """

    pass


class ReadOnlyRegisterError(RegisterError):
    """
    Attempt to write to a read-only register.
    """

    pass


class InvalidRegisterError(RegisterError):
    """
    Invalid or unsupported register.
    """

    pass


class InvalidValueError(RegisterError):
    """
    Invalid value supplied for a register.
    """

    pass


# =============================================================================
# Controller
# =============================================================================

class ControllerError(EurothermError):
    """
    Controller-specific error.
    """

    pass


class ConfigurationError(ControllerError):
    """
    Invalid controller configuration.
    """

    pass