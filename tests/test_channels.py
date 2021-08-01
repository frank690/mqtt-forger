"""This module is used to test the classes in forger.engine.channels"""

import pytest

from forger.engine.channels import Channel, Channels
from forger.engine.generator import Generator
from tests.conftest import generator_samples


class TestChannel:
    @pytest.mark.parametrize(
        "name,frequency,channel_type,dead_frequency,dead_period,scale,replay_data,seed",
        generator_samples,
    )
    def test___init__(
        self,
        name,
        scale,
        frequency,
        channel_type,
        dead_frequency,
        dead_period,
        replay_data,
        seed,
    ):
        """
        Test the initialization method of the Channel class.
        """
        channel = Channel(
            name=name,
            scale=scale,
            frequency=frequency,
            channel_type=channel_type,
            dead_frequency=dead_frequency,
            dead_period=dead_period,
            replay_data=replay_data,
            seed=seed,
        )

        assert isinstance(channel, Channel)
        assert isinstance(channel.generator, Generator)


@pytest.fixture()
def channels():
    return Channels()


class TestChannels:
    @pytest.mark.parametrize(
        "name,frequency,channel_type,dead_frequency,dead_period,scale,replay_data,seed",
        generator_samples,
    )
    def test_add_and_remove(
        self,
        channels,
        name,
        scale,
        frequency,
        channel_type,
        dead_frequency,
        dead_period,
        replay_data,
        seed,
    ):
        """
        Test the add and remove methods of the Channels class.
        """
        assert isinstance(channels.channels, dict)

        c1 = channels.add(
            name=name,
            scale=scale,
            frequency=frequency,
            channel_type=channel_type,
            dead_frequency=dead_frequency,
            dead_period=dead_period,
            replay_data=replay_data,
            seed=seed,
        )

        assert isinstance(channels.channels[0], Channel)
        assert channels.channels[0] == c1
        assert len(channels.channels) == 1

        c2 = channels.add(
            name=name,
            scale=scale,
            frequency=frequency,
            channel_type=channel_type,
            dead_frequency=dead_frequency,
            dead_period=dead_period,
            replay_data=replay_data,
            seed=seed,
        )

        assert isinstance(channels.channels[1], Channel)
        assert channels.channels[1] == c2
        assert len(channels.channels) == 2

        channels.remove(channel_to_remove=c1)

        assert isinstance(channels.channels.get(0), type(None))
        assert len(channels.channels) == 1

    def test__get_unique_channels(self, channels):
        """
        Test the _get_unique_channels method of Channels class.
        """
        names = []
        for generator_sample in generator_samples:
            names.append(generator_sample[0])
            channels.add(
                name=generator_sample[0],
                frequency=generator_sample[1],
                channel_type=generator_sample[2],
                dead_frequency=generator_sample[3],
                dead_period=generator_sample[4],
                scale=generator_sample[5],
                replay_data=generator_sample[6],
                seed=generator_sample[7],
            )

        assert list(set(names)) == channels._get_unique_channels()
