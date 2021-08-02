"""Main module to run the mqtt-forger."""

from typing import List

from apscheduler.schedulers.background import BackgroundScheduler

from forger.auxiliary.constants import DEFAULT_PIPELINE_SETTINGS
from forger.auxiliary.misc import get_new_id
from forger.engine.pipelines import Pipeline


class Manager:
    """
    Class that manages the mqtt-forger and contains all publicly available methods to run.
    """

    # set default values
    defaults = DEFAULT_PIPELINE_SETTINGS

    def __init__(self):
        """
        Initialize variables
        """
        self.pipelines = {}
        self.Scheduler = BackgroundScheduler()
        self.Scheduler.start()

    def add_pipeline(
        self, ip: str, port: int, topic: str, frequency: float, pipeline_name: str = ""
    ) -> Pipeline:
        """
        Call Pipelines class to create a new pipeline.

        :param ip: IP of target host.
        :param port: Port of target host.
        :param topic: Name of topic that data should be published on.
        :param frequency: Frequency (in Hz) in that the data will be published on the given topic.
        :param pipeline_name: Optional name of pipeline.
        :return: New Pipeline class instance.
        """
        pid = get_new_id(self.pipelines)

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

    def get_names(self) -> List[str]:
        """
        Get names of all pipelines that have already been added.
        :return: List of names (strings) of pipelines.
        """
        return [v.name for k, v in self.pipelines.items()]
