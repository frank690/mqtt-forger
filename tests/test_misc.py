"""This module is used to test the functions in  forger.auxiliary.misc"""

import pytest

from forger.auxiliary.misc import count_up, get_new_id, get_unique_name


@pytest.mark.parametrize(
    "name,suffix,expected",
    [
        ("abc", "_", "abc_0"),
        ("abc_", "_", "abc__0"),
        ("abc_0", "_", "abc_1"),
        ("abc_123", "_", "abc_124"),
    ],
)
def test_count_up(name, suffix, expected):
    """
    Test the count_up function
    """
    assert expected == count_up(name=name, suffix=suffix)


@pytest.mark.parametrize(
    "name,names,expected",
    [
        ("abc", ["asdf", "xyz"], "abc"),
        ("abc", ["asdf", "xyz", "abc"], "abc_0"),
        ("abc", ["asdf", "xyz", "abc", "abc_0"], "abc_1"),
        ("abc", ["asdf", "xyz", "abc", "abc_0", "abc_1"], "abc_2"),
    ],
)
def test_get_unique_name(name, names, expected):
    """
    Test the get_unique_name function
    """
    assert expected == get_unique_name(name=name, names=names)


@pytest.mark.parametrize(
    "dictionary,expected",
    [
        ({}, 0),
        ({0: "value"}, 1),
        ({0: "value", 1: "value"}, 2),
        ({0: "value", 4: "value"}, 5),
    ],
)
def test_get_new_id(dictionary, expected):
    """
    Test the get_new_id function
    """
    assert expected == get_new_id(dictionary=dictionary)
