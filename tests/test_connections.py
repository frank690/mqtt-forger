"""This module is used to test the functions in  forger.engine.connections"""

import pytest

from forger.auxiliary.exceptions import OnConnectError
from forger.engine.connections import Connection


class TestConnection:
    @pytest.mark.parametrize(
        "ip,port,expected",
        [
            ("127.0.0.1", 1234, None),
            ("1.2.3.4.5.6", 1234815, OnConnectError),
            ("thereisnomqttbroker.here", 1883, OnConnectError),
        ],
    )
    def test_check_connection(self, ip, port, expected):
        """
        Test the check_connection method
        """
        if expected is None:
            con = Connection(ip=ip, port=port)
        else:
            with pytest.raises(expected):
                Connection(ip=ip, port=port)

    @pytest.mark.parametrize(
        "ip,port",
        [
            ("127.0.0.1", 1234),
        ],
    )
    def test_get_address(self, ip, port):
        """
        Test the get_address method
        """
        con = Connection(ip=ip, port=port)
        assert con.get_address() == (ip, port)
