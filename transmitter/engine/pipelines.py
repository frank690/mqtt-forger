"""This module contains all Pipeline classes that are used by the manager class."""

__all__ = [
    "Pipelines",
]

from typing import List
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.job import Job


class Pipeline:
    """
    Pipeline class that is created by Pipelines class.
    """
    def __init__(self, host_id: int, topic_id: int, job: Job, name: str = ''):
        """Adding a new entry in the pipeline dictionary.

        :param host_id: (mandatory, int) ID of host in host dictionary.
        :param topic_id: (mandatory, int) ID of topic in topic dictionary.
        :param job: (mandatory, apscheduler.job.Job) Job of apscheduler class for this pipeline.
        :param name: (optional, str) Name of the new pipeline.

        Note:
        - name can also be None or an empty string.
        """
        self.host_id = host_id
        self.topic_id = topic_id
        self.job = job
        self.name = name
        self.channel_id = []
        self.active = False

    def switch_state(self):
        """
        Switch state of current state.
        """
        self.active = not self.active
        if self.active:
            self.job.resume()
        else:
            self.job.pause()


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

    def add_pipeline(self, host_id: int, topic_id: int, name: str = '') -> int:
        """Adding a new entry in the pipeline dictionary.

        :param name: (mandatory, str) Name of the new pipeline.
        :param host_id: (mandatory, int) ID of host in host dictionary.
        :param topic_id: (mandatory, int) ID of topic in topic dictionary.
        :return: id of pipeline that has just been added.

        Note:
        - name can also be None or an empty string.
        """
        pid = len(self.pipelines)
        job = self.Scheduler.get_job(str(pid))
        self.pipelines[pid] = Pipeline(name=name, host_id=host_id, topic_id=topic_id, job=job)
        return pid

    def switch_state(self, pid: int):
        """
        Switches the state of the pipeline with the given id (pid) to either active / inactive.

        :param pid: (mandatory, int) ID of pipeline.
        """
        self.pipelines[pid].switch_state()

    def create_pipeline(self, ip: str, port: int, topic: str, frequency: float, pipeline_name: str):
        # check inputs
        self._check_inputs(
            ip=ip,
            port=port,
            topic=topic,
            frequency=frequency,
            pipeline_name=pipeline_name,
        )
        # add host
        host_id = self.connections.add_connection(ip, port)
        # add topic
        topic_id = self._add_topic(topic, frequency)
        # add everything to pipeline
        pipeline_id = self._add_pipeline(name=pipeline_name, host_id=host_id, topic_id=topic_id)
        # init and assign generator for each new pipeline
        self._add_handlers(pipeline_id)
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