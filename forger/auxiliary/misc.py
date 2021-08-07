"""
This module contains a collection of functions that are commonly used in the mqtt-forger code base
"""

__all__ = [
    "get_unique_name",
    "count_up",
    "get_new_id",
    "datestr2num",
]

from datetime import datetime
from re import search as research
from typing import List

import matplotlib.dates as mdates

from forger.auxiliary.constants import DATE_FORMAT


def get_unique_name(names: List[str], name: str) -> str:
    """
    Find a new name for name so that it is unique in the list of names.

    :param names: (mandatory, list of strings) List of names that are already in use.
    :param name: Name that should be unique to names.
    :return: unique name
    """
    while name in names:
        name = count_up(name)
    return name


def count_up(name: str, suffix: str = "_") -> str:
    """
    Search for pattern in name. Add that pattern if not found or add +1 to existing pattern.

    :param name: Name that should be unique to names.
    :param suffix: Will be attached to very end of name.
    :return: modified name
    """
    # search for suffix and numbers at the very end of name.
    search = research(r"[" + suffix + r"]([0-9]+)$", name)
    # found something?
    if search:
        # what number was found?
        num = int(search.group(0)[1:])
        # add +1 to that number.
        return name[: -len(search.group(0))] + suffix + str(num + 1)
    return name + suffix + "0"


def get_new_id(dictionary: dict) -> int:
    """
    Get a new key id.
    It is assumed that the given dictionary only has integers as keys.
    This task sounds rather trivial but if certain keys can be removed from a dictionary,
    you may want to be sure that you are not overwriting existing ones while figuring out a new key id.
    :param dictionary: current dictionary to determine new key for.
    :return: New key that can be used without the hazard of overwriting an existing key.
    """
    return 0 if len(dictionary.keys()) == 0 else max(dictionary.keys()) + 1


def datestr2num(date_string: str) -> int:
    """
    Convert given datestring to numeric value.
    :param date_string: String in date format
    :return Date as numeric value
    """
    return mdates.date2num(datetime.strptime(date_string, DATE_FORMAT))
