"""This module contains all Channel classes that are used by the manager class."""

__all__ = [
    "Channels",
    "Channel",
]

import json
from datetime import datetime
from typing import List, Optional, Union

from forger.auxiliary.misc import get_new_id
from forger.engine.generator import Generator


class Channel:
    """
    Channel class that is created by Channels class.
    """

    def __init__(
        self,
        name: str,
        scale: List[Union[float, int]],
        frequency: float,
        channel_type: str,
        dead_frequency: float,
        dead_period: float,
        replay_data: List,
    ):
        """
        Initialize variables
        """
        self.name = name
        self.scale = scale
        self.frequency = frequency
        self.channel_type = channel_type
        self.dead_frequency = dead_frequency
        self.dead_period = dead_period
        self.replay_data = replay_data

        self.generator = Generator(
            name=name,
            scale=scale,
            frequency=frequency,
            channel_type=channel_type,
            dead_frequency=dead_frequency,
            dead_period=dead_period,
            replay_data=replay_data,
        )


class Channels:
    """
    Channels class that creates and keeps track of each Channel class.
    """

    def __init__(self):
        """
        Initialize variables
        """
        self.channels = {}

    def add(
        self,
        name: str,
        scale: Optional[List],
        frequency: float,
        channel_type: str,
        dead_frequency: float,
        dead_period: float,
        replay_data: Optional[List],
    ) -> Channel:
        """
        Add new channel to dict of channels.

        :param name: Name of the new channel.
        :param scale: The lower/upper scale that the data should be rescaled to.
        :param frequency: Frequency (in Hertz) in that the data will repeat itself.
        :param channel_type: Type of channel (e.g. sin, cos, ...).
        :param dead_frequency: Frequency in that the dead period will be applied again.
        :param dead_period: Time in seconds that the channel will not produce any data.
        :param replay_data: List of data points that will be replayed.
        :return: Instance of Channel class that has just been added.
        """
        cid = get_new_id(self.channels)

        self.channels[cid] = Channel(
            name=name,
            scale=scale,
            frequency=frequency,
            channel_type=channel_type,
            dead_frequency=dead_frequency,
            dead_period=dead_period,
            replay_data=replay_data,
        )

        return self.channels[cid]

    def remove(self, channel_to_remove: Channel):
        """
        Removes a given Channel instance from the dict of channels.

        :param channel_to_remove: Channel instance to remove.
        """
        for cid in list(self.channels):
            if self.channels[cid] is channel_to_remove:
                self.channels.pop(cid)

    def _get_overall_output(self, name: str, time: Optional[datetime] = None):
        """
        Get the combined output of all generators.

        :param name: Name of channel that the data should be extracted from.
        :param time: Timestamp that the data should be extracted from.
        """
        if not time:
            time = datetime.now()

        return sum(
            [
                channel.generator.get_data(current_datetime=time)
                for cid, channel in self.channels.items()
                if channel.name == name
            ]
        )

    def _get_unique_channels(self):
        """
        Extract the unique channel names since multiple generators can output on the same channel (name).
        """
        return list(set([channel.name for key, channel in self.channels.items()]))

    def get_payload(self) -> str:
        """
        Gather the data of all generators and pack it into a nice json.
        :return: current payload.
        """
        # get current time.
        time = datetime.now()
        # create payload template
        data = {"timestamp": time.isoformat()}
        # get all channels
        channels = self._get_unique_channels()
        # loop over each unique channel and gather data.
        for channel in channels:
            data[channel] = self._get_overall_output(channel, time)
        return json.dumps(data)
