#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
# from IPython.core.debugger import set_trace

class Painter:

    MAX_MSGS = 100
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
    DISPLAY_DATE_FORMAT = '%M:%S'
    
    """Class to listen to an mqtt connection and draw all the data.
    """
    def __init__(self, ip_, port_, topic_):
        """Pass information about target mqtt connection to init painter.
        """
        # inputs
        self.ip = ip_
        self.port = port_
        self.topic = topic_
        # internal definitions
        # init plot
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.lines, = self.ax.plot([],[], '-')
        self.ax.set_autoscaley_on(True)

        self.hfmt = mdates.DateFormatter(self.DISPLAY_DATE_FORMAT)
        self.ax.xaxis.set_major_formatter(self.hfmt)
        self.ax.xaxis.set_major_locator(mdates.SecondLocator())
        self.ax.grid()
        # client
        self.data = {}
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self._establish_connection()
        
    def _establish_connection(self):
        """Establish connection to mqtt broker
        """
        self.client.connect(self.ip, self.port, 60)
        self.client.loop_forever()

    def _on_connect(self, client, userdata, flags, rc):
        """Define what to do when connection was established.
        """
        # subscribe to topic
        client.subscribe(self.topic)

    def _on_message(self, client, userdata, msg):
        """Define what to do when message is received.
        """
        # collect payload
        sample = json.loads(msg.payload.decode())
        # get timestamp and convert to datetime
        key = datetime.strptime(sample['timestamp'], self.DATE_FORMAT)
        # create new subdict for nice timestamp
        self.data[key] = {}
        # add each key+value to datastore (except timestamp itself)
        for k,v in sample.items():
            if k != 'timestamp':
                self.data[key][k] = v 
        # store list of timestamps
        self.times = [*self.data].copy()
        # sort it
        self.times.sort(reverse=True)
        # make sure only latest data is kept.
        self._remove_old_data()
        # update plot
        self._draw()
        
    def _remove_old_data(self):
        """Make sure old data is removed from datastore.
        """
        # get times that drop out
        dropouts = self.times[self.MAX_MSGS:]
        # adjust times
        self.times = self.times[:self.MAX_MSGS]
        # make local copy of datastore
        datastore = self.data.copy()
        # loop over dropouts
        for dropout in dropouts:
            datastore.pop(dropout)
        # set new datastore
        self.data = datastore
                
    def _draw(self):
        """Plot latest datapoints.
        """
        # data to plot
        x = [mdates.date2num(dt) for dt in self.times]
        y = []
        # loop over each timestamp to collect corresponding data.
        for ts in self.times:
            y.append(tuple(self.data[ts].values()))
        
        # update the plot
        self.lines.set_xdata(x)
        self.lines.set_ydata(y)
        # make sure limits are correct
        self.ax.relim()
        self.ax.autoscale_view()
        # flush it.
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
    