"""This module is used to test the classes in forger.engine.plotter"""

from unittest.mock import patch

import numpy as np
import pytest
from matplotlib.lines import Line2D

from forger.engine.plotter import Plotter


@pytest.fixture()
def plotter():
    with patch.object(Plotter, "_run", return_value=True):
        return Plotter(ip="127.0.0.1", port=1234, topic="foo")


class TestPlotter:
    @pytest.mark.parametrize(
        "data,new_value,expected",
        [
            (np.array([1, 2, 3, 4]), 5, np.array([2, 3, 4, 5])),
            (
                np.array([None, None, 1, 2, 3, None]),
                None,
                np.array([None, 1, 2, 3, None, None]),
            ),
        ],
    )
    def test__add_data_point(self, plotter, data, new_value, expected):
        """
        Test the _add_data_point method of the Plotter class.
        """
        assert np.array_equal(
            expected, plotter._add_data_point(data=data, new_value=new_value)
        )

    def test__process_payload(self):
        """
        Test the _process_payload method of the Plotter class.
        """
        pass

    @pytest.mark.parametrize(
        "channel,latest_x,latest_y",
        [
            ("foo", 1234.567, -42.123),
            ("bar", 0, 0),
            ("foobar", -31, 122),
        ],
    )
    def test_add_and_remove_plot(self, plotter, channel, latest_x, latest_y):
        """
        Test the _add_plot and _remove_plot methods of the Plotter class.
        """
        assert len(plotter.plots) == 0
        plotter._add_plot(channel=channel, latest_x=latest_x, latest_y=latest_y)
        assert len(plotter.plots) == 1
        assert channel in plotter.plots
        assert isinstance(plotter.plots[channel], Line2D)
        plotter._remove_plot(channel=channel)
        assert len(plotter.plots) == 0

    @pytest.mark.parametrize(
        "channel,latest_x,latest_y,x,y",
        [
            ("foo", 1234.567, -42.123, 1234.898, 12.32),
            ("bar", 0, 0, 1, 1),
            ("foobar", -31, 122, 30, -32),
            ("nobar", 1, np.nan, 2, np.nan),
        ],
    )
    def test__update_plot(self, plotter, channel, latest_x, latest_y, x, y):
        """
        Test the _update_plot method of the Plotter class.
        """
        plotter._add_plot(channel=channel, latest_x=latest_x, latest_y=latest_y)
        plotter._update_plot(channel=channel, x=x, y=y)
        if channel in plotter.plots:
            x_data = plotter.plots[channel].get_xdata()
            y_data = plotter.plots[channel].get_ydata()
            assert x_data[-1] == x
            assert all([latest_x == xd for xd in x_data[:-1]])
            assert y_data[-1] == y
            assert all([latest_y == yd for yd in y_data[:-1]])
