"""This module contains all Handlers classes that are used by the manager class."""

__all__ = [
    "Handler",
]

from transmitter.auxiliary.exceptions import OnConnectError
from transmitter.engine.technician import Technician

import paho.mqtt.client as mqtt
from typing import Optional


class Handler:
    """
    Handlers class that has a technician instance for computing payloads and a mqtt client instance for sending data.
    """
    def __init__(
            self, topic: str, frequency: float, technician: Optional[Technician] = None,
            mqtt_client: Optional[mqtt.Client] = None
    ):
        """
        Initialize handler class.

        :param topic: (mandatory, string) Name of topic that data should be published on.
        :param frequency: (mandatory, float) Frequency (in Hz) in that the data will be published on the given topic.
        :param technician: (mandatory, Technician) Instance of Technician class to use.
        :param mqtt_client: (mandatory, mqtt.Client) Instance of mqtt client class to use.
        """

        self.topic = topic
        self.frequency = frequency

        if technician is None:
            self.technician = Technician()
        else:
            self.technician = technician

        if mqtt_client is None:
            self.mqtt_client = mqtt.Client()
        else:
            self.mqtt_client = mqtt_client

    def check_connection(self, ip: str, port: int):
        """
        Try to establish a test connection on the given ip and port.
        Raise error if attempt fails.

        :param ip: (mandatory, str) IP to connect to.
        :param port: (mandatory, int) Port to connect to.
        """
        try:
            self.mqtt_client.connect(
                ip, port, 60
            )
        except Exception as err:
            raise OnConnectError(
                "Failed to establish connection to %s:%i - %s"
                % ip, port, err
            )

    def get_payload(self) -> str:
        """
        Get payload from technician of this handler.
        :return: payload of technician.
        """
        return self.technician.get_payload()

    def publish(self):
        """
        Publish data via mqtt client of this handler on topic that was set upon init of this class.
        """
        self.mqtt_client.publish(topic=self.topic, payload=self.get_payload())

    def _remove_generator(self, pid_, cid_):
        """
        Remove old generator and update list of corresponding technician.

        :param pid: (mandatory, int) Pipeline id.
        :param cid: (mandatory, int) Channel id.
        """
        # get corresponding technician
        techie = self.handlers[pid_]["technician"]
        # remove old generator from dict of generators
        techie.generators.pop(cid_)