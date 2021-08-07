"""Use this module to visualize the data send to the target."""

__all__ = [
    "Plotter",
]

import json
import time

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

from forger.auxiliary.constants import DISPLAY_DATE_FORMAT, MEMORY
from forger.auxiliary.misc import datestr2num
from forger.engine.connections import Listener


class Plotter:
    """
    Class to listen to an mqtt connection and draw all the data.
    """

    def __init__(self, ip: str, port: int, topic: str, memory: int = MEMORY):
        """
        Initialize painter.
        :param ip: IP to scan for data.
        :param port: Port to scan for data.
        :param topic: Topic to listen to.
        :param memory: Number of data points to show at the same time.
        """
        self.memory = memory

        self.running = True
        self.plots = dict()
        self.buffer = []

        self.listener = Listener(
            ip=ip, port=port, topic=topic, on_message=self._on_message
        )

        self._create_figure()
        self._run()

    def _run(self):
        """
        Define main running loop.
        """
        while self.running:
            plt.pause(0.0001)

            if len(self.buffer) > 0:
                self.update(payload=self.buffer[0])
                self.buffer = self.buffer[1:]
                print(f"# payloads in buffer: {len(self.buffer)}")
            else:
                time.sleep(0.1)

    def _stop(self):
        """
        Define what to do when things should stop.
        """
        self.running = False
        self.listener.disconnect()

    def _create_figure(self):
        """
        Makes sure that the figure exists and is visible.
        Create new figure if necessary.
        """
        self.fig = plt.figure()
        self.gs = self.fig.add_gridspec()
        self.ax = self.gs.subplots(sharex=True, sharey=True)

        plt.ion()

        self.ax.set_autoscaley_on(True)
        formatter = mdates.DateFormatter(DISPLAY_DATE_FORMAT)
        self.ax.xaxis.set_major_formatter(formatter)
        # self.ax.xaxis.set_major_locator(mdates.SecondLocator())
        self.ax.grid()
        self.fig.canvas.mpl_connect("close_event", self._stop)

        plt.show()

    def _on_message(self, client, userdata, msg):
        """
        Define what to do when message is received.
        """
        self.buffer.append(json.loads(msg.payload.decode()))

    def update(self, payload: dict):
        """
        Use the given payload to update all plots.
        """
        x = datestr2num(payload.pop("timestamp"))

        for channel in list(self.plots):
            self._update_plot(channel=channel, x=x, y=payload.get(channel))

        for missing_plot in set(payload) - set(self.plots):
            self._add_plot(
                channel=missing_plot, latest_x=x, latest_y=payload.get(missing_plot)
            )

        self._update_canvas()

    def _update_plot(self, channel: str, x: float, y: float):
        """
        Update visualization of each plot.
        :param channel: Name of plot/channel to update.
        :param x: Timestamp of latest data point.
        :param y: Latest data point of the given channel.
        """
        x_data = self._add_data_point(data=self.plots[channel].get_xdata(), new_value=x)
        y_data = self._add_data_point(data=self.plots[channel].get_ydata(), new_value=y)

        if np.isnan(y_data).all():
            self._remove_plot(channel=channel)
        else:
            self.plots[channel].set_data(x_data, y_data)

    def _add_plot(self, channel: str, latest_x: float, latest_y: float):
        """
        Create a new plot. Use latest x and y values to fill initial data arrays.
        :param channel: Name of plot/channel to update.
        :param latest_x: Timestamp of latest data point.
        :param latest_y: Latest data point of the given channel.
        """
        x = [latest_x] * self.memory
        y = [latest_y] * self.memory

        self.plots[channel] = self.ax.plot(x, y, "-", label=channel)[0]
        self.ax.legend(loc=2)

    def _remove_plot(self, channel: str):
        """
        Removes a plot.
        :param channel: Name of plot/channel to remove.
        """
        self.ax.lines.remove(self.plots[channel])
        self.plots.pop(channel)
        self.ax.legend(loc=2)

    @staticmethod
    def _add_data_point(data: np.array, new_value: float) -> np.array:
        """
        Add the new_value to the list of data without changing it size (oldest value will be removed).
        :param data: numpy array of data points to update.
        :param new_value: new value to insert into data.
        :return: updated list of data.
        """
        return np.insert(data[1:], data.size - 1, new_value)

    def _update_canvas(self):
        """
        After plots were updated, the scaling or limits might be off.
        Take care of that.
        """
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
