"""This module contains all Topic classes that are used by the manager class."""

__all__ = [
    "Topics",
]

from typing import List


class Topic:
    """
    Topic class that is created by Topics class.
    """
    def __init__(self, topic: str, frequency: float):
        """
        Initialize new topic class.
        """
        self.topic = topic
        self.frequency = frequency


class Topics:
    """
    Topics class that creates and keeps track of each Topic class.
    """

    def __init__(self):
        """
        Initialize variables
        """
        self.topics = {}

    def add_topic(self, topic: str, frequency: float) -> int:
        """
        Add topic to dict of topics.

        :param topic: (mandatory, string) Name of topic that data should be published on.
        :param frequency: (mandatory, float) Frequency (in Hz) in that the data will be published on the given topic.
        :return: id of new topic.
        """
        tid = len(self.topics.keys())
        self.topics[tid] = Topic(topic=topic, frequency=frequency)
        return tid

    def get_frequency(self, tid: int) -> float:
        """
        Get frequency of topic with given id (tid).

        :param tid: (mandatory, int) ID of topic
        :return: Frequency of float
        """
        return self.topics[tid].frequency

    def get_topic(self, tid: int) -> str:
        """
        Get topic value of topic with given id (tid).

        :param tid: (mandatory, int) ID of topic
        :return: Value of topic
        """
        return self.topics[tid].topic
