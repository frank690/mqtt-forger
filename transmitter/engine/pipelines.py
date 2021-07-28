"""This module contains all Pipeline classes that are used by the manager class."""

__all__ = [
    "Pipelines",
    "Pipeline",
]

import apscheduler.schedulers.background

from transmitter.auxiliary.exceptions import InvalidInputValueError, InvalidInputTypeError
from transmitter.engine.channels import Channels, Channel
from transmitter.engine.connections import Connection
from transmitter.engine.handlers import Handler

from typing import List, Optional
from apscheduler.schedulers.background import BackgroundScheduler


class Pipeline:
    """
    Pipeline class that is created by Pipelines class.
    """
    def __init__(self, pid: int, ip: str, port: int, topic: str, frequency: float,
                 scheduler: apscheduler.schedulers.background.BackgroundScheduler, name: str = ''):
        """Adding a new entry in the pipeline dictionary.

        :param pid: (mandatory, int) ID of pipeline.
        :param ip: (mandatory, str) IP of host that will receive data.
        :param port: (mandatory, int) Port of host that will receive data.
        :param topic: (mandatory, str) Topic to publish data onto.
        :param frequency: (mandatory, float) Frequency in that data will be published.
        :param scheduler: (mandatory, BackgroundScheduler) Scheduler that times the data publishing.
        :param name: (optional, str) Name of the new pipeline.

        Note:
        - name can also be None or an empty string.
        """

        self.channels = Channels()
        self.connection = Connection(ip=ip, port=port)
        self.handler = Handler(topic=topic, frequency=frequency)
        self.name = name
        self.active = True
        self.job = scheduler.add_job(
            func=self.publish_data,
            trigger="interval",
            seconds=(1 / frequency),
            id=str(pid),
        )

    def add_channel(self, name: str, limits: List, frequency: float, channel_type: str,
                    dead_frequency: float, dead_period: float, replay_data: Optional[List] = None) -> Channel:
        """
        Call Channels class to create a new Channel class instance.

        :param name: (mandatory, string) Name of the new channel.
        :param limits: (optional, list of floats) The lower/upper limits of the data.
        :param frequency: (optional, float) Frequency (in Hertz) in that the data will repeat itself.
        :param channel_type: (optional, str) Type of channel (e.g. sin, cos, ...).
        :param dead_frequency: (optional, float) Frequency in that the dead period will be applied again.
        :param dead_period: (optional, float) Time in seconds that the channel will not produce any data.
        :param replay_data: (optional, List) List of datapoints that will be replayed.
        :return: Instance of Channel class that has just been added.
        """
        return self.channels.add(name=name, limits=limits, frequency=frequency, channel_type=channel_type,
                                 dead_frequency=dead_frequency, dead_period=dead_period, replay_data=replay_data)

    def remove_channel(self, cid: int):
        """
        Remove channel with given channel id (cid).

        :param cid: (mandatory, int) ID of channel to remove.
        """
        self.channels.remove(cid)

    def switch_state(self, state: Optional[bool] = None):
        """
        Switch state of current state.

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

    def publish_data(self):
        """
        Get data and publish it to target host.
        """
        self.handler.publish()


class Pipelines:
    """
    Pipelines class that creates and keeps track of each Pipeline class.
    """
    def __init__(self):
        """Initialize variables"""
        self.pipelines = {}

        self.Scheduler = BackgroundScheduler()
        self.Scheduler.start()

    def get_names(self) -> List[str]:
        """
        Get names of all pipelines that have already been added.
        :return: List of names (strings) of pipelines.
        """
        return [v["name"] for k, v in self.pipelines.items()]

    def switch_state(self, pid: int, state: Optional[bool] = None):
        """
        Switches the state of the pipeline with the given id (pid) to either active / inactive.

        :param pid: (mandatory, int) ID of pipeline.
        :param state: (optional, boolean) If state is given, set to given state (true -> active).
        """
        self.pipelines[pid].switch_state(state=state)

    def add(self, ip: str, port: int, topic: str, frequency: float, pipeline_name: str) -> Pipeline:
        """
        Create pipeline and start it afterwards.

        :param ip: (mandatory, string) IP of target host.
        :param port: (mandatory, int) Port of target host.
        :param topic: (mandatory, string) Name of topic that data should be published on.
        :param frequency: (mandatory, float) Frequency (in Hz) in that the data will be published on the given topic.
        :param pipeline_name: (optional, str) Optional name of pipeline.
        :return: New Pipeline class instance.
        """

        self._check_inputs(
            ip=ip,
            port=port,
            topic=topic,
            frequency=frequency,
            pipeline_name=pipeline_name,
        )

        pid = len(self.pipelines)

        self.pipelines[pid] = Pipeline(
            pid=pid,
            name=pipeline_name,
            ip=ip,
            port=port,
            topic=topic,
            frequency=frequency,
            scheduler=self.Scheduler,
        )

        return self.pipelines[pid]

    @staticmethod
    def _check_inputs(**kwargs):
        """
        Check all inputs that are used to create a pipeline

        :param kwargs: Given keyword arguments to check.
        """

        if "ip" in kwargs:
            if not isinstance(kwargs["ip"], str):
                raise InvalidInputTypeError(
                    "Content of ip is type %s but should be a of type string."
                    % type(kwargs["ip"])
                )

        if "port" in kwargs:
            if not isinstance(kwargs["port"], int):
                raise InvalidInputTypeError(
                    "Content of port is type %s but should be a of type int."
                    % type(kwargs["port"])
                )
            if (kwargs["port"] < 0) | (kwargs["port"] > 65535):
                raise InvalidInputValueError(
                    "Value of port (%s) is not in valid port range (0 - 65535)."
                    % str(kwargs["port"])
                )

        if "topic" in kwargs:
            if not isinstance(kwargs["topic"], str):
                raise InvalidInputTypeError(
                    "Content of topic is type %s but should be a of type string."
                    % type(kwargs["topic"])
                )

        if "frequency" in kwargs:
            if not isinstance(kwargs["frequency"], (int, float)):
                raise InvalidInputTypeError(
                    "Content of frequency is type %s but should be a of type int or float."
                    % type(kwargs["frequency"])
                )
            if kwargs["frequency"] <= 0:
                raise InvalidInputValueError(
                    "Value of frequency (%s [Hz]) is negative "
                    "or zero but should be positive." % str(kwargs["frequency"])
                )

        if "channel_name" in kwargs:
            if not isinstance(kwargs["channel_name"], str):
                raise InvalidInputTypeError(
                    "Content of channel_name is type %s but should be a of type string."
                    % type(kwargs["channel_name"])
                )

        if "channel_limits" in kwargs:
            if kwargs["channel_limits"]:
                if not isinstance(kwargs["channel_limits"], list):
                    raise InvalidInputTypeError(
                        "Content of channel_limits is type %s but should be a of type list."
                        % type(kwargs["channel_limits"])
                    )
                if not all(
                    isinstance(x, (int, float)) for x in kwargs["channel_limits"]
                ):
                    raise InvalidInputValueError(
                        "Not all values of channel_limits are of type int or float."
                    )

        if "channel_frequency" in kwargs:
            if not isinstance(kwargs["channel_frequency"], (int, float)):
                raise InvalidInputTypeError(
                    "Content of channel_frequency is type %s but should "
                    "be a of type int or float." % type(kwargs["channel_frequency"])
                )
            if kwargs["channel_frequency"] <= 0:
                raise InvalidInputValueError(
                    "Value of channel_frequency (%s [Hz]) is negative or zero but"
                    " should be positive." % str(kwargs["channel_frequency"])
                )

        if "channel_type" in kwargs:
            if not isinstance(kwargs["channel_type"], str):
                raise InvalidInputTypeError(
                    "Content of channel_type is type %s but should be a of type string."
                    % type(kwargs["channel_type"])
                )

        if "pipeline_name" in kwargs:
            if not isinstance(kwargs["pipeline_name"], str):
                raise InvalidInputTypeError(
                    "Content of pipeline_name is type %s but should be a of type string."
                    % type(kwargs["pipeline_name"])
                )

        if "dead_frequency" in kwargs:
            if not isinstance(kwargs["dead_frequency"], (int, float)):
                raise InvalidInputTypeError(
                    "Content of dead_frequency is type %s but should "
                    "be a of type int or float." % type(kwargs["dead_frequency"])
                )
            if kwargs["dead_frequency"] <= 0:
                raise InvalidInputValueError(
                    "Value of dead_frequency (%s [Hz]) is negative or "
                    "zero but should be positive." % str(kwargs["dead_frequency"])
                )

        if "dead_period" in kwargs:
            if not isinstance(kwargs["dead_period"], (int, float)):
                raise InvalidInputTypeError(
                    "Content of dead_period is type %s but "
                    "should be a of type int or float." % type(kwargs["dead_period"])
                )
            if kwargs["dead_period"] < 0:
                raise InvalidInputValueError(
                    "Value of dead_period (%s [Hz]) is "
                    "negative but should be zero or positive."
                    % str(kwargs["dead_period"])
                )

        if "replay_data" in kwargs:
            if not isinstance(kwargs["replay_data"], list):
                raise InvalidInputTypeError(
                    "Content of replay_data is "
                    "type %s but should be an list." % type(kwargs["replay_data"])
                )
