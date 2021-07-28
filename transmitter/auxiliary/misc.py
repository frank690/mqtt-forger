"""
This module contains a collection of functions that are commonly used in the mqtt-forger code base
"""

__all__ = [
    "get_unique_name",
    "count_up",
]

from typing import List
from re import search as research


def get_unique_name(names: List[str], name: str) -> str:
    """
    Find a new name for name_ so that it is unique in the list of names_.

    :param names: (mandatory, list of strings) List of names that are already in use.
    :param name: (mandatory, string) Name that should be unique to names.
    :return: unique name
    """
    while name in names:
        name = count_up(name)
    return name


def count_up(name: str, suffix: str = "_") -> str:
    """
    Search for pattern in name_. Add that pattern if not found or add +1 to existing pattern.

    :param name: (mandatory, string) Name that should be unique to names.
    :param suffix: (optional, string) Will be attached to very end of name.
    :return: modified name
    """
    # search for suffix and numbers at the very end of name.
    search = research(r"[" + suffix + r"]([0-9]+)$", name)
    # found something?
    if search:
        # what number was found?
        num = int(search.group(0)[1:])
        # add +1 to that number.
        return name[:-len(search.group(0))] + suffix + str(num + 1)
    return name + suffix + "0"
