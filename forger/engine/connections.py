"""This module contains all Connection classes that are used by the manager class."""

__all__ = [
    "Connection",
    "Listener",
]

from typing import Callable, Tuple

import paho.mqtt.client as mqtt

from forger.auxiliary.exceptions import OnConnectError


class Connection:
    """
    Connection class that is created by Connections class.
    """

    def __init__(self, ip: str, port: int):
        """
        Initialize new connection.

        :param ip: IP of target host.
        :param port: Port of target host.
        """
        self.ip = ip
        self.port = port
        self.mqtt_client = mqtt.Client()

        self.check_connection()

    def check_connection(self):
        """
        Try to establish a test connection on the given ip and port.
        Raise error if attempt fails.
        """
        try:
            self.mqtt_client.connect(self.ip, self.port, 60)
        except Exception as err:
            raise OnConnectError(
                "Failed to establish connection to %s:%i - %s"
                % (self.ip, self.port, err)
            )

    def get_address(self) -> Tuple:
        """
        Get address information (ip and port).

        :return: ip and port as tuple.
        """
        return self.ip, self.port


class Listener:  # pragma: no cover
    """
    Class to listen for new data on mqtt connection.
    """

    def __init__(self, ip: str, port: int, topic: str, on_message: Callable):
        """
        Initialize new connection.

        :param ip: IP of target host.
        :param port: Port of target host.
        :param topic: Topic to listen and wait for data.
        :param on_message: Function to define what will happen when data is received.
        """
        self.ip = ip
        self.port = port
        self.topic = topic

        self.connection = Connection(ip=ip, port=port)
        self.connection.mqtt_client.on_connect = self._on_connect
        self.connection.mqtt_client.on_message = on_message
        self.connect()

    def connect(self):
        """
        Establish connection to mqtt broker
        """
        self.connection.mqtt_client.connect(self.ip, self.port, 60)
        self.connection.mqtt_client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        """
        Define what to do when connection was established.
        """
        self.connection.mqtt_client.subscribe(self.topic)

    def disconnect(self):
        """
        Terminate connection to mqtt broker
        """
        self.connection.mqtt_client.loop_stop()
        self.connection.mqtt_client.disconnect()
