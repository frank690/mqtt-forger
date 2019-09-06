#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
# from IPython.core.debugger import set_trace

class Painter:

    MEMORY = 5/(24*60*60) # 5 seconds
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
        self.channels = {} 
        self.ax.set_autoscaley_on(True)
        self.hfmt = mdates.DateFormatter(self.DISPLAY_DATE_FORMAT)
        self.ax.xaxis.set_major_formatter(self.hfmt)
        self.ax.xaxis.set_major_locator(mdates.SecondLocator())
        self.ax.grid()
        # figure events
        self.fig.canvas.mpl_connect('close_event', self._on_close_figure)
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
        # get latest timestamp
        current_time = self._datestr2num(sample['timestamp'])
        oldest_time = current_time - self.MEMORY
        # get all channel names
        current_names = [*sample.keys()]
        current_names.remove('timestamp')
        # get list of existing channels
        old_names = [*self.channels.keys()]
        
        # loop over all channels
        for name in list(set(current_names + old_names)):
            # is channel unknown? 
            if name not in old_names:
                self._add_channel(name)
            # channel in current sample?
            if name in current_names:
                # append new data to each channel
                self.channels[name]['x'].append(current_time)
                self.channels[name]['y'].append(sample[name])
                
            # make sure data is up-to-date
            # create list for latest data
            validx = []
            validy = []
            # remove old data
            for (x,y) in zip(self.channels[name]['x'], self.channels[name]['y']):
                if x >= oldest_time:
                    validx.append(x)
                    validy.append(y)
            # assign new data
            self.channels[name]['x'] = validx
            self.channels[name]['y'] = validy
            
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
        # loop over each channel and update plot
        for chn in self.channels:
            self.channels[chn]['line'].set_data(self.channels[chn]['x'], self.channels[chn]['y'])
        # make sure limits are correct
        self.ax.relim()
        self.ax.autoscale_view()
        # flush it.
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
    def _on_close_figure(self, evt):
        """Triggered when plot is closed by the user. End connection.
        """
        self.client.loop_stop()
        
    def _datestr2num(self, str_):
        """Convert datestring to num
        """
        return mdates.date2num(datetime.strptime(str_, self.DATE_FORMAT))
        
    def _add_channel(self, channel_):
        """Add new line to plot for a new channel
        """
        self.channels[channel_] = {}
        self.channels[channel_]['line'] = self.ax.plot([],[], '-')[0]
        self.channels[channel_]['x'] = []
        self.channels[channel_]['y'] = []