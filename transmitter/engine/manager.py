"""Main module to run the mqtt-forger."""

# import own libs
from transmitter.engine.generator import Generator
from transmitter.engine.pipelines import Pipelines, Pipeline
from transmitter.auxiliary.constants import DEFAULT_PIPELINE_SETTINGS

# import native libs
from typing import List


class Manager:
    """
    Class that manages the mqtt-forger and contains all publicly available methods to run.
    """

    # set default values
    defaults = DEFAULT_PIPELINE_SETTINGS

    def __init__(self, verbose=False):
        """
        Initialize variables

        :param verbose: (optional, boolean) Boolean flag whether or not to print output.
        """
        self.pipelines = Pipelines()
        self.verbose = verbose

    def add_pipeline(self, ip: str, port: int, topic: str, frequency: float, pipeline_name: str = '') -> Pipeline:
        """
        Call Pipelines class to create a new pipeline.

        :param ip: (mandatory, string) IP of target host.
        :param port: (mandatory, int) Port of target host.
        :param topic: (mandatory, string) Name of topic that data should be published on.
        :param frequency: (mandatory, float) Frequency (in Hz) in that the data will be published on the given topic.
        :param pipeline_name: (optional, str) Optional name of pipeline.
        :return: New Pipeline class instance.
        """
        return self.pipelines.add(ip=ip, port=port, frequency=frequency, topic=topic, pipeline_name=pipeline_name)

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
