# import own libs
from transmitter.engine.generator import Generator
from transmitter.engine.connections import Connections
from transmitter.engine.handlers import Handlers
from transmitter.engine.pipelines import Pipelines
from transmitter.engine.topics import Topics
from transmitter.engine.channels import Channels
from transmitter.auxiliary.constants import DEFAULT_PIPELINE_SETTINGS
from transmitter.auxiliary.exceptions import (
    InvalidInputTypeError,
    InvalidInputValueError,
)

# import native libs
from re import search as research
from typing import List

# import 3rd party libs
import paho.mqtt.client as mqtt

"""Use this module to manage the complete mqtt process and all the other engine parts."""


class Manager:
    """
    Class to connect to a given host and send data with a given frequency.
    """

    # set default values
    defaults = DEFAULT_PIPELINE_SETTINGS

    def __init__(self, verbose_=False):
        """Initialize variables"""
        # init dict for handlers, pipelines, connections, topics and channels
        self.handlers = Handlers()  # contains instances of Generator
        self.pipelines = Pipelines()  # contains ids of host, topic, ...
        self.connections = Connections()  # contains host information
        self.topics = Topics()  # contains topic information
        self.channels = Channels()  # contains channel information

        # init parameters
        self.verbose = verbose_

    def create_pipeline(
        self, ip: str, port: int, topic: str, frequency: float, pipeline_name: str = defaults["pipeline_name"]
    ):
        """
        Create pipeline and add each element to its dict. Start pipeline afterwards.

        :param ip: (mandatory, string) IP of target host.
        :param port: (mandatory, int) Port of target host.
        :param topic: (mandatory, string) Name of topic that data should be published on.
        :param frequency: (mandatory, float) Frequency (in Hz) in that the data will be published on the given topic.
        :param pipeline_name: (optional, str) Optional name of pipeline.
        """
        self._check_inputs(
            ip=ip,
            port=port,
            topic=topic,
            frequency=frequency,
            pipeline_name=pipeline_name,
        )

        host_id = self.connections.add_connection(ip=ip, port=port)
        topic_id = self.topics.add_topic(topic=topic, frequency=frequency)
        pipeline_id = self.pipelines.add_pipeline(name=pipeline_name, host_id=host_id, topic_id=topic_id)

        # init and assign generator for each new pipeline
        self.handlers.add_handler(pid=pipeline_id)
        # add new job in scheduler
        self.Scheduler.add_job(
            func=self.publish_data,
            trigger="interval",
            seconds=(1 / frequency),
            id=str(pipeline_id),
            kwargs={"pid_": pipeline_id},
        )
        # pause job since no channel is yet on pipeline
        self.Scheduler.get_job(str(pipeline_id)).pause()
        # return id of pipeline that has just been created
        return pipeline_id

    def add_function(self, pid, channel_name, limits, frequency, channel_type, dead_frequency, dead_period):
        """
        Add a function to an already existing pipeline.

        :param pid: (mandatory, int) ID of pipeline.
        :param channel_name: (mandatory, string) Name of channel.
        :param limits: (optional, list of floats) The lower/upper limits of the data.
        :param frequency: (optional, float) Frequency (in Hz) in that the data will repeat itself.
        :param channel_type: (optional, string) Defines kind of function that will be added (e.g. sine wave).
        :param dead_frequency: (optional, float) Frequency (in Hz) in that the function will return zero.
        :param dead_period: (optional, float) Duration in that the output will stay zero.
        """
        self._check_inputs(
            channel_name=channel_name,
            channel_limits=limits,
            channel_frequency=frequency,
            channel_type=channel_type,
            dead_frequency=dead_frequency,
            dead_period=dead_period,
        )

        cid = self.channels.add_channel(
            name=channel_name,
            limits=limits,
            frequency=frequency,
            channel_type=channel_type,
            dead_frequency=dead_frequency,
            dead_period=dead_period
        )

        # add channel to target pipeline
        self.pipelines[pid]["channel_id"].append(cid)
        # is pipeline currently inactive?
        if self.pipelines[pid]["active"] == 0:
            # switch pipeline on
            self.switch_pipeline(pid)
        # get new generator and pass it to Technician
        self._update_technician(pid)
        # return id of channel that has just been added
        return cid

    def add_replay(self, pid: int, data: List, name: str):
        """Add an dataset that will be replayed.

        Parameters:
        :param pid: (mandatory, int) ID of pipeline.
        :param data: (mandatory, list) Data to replay.
        :param name: (mandatory, string) Name of channel.
        """
        self._check_inputs(replay_data_=data, channel_name=name)
        frequency = self.topics.get_frequency(tid=pid)

        cid = self._add_channel(
            name_=name, frequency=frequency, type_="replay", replay_data_=data
        )
        # add channel to target pipeline
        self.pipelines[pid]["channel_id"].append(cid)
        # is pipeline currently inactive?
        if self.pipelines[pid]["active"] == 0:
            # switch pipeline on
            self.switch_pipeline(pid)
        # get new generator and pass it to Technician
        self._update_technician(pid)
        # return ids of channels that has just been added
        return cid

    def remove_channel(self, cid_):
        """Remove existing channel from each pipeline.

        Parameters:
        cid_ (mandatory, int): ID of channel.
        """
        # remove channel from channel dict
        self.channels.pop(cid_)
        # loop each pipeline
        for pid in self.pipelines:
            # is channel id in pipeline?
            if cid_ in self.pipelines[pid]["channel_id"]:
                # remove it.
                self.pipelines[pid]["channel_id"].remove(cid_)
                # no channels left on pipeline?
                if len(self.pipelines[pid]["channel_id"]) == 0:
                    # switch pipeline to inactive
                    self.switch_pipeline(pid)
                # call corresponding Technician.
                self._update_technician(pid)

    def publish_data(self, pid: int):
        """Get data and publish it to target host.

        :param pid: (mandatory, int) ID of pipeline.
        """
        topic = self.topics.get_topic(tid=pid)
        jdata = self.handlers.get_payload(pid=pid)
        self.handlers.publish(pid=pid, topic=topic, jdata=jdata)

    def _update_technician(self, pid_):
        """Get list of installed generators from technician. Compare with desired list. Take action if necessary.

        Parameters:
        pid_ (mandatory, int): Pipeline id.
        """
        # get corresponding technician
        techie = self.handlers[pid_]["technician"]

        # get keys (channel ids) of generators
        installed_generators = [key for key, gen in techie.generators.items()]
        desired_generators = self.pipelines[pid_]["channel_id"]

        # compare with current channel ids
        todos = [
            g
            for g in installed_generators + desired_generators
            if g not in installed_generators or g not in desired_generators
        ]

        # anything to do?
        for todo in todos:
            # install new generators?
            if todo in desired_generators:
                self._add_generator(pid_, todo)
            # remove installed generator?
            elif todo in installed_generators:
                self._remove_generator(pid_, todo)

    def _add_generator(self, pid_, cid_):
        """Init new generator and update list of corresponding technician.

        Parameters:
        pid_ (mandatory, int): Pipeline id.
        cid_ (mandatory, int): Channel id.
        """
        # get corresponding technician
        techie = self.handlers[pid_]["technician"]

        # create new generator
        gen = Generator(
            name_=self.channels[cid_]["name"],
            limits_=self.channels[cid_]["limits"],
            frequency=self.channels[cid_]["frequency"],
            type_=self.channels[cid_]["type"],
            dead_frequency=self.channels[cid_]["dead_frequency"],
            dead_period_=self.channels[cid_]["dead_period"],
            replay_data_=self.channels[cid_]["replay_data"],
        )

        # add generator to his dict of generators
        techie.generators[cid_] = gen

    def _remove_generator(self, pid_, cid_):
        """Remove old generator and update list of corresponding technician.

        Parameters:
        pid_ (mandatory, int): Pipeline id.
        cid_ (mandatory, int): Channel id.
        """
        # get corresponding technician
        techie = self.handlers[pid_]["technician"]
        # remove old generator from dict of generators
        techie.generators.pop(cid_)

    def add_handlers(self, pid: int):
        """
        Initializes instance of Generator, Clients, etc.. Pass these instances to their corresponding dicts.

        :param pid: (mandatory, int) ID of pipeline.
        """
        self.handlers.add_handler(pid=pid)

    def _add_pipeline(self, host_id: int, topic_id: int, name: str = '') -> int:
        """
        Add new pipeline but pay attention that the desired name of the new pipeline is unique.
        Make it unique if it is not.

        :param name: (mandatory, str) Name of the new pipeline.
        :param host_id: (mandatory, int) ID of host in host dictionary.
        :param topic_id: (mandatory, int) ID of topic in topic dictionary.
        :return: ID of pipeline that has just been added.

        Note:
        - name can also be None or an empty string.
        """
        pipeline_names = self.pipelines.get_names()
        if name in pipeline_names:
            name = self._get_unique_name(pipeline_names, name)
        return self.pipelines.add_pipeline(name=name, host_id=host_id, topic_id=topic_id)

    def switch_pipeline(self, pid: int):
        """
        Turn on/off a pipeline.

        :param pid: (mandatory, int) ID of the pipeline in the pipeline dict.
        """
        self.pipelines.switch_state(pid=pid)

    def _get_unique_name(self, names: List[str], name: str) -> str:
        """
        Find a new name for name_ so that it is unique in the list of names_.

        :param names: (mandatory, list of strings) List of names that are already in use.
        :param name: (mandatory, string) Name that should be unique to names.
        :return: unique name
        """
        while name in names:
            name = self._count_up(name)
        return name

    @staticmethod
    def _count_up(name: str, suffix: str = "_") -> str:
        """
        Search for pattern in name_. Add that pattern if not found or add +1 to existing pattern.

        :param name: (mandatory, string) Name that should be unique to names.
        :param suffix: (optional, string) Will be attached to very end of name.
        :return: modified name
        """
        # search for suffix and numbers at the very end of name.
        search = research(r"[" + suffix + r"]([0-9]+)$", name)
        # found something?
        if search:
            # what number was found?
            num = int(search.group(0)[1:])
            # add +1 to that number.
            return name[:-len(search.group(0))] + suffix + str(num + 1)
        return name + suffix + "0"

    @staticmethod
    def _check_inputs(**kwargs):
        """Check all inputs that are used to create a pipeline"""
        # ip
        if "ip" in kwargs:
            if not isinstance(kwargs["ip"], str):
                raise InvalidInputTypeError(
                    "Content of ip is type %s but should be a of type string."
                    % type(kwargs["ip"])
                )

        # port
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

        # topic
        if "topic" in kwargs:
            if not isinstance(kwargs["topic"], str):
                raise InvalidInputTypeError(
                    "Content of topic is type %s but should be a of type string."
                    % type(kwargs["topic"])
                )

        # frequency
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

        # channel_name
        if "channel_name" in kwargs:
            if not isinstance(kwargs["channel_name"], str):
                raise InvalidInputTypeError(
                    "Content of channel_name is type %s but should be a of type string."
                    % type(kwargs["channel_name"])
                )

        # channel_limits
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

        # channel_frequency
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

        # channel_type
        if "channel_type" in kwargs:
            if not isinstance(kwargs["channel_type"], str):
                raise InvalidInputTypeError(
                    "Content of channel_type is type %s but should be a of type string."
                    % type(kwargs["channel_type"])
                )

        # pipeline_name
        if "pipeline_name" in kwargs:
            if not isinstance(kwargs["pipeline_name"], str):
                raise InvalidInputTypeError(
                    "Content of pipeline_name is type %s but should be a of type string."
                    % type(kwargs["pipeline_name"])
                )

        # dead_frequency
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

        # dead_period_
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

        # replay_data_
        if "replay_data" in kwargs:
            if not isinstance(kwargs["replay_data"], list):
                raise InvalidInputTypeError(
                    "Content of replay_data is "
                    "type %s but should be an list." % type(kwargs["replay_data"])
                )
