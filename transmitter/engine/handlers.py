"""This module contains all Handlers classes that are used by the manager class."""

__all__ = [
    "Handlers",
]

from transmitter.auxiliary.exceptions import OnConnectError
from transmitter.engine.technician import Technician

import paho.mqtt.client as mqtt


class Handler:
    """
    Handlers class that is created by Handlers parent class.
    """
    def __init__(self, technician: Technician, mqtt_client: mqtt.Client):
        """
        Initialize handler class.
        """
        self.technician = technician
        self.mqtt_client = mqtt_client

    def get_payload(self) -> str:
        """
        Get payload from technician of this handler.
        :return: payload of technician.
        """
        return self.technician.get_payload()

    def publish(self, topic: str, jdata: str):
        """
        Publish given jdata on topic on mqtt client of this handler.
        """
        self.mqtt_client.publish(topic=topic, payload=jdata)


class Handlers:
    """
    Handlers parent class that creates and keeps track of each handler child class.
    """

    def __init__(self):
        """Initialize variables"""
        self.handlers = {}

    def add_handler(self, pid: int, connections):
        """
        Add new handler to dict of handlers.

        :param pid: (mandatory, int) ID to assign to new handler.
        """
        client = mqtt.Client()
        try:
            client.connect(
                self.connections.get_address(cid=pid), 60
            )
        except Exception as err:
            raise OnConnectError(
                "Failed to establish connection to %s:%i - %s"
                % self.connections.get_address(cid=pid), err
            )

        self.handlers[pid] = Handler(technician=Technician(), mqtt_client=client)

    def get_payload(self, pid: int) -> str:
        """
        Get payload of technician of handler with given id (pid).

        :param pid: (mandatory, int) ID of pipeline.
        :return: payload data
        """
        return self.handlers[pid].get_payload()

    def publish(self, pid: int, topic: str, jdata: str):
        """
        Publish given jdata of topic on handler with pid.

        :param pid: (mandatory, int) ID of handler to use.
        :param topic: (mandatory, str) Topic to publish data on.
        :param jdata: (mandatory, str) JSON data to publish.
        """
        self.handlers[pid].publish(topic=topic, jdata=jdata)
