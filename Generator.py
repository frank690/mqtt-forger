#!/usr/bin/env python3
import json
import numpy as np
from datetime import datetime

class Generator:
    """
    Class to compute current value of an initialized channel.
    """
    def __init__(self, channel_name_, channel_limits_, channel_frequency_, novelty_frequency_, novelty_duration_, novelty_impact_):
            # init parameters for this instance
            self.channel_name=channel_name_ # name of current channel
            self.channel_limits=channel_limits_ # lower/upper limits of data
            self.channel_frequency=channel_frequency_ # frequency in that the data will repeat itself
            self.novelty_frequency=novelty_frequency_ # frequency in that novelties (noise) will appear
            self.novelty_duration=novelty_duration_ # duration of the novelty
            self.novelty_impact=novelty_impact_ # scaling factor
            # store basetime
            self.basetime = datetime.now()

    def _get_clean_data(self):
        """Get data without noise.
        """
        # get seconds since start
        (seconds, iso) = self._get_times()
        # get current position in radiant degree
        x = 2 * np.pi * ((seconds%(1/self.channel_frequency)) / (1/self.channel_frequency))
        # compute y and rescale it
        y = self._rescale(np.sin(x))
        # return data
        return y
    
    def _get_noise(self):
        """ Get the noise.
        """
        # get times since start
        (seconds, iso) = self._get_times()
        # define output
        y = 0
        # is noise currently active?
        if (seconds%(1/self.novelty_frequency) <= self.novelty_duration):
            # generate random noise
            y = np.random.normal(scale=self.novelty_impact)
        # return output
        return y
    
    def get_data(self):
        """ Get the data including the noise.
        """
        # get clean data
        y = self._get_clean_data()
        # add noise
        y = y + self._get_noise()
        # return data
        return y

    def get_payload(self):
        """ Get the data, including the noise, dump it into json and return it to NoveltyProducer
        """
        # get iso time
        (_, iso) = self._get_times()
        # get payload
        data = {'timestamp':iso, self.channel_name:self.get_data()}
        # pack it into json
        jdata = json.dumps(data)
        # pass data
        return jdata

    def _get_times(self):
        """ Get current time in iso format as well as the seconds since this generator was initialized.
        """
        # get current datetime in iso
        iso = datetime.now().isoformat()
        # get time diff
        dt = datetime.now() - self.basetime
        # get seconds since basetime
        seconds = dt.seconds + dt.microseconds/1E6
        # return seconds since basetime and iso time
        return (seconds, iso)

    def _rescale(self, value_):
        """ Rescale value to new scale.

        Parameters:
        value_ (mandatory, float): Value to rescale.

        Note:
        - Old scale is fixed to be [-1, 1]
        """
        # get lower/upper limit
        max = np.max(self.channel_limits)
        min = np.min(self.channel_limits)
        # rescale current value
        value = ((max-min)/(1-(-1))) * (value_ - (-1)) + min
        # return rescaled value
        return value