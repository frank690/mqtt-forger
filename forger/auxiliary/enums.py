"""
This modules holds all enums that are used in the code base.
"""

__all__ = [
    "ChannelTypes",
]

from enum import Enum


class ChannelTypes(Enum):
    SIN = ["sin", "sine", "sinus"]
    RANDOM = ["random", "rand", "rnd"]
    FIXED = ["fixed", "static", "constant", "const"]
    REPLAY = ["replay", "repeating", "custom"]
