"""This module contains all Pipeline classes that are used by the manager class."""

__all__ = [
    "Pipeline",
]

from typing import List, Optional

import apscheduler.schedulers.background

from forger.auxiliary.constants import DEFAULT_PIPELINE_SETTINGS
from forger.engine.channels import Channel, Channels
from forger.engine.connections import Connection

defaults = DEFAULT_PIPELINE_SETTINGS


class Pipeline:
    """
    Pipeline class that is created by Pipelines class.
    """

    def __init__(
        self,
        pid: int,
        ip: str,
        port: int,
        topic: str,
        frequency: float,
        scheduler: apscheduler.schedulers.background.BackgroundScheduler,
        name: str = "",
    ):
        """Adding a new entry in the pipeline dictionary.

        :param pid: ID of pipeline.
        :param ip: (mandatory, str) IP of host that will receive data.
        :param port: Port of host that will receive data.
        :param topic: (mandatory, str) Topic to publish data onto.
        :param frequency: Frequency in that data will be published.
        :param scheduler: (mandatory, BackgroundScheduler) Scheduler that times the data publishing.
        :param name: Name of the new pipeline.

        Note:
        - name can also be None or an empty string.
        """

        self.channels = Channels()
        self.connection = Connection(ip=ip, port=port)

        self.topic = topic
        self.frequency = frequency
        self.name = name
        self.active = True
        self.job = scheduler.add_job(
            func=self.publish,
            trigger="interval",
            seconds=(1 / frequency),
            id=str(pid),
        )

    def add_channel(
        self,
        name: str,
        limits: Optional[List] = defaults["channel_limits"],
        frequency: Optional[float] = defaults["channel_frequency"],
        channel_type: Optional[str] = defaults["channel_type"],
        dead_frequency: Optional[float] = defaults["dead_frequency"],
        dead_period: Optional[float] = defaults["dead_period"],
        replay_data: Optional[List] = defaults["replay_data"],
    ) -> Channel:
        """
        Call Channels class to create a new Channel class instance.

        :param name: Name of the new channel.
        :param limits: (optional, list of floats) The lower/upper limits of the data.
        :param frequency: Frequency (in Hertz) in that the data will repeat itself.
        :param channel_type: Type of channel (e.g. sin, cos, ...).
        :param dead_frequency: Frequency in that the dead period will be applied again.
        :param dead_period: Time in seconds that the channel will not produce any data.
        :param replay_data: List of data points that will be replayed.
        :return: Instance of Channel class that has just been added.
        """
        channel = self.channels.add(
            name=name,
            limits=limits,
            frequency=frequency,
            channel_type=channel_type,
            dead_frequency=dead_frequency,
            dead_period=dead_period,
            replay_data=replay_data,
        )

        return channel

    def remove_channel(self, channel: Channel):
        """
        Removes a given Channel instance.

        :param channel: Instance of Channel class to remove.
        """
        self.channels.remove(channel_to_remove=channel)

    def remove_all_channels(self):
        """
        Removes all channels from this pipeline.
        """
        self.channels = Channels()

    def get_channels(self, name: str) -> List[Channel]:
        """
        Get all channels that broadcast on the same name.

        :param name: Name that one-to-n channel(s) broadcast their data to. This is NOT the topic.
        :return: List of Channel instances that broadcast on the same name.
        """
        return [
            channel
            for cid, channel in self.channels.channels.items()
            if channel.name == name
        ]

    def switch_state(self, state: Optional[bool] = None):
        """
        Turns the pipeline on or offline.
        By default a new pipeline is "on" and sends timestamps (in json format) right away.

        :param state: (optional, boolean) If state is given, set to given state (true -> active).
        """
        if state is not None:
            self.active = state
        else:
            self.active = not self.active

        if self.active:
            self.job.resume()
        else:
            self.job.pause()

    def publish(self):
        """
        Publish data via mqtt client of this handler on topic that was set upon init of this class.
        """
        self.connection.mqtt_client.publish(
            topic=self.topic, payload=self.channels.get_payload()
        )
