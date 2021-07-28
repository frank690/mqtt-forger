"""This module contains all Channel classes that are used by the manager class."""

__all__ = [
    "Channels",
    "Channel",
]

from transmitter.auxiliary.constants import DEFAULT_PIPELINE_SETTINGS
from typing import List, Optional

defaults = DEFAULT_PIPELINE_SETTINGS


class Channel:
    """
    Channel class that is created by Channels class.
    """
    def __init__(self, name: str, limits: List = defaults["channel_limits"],
                 frequency: float = defaults["channel_frequency"], channel_type: str = defaults["channel_type"],
                 dead_frequency: float = defaults["dead_frequency"], dead_period: float = defaults["dead_period"],
                 replay_data: List = defaults["replay_data"]):
        """
        Initialize variables
        """
        self.name = name
        self.limits = limits
        self.frequency = frequency
        self.channel_type = channel_type
        self.dead_frequency = dead_frequency
        self.dead_period = dead_period
        self.replay_data = replay_data


class Channels:
    """
    Channels class that creates and keeps track of each Channel class.
    """
    def __init__(self):
        """
        Initialize variables
        """
        self.channels = {}

    def add(self, name: str, limits: List, frequency: float, channel_type: str,
            dead_frequency: float, dead_period: float, replay_data: Optional[List] = None) -> Channel:
        """
        Add new channel to dict of channels.

        :param name: (mandatory, string) Name of the new channel.
        :param limits: (optional, list of floats) The lower/upper limits of the data.
        :param frequency: (optional, float) Frequency (in Hertz) in that the data will repeat itself.
        :param channel_type: (optional, str) Type of channel (e.g. sin, cos, ...).
        :param dead_frequency: (optional, float) Frequency in that the dead period will be applied again.
        :param dead_period: (optional, float) Time in seconds that the channel will not produce any data.
        :param replay_data: (optional, List) List of datapoints that will be replayed.
        :return: Instance of Channel class that has just been added.
        """
        cid = 0 if len(self.channels.keys()) == 0 else max(self.channels.keys()) + 1

        self.channels[cid] = Channel(
            name=name,
            limits=limits,
            frequency=frequency,
            channel_type=channel_type,
            dead_frequency=dead_frequency,
            dead_period=dead_period,
            replay_data=replay_data
        )

        return self.channels[cid]

    def remove(self, cid: int):
        """
        Remove channel with given channel id (cid).

        :param cid: (mandatory, int) ID of channel to remove.
        """
        self.channels.pop(cid)
