"""This module is used to test the functions in  forger.engine.generator"""

from datetime import datetime

import numpy as np
import pytest

from forger.auxiliary.exceptions import InvalidInputTypeError, SeedReplantError
from forger.engine.generator import Generator

data = [5 * np.tanh(x) for x in np.linspace(-2, 2, 100)]


@pytest.fixture(
    params=[
        ("Foo", 1, "sin", 0, 0, None, None, None),
        ("Foo", 10.5, "rnd", 0, 0, None, None, None),
        ("Foo", 0.15, "fixed", 0, 0, None, None, None),
        ("Foo", 0.015, "replay", 0, 0, None, data, None),
        ("Bar", 1, "sin", 1, 1, None, None, None),
        ("Bar", 10.5, "rnd", 2, 0.5, None, None, None),
        ("Bar", 0.15, "fixed", 3, 0.2, None, None, None),
        ("Bar", 0.015, "replay", 4, 0.1, None, data, None),
        ("Baz", 1, "sin", 0, 0, [42, 1337], None, None),
        ("Baz", 10.5, "rnd", 0, 0, [-0.24, 0.99], None, None),
        ("Baz", 0.15, "fixed", 0, 0, [-8, -4], None, None),
        ("Baz", 0.015, "replay", 0, 0, [1, 2], data, None),
        ("Qux", 1, "sin", 1, 1, [0.1, 0.11], None, 2),
        ("Qux", 10.5, "rnd", 2, 0.5, [-10, 5], None, 3),
        ("Qux", 0.15, "fixed", 3, 0.2, [12.5, 14.81], None, 42),
        ("Qux", 0.015, "replay", 4, 0.1, None, data, 1337),
    ],
)
def generator(request):
    return Generator(
        name=request.param[0],
        frequency=request.param[1],
        channel_type=request.param[2],
        dead_frequency=request.param[3],
        dead_period=request.param[4],
        scale=request.param[5],
        replay_data=request.param[6],
        seed=request.param[7],
    )


class TestGenerator:
    @pytest.mark.parametrize(
        "seed",
        [
            None,
            42,
            -1337,
        ],
    )
    def test__plant_a_seed(self, generator, seed):
        """
        Test the _plant_a_seed method
        """
        if (generator.seed is None) and (seed is None):
            with pytest.raises(SeedReplantError):
                generator._plant_a_seed(seed=seed)
        else:
            generator._plant_a_seed(seed=seed)

    @pytest.mark.parametrize(
        "value,scale,limits,expected",
        [
            (0, [5, 10], [-1, 1.5], 7),
            (-1, [-42.5, 323.123], [-1, 1], -42.5),
            (0.5, [-10, 100], [-1, 1], 72.5),
            (-0.8, [-1000, -2000], [-1, 1], -1900),
            (0, [5, 10], [10, -30], 8.75),
            (-1, [-42.5, 323.123], [-1, 100], -42.5),
            (0.5, [-10, 100], [-1, 0], 155),
            (-0.8, [-1000, -2000], [0, 12.5], -2064),
        ],
    )
    def test__rescale(self, generator, value, scale, limits, expected):
        """
        Test the _rescale method
        """
        generator.scale = scale
        generator.limits = limits
        assert generator._rescale(value=value) == expected

    @pytest.mark.parametrize(
        "dt",
        [
            datetime.now(),
            None,
        ],
    )
    def test__seconds_since_init(self, generator, dt):
        """
        Test the _seconds_since_init method
        """
        seconds = generator._seconds_since_init(current_datetime=dt)
        assert isinstance(seconds, float)
        assert seconds > 0

    @pytest.mark.parametrize(
        "dt",
        [
            datetime.now(),
            None,
        ],
    )
    def test_get_data(self, generator, dt):
        """
        Test the get_data method
        """
        value = generator.get_data(current_datetime=dt)
        assert isinstance(value, float)
