"""This module contains all Connection classes that are used by the manager class."""

__all__ = [
    "Connection",
]

from typing import Tuple

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
