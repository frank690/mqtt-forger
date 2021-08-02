"""This module is used to test the classes in forger.engine.channels"""

import json
from datetime import datetime

import pytest

from forger.engine.channels import Channel, Channels
from forger.engine.generator import Generator
from tests.conftest import (
    generator_samples,
    generator_samples_names,
    valid_generator_samples,
    valid_generator_samples_names,
)


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


@pytest.fixture()
def valid_channels(channels):
    for generator_sample in valid_generator_samples:
        channels.add(
            name=generator_sample[0],
            frequency=generator_sample[1],
            channel_type=generator_sample[2],
            dead_frequency=generator_sample[3],
            dead_period=generator_sample[4],
            scale=generator_sample[5],
            replay_data=generator_sample[6],
            seed=42,
        )
    return channels


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

        assert set(generator_samples_names) == set(channels._get_unique_channels())

    @pytest.mark.parametrize(
        "name,dt",
        [
            ("Foo", None),
            ("Foo", datetime.now()),
            ("Bar", None),
            (
                "Bar",
                datetime(
                    year=2003,
                    month=11,
                    day=4,
                    hour=8,
                    minute=44,
                    second=1,
                    microsecond=432,
                ),
            ),
        ],
    )
    def test__get_overall_output(self, valid_channels, name, dt):
        """
        Test the _get_overall_output method of Channels class.
        """
        foo_output = valid_channels._get_overall_output(name=name, time=dt)
        assert isinstance(foo_output, float)

    def test_get_payload(self, valid_channels):
        """
        Test the get_payload method of Channels class.
        """
        payload = valid_channels.get_payload()
        payload_dict = json.loads(payload)

        assert isinstance(payload, str)
        for valid_generator_samples_name in valid_generator_samples_names:
            assert valid_generator_samples_name in payload_dict
