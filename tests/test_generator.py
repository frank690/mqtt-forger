"""This module is used to test the classes in forger.engine.generator"""

from datetime import datetime

import pytest

from forger.auxiliary.exceptions import InvalidInputTypeError, SeedReplantError
from forger.engine.generator import Generator
from tests.conftest import generator_samples


@pytest.fixture(
    params=generator_samples,
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
            datetime(
                year=2020,
                month=7,
                day=10,
                hour=12,
                minute=10,
                second=0,
                microsecond=123,
            ),
            datetime(
                year=2000,
                month=7,
                day=10,
                hour=12,
                minute=10,
                second=0,
                microsecond=123,
            ),
            datetime(
                year=2021,
                month=7,
                day=10,
                hour=12,
                minute=10,
                second=0,
                microsecond=123,
            ),
            None,
            datetime(
                year=2020,
                month=1,
                day=10,
                hour=12,
                minute=10,
                second=0,
                microsecond=123,
            ),
            datetime(
                year=2020,
                month=2,
                day=10,
                hour=12,
                minute=10,
                second=0,
                microsecond=123,
            ),
            datetime(
                year=2020,
                month=3,
                day=10,
                hour=12,
                minute=10,
                second=0,
                microsecond=123,
            ),
            datetime(
                year=2020, month=7, day=10, hour=1, minute=0, second=0, microsecond=0
            ),
            None,
            None,
        ],
    )
    def test_get_data(self, generator, dt):
        """
        Test the get_data method
        """
        if generator.channel_type == "wrong":
            with pytest.raises(InvalidInputTypeError):
                generator.get_data(current_datetime=dt)
        else:
            value = generator.get_data(current_datetime=dt)
            assert isinstance(value, float)
