"""This module holds all the custom Exception"""

__all__ = [
    "InvalidInputTypeError",
    "InvalidInputValueError",
    "SeedReplantError",
    "OnConnectError",
]


class InvalidInputTypeError(Exception):
    """The InvalidInputTypeError is raised whenever an instance of the
    Generator class is initialized with unexpected types of certain input variables."""

    pass


class InvalidInputValueError(Exception):
    """The InvalidInputValueError is raised whenever an instance of the
    Generator class is initialized with invalid values of certain input variables."""

    pass


class SeedReplantError(Exception):
    """The SeedReplantError is raised whenever a replant of a
    seed is being tried but no seed has ever been planted before."""

    pass


class OnConnectError(Exception):
    """The OnConnectError is raised whenever the connection to a target system failed."""

    pass
