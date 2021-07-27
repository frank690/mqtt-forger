"""This module contains all Connection classes that are used by the manager class."""

__all__ = [
    "Connections",
]

from typing import Tuple


class Connection:
    """
    Connection class that is created by Connections class.
    """
    def __init__(self, ip: str, port: int):
        """Initialize new connection.

        :param ip: (mandatory, string) IP of target host.
        :param port: (mandatory, int) Port of target host.
        """
        self.ip = ip
        self.port = port


class Connections:
    """
    Connections class that creates and keeps track of each Connection class.
    """

    def __init__(self):
        """Initialize variables"""
        self.connections = {}

    def add_connection(self, ip: str, port: int):
        """
        Add new connection to dict of connections.

        :param ip: (mandatory, string) IP of target host.
        :param port: (mandatory, int) Port of target host.
        """
        # get id of next connection
        cid = len(self.connections.keys())
        # add connection to dict
        self.connections[cid] = Connection(ip=ip, port=port)
        # return the id that has just been added
        return cid

    def get_address(self, cid: int) -> Tuple:
        """
        Get address information of connection with given id (pid).

        :param cid: (mandatory, int) id of connection.
        :return: ip and port as tuple.
        """
        return self.connections[cid].ip, self.connections[cid].port
