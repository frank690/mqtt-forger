#!/usr/bin/env python3
import json
import numpy as np
from datetime import datetime

class InvalidInputTypeError(Exception):
    """The InvalidInputTypeError is raised whenever an instance of the Generator class is initialized with unexpected types of certain input variables."""
    pass

class InvalidInputValueError(Exception):
    """The InvalidInputValueError is raised whenever an instance of the Generator class is initialized with invalid values of certain input variables."""
    pass

class SeedReplantError(Exception):
    """The SeedReplantError is raised whenever a replant of a seed is being tried but no seed has ever been planted before."""
    pass

class Generator:
    """
    Class to compute current value of an initialized channel.
    """
    def __init__(self, channel_name_, channel_limits_, channel_frequency_, novelty_frequency_, novelty_duration_, novelty_impact_, seed_=None):
            # init parameters for this instance
            self.channel_name=channel_name_ # name of current channel
            self.channel_limits=channel_limits_ # lower/upper limits of data
            self.channel_frequency=channel_frequency_ # frequency in that the data will repeat itself
            self.novelty_frequency=novelty_frequency_ # frequency in that novelties (noise) will appear
            self.novelty_duration=novelty_duration_ # duration of the novelty
            self.novelty_impact=novelty_impact_ # scaling factor
            self.seed=seed_ # random number seed
            
            # store basetime
            self.basetime = datetime.now()
            # check input types
            self._check_input()
            # set seed to noise?
            if self.seed:
                self._plant_a_seed()
            
    def _check_input(self):
        """ Check the given input data for type.
        """
        # channel_name_
        if not isinstance(self.channel_name, str):
            raise InvalidInputTypeError("Content of channel_name_ is type %s but should be a of type string." % type(self.channel_name))
            
        # channel_limits_
        if not isinstance(self.channel_limits, list):
            raise InvalidInputTypeError("Content of channel_limits_ is type %s but should be a of type list." % type(self.channel_limits))
        if not all(isinstance(x, (int, float)) for x in self.channel_limits):
            raise InvalidInputValueError("Not all values of channel_limits are of type int or float.")
        
        # channel_frequency_
        if not isinstance(self.channel_frequency, (int, float)):
            raise InvalidInputTypeError("Content of channel_frequency_ is type %s but should be a of type int or float." % type(self.channel_frequency))
        if self.channel_frequency <= 0:
            raise InvalidInputValueError("Value of channel_frequency_ is negative (%s) but should be positive." % str(self.channel_frequency))
         
        # novelty_frequency_
        if not isinstance(self.novelty_frequency, (int, float)):
            raise InvalidInputTypeError("Content of novelty_frequency_ is type %s but should be a of type int or float." % type(self.novelty_frequency))
        if self.novelty_frequency <= 0:
            raise InvalidInputValueError("Value of novelty_frequency_ is negative (%s) but should be positive." % str(self.novelty_frequency))
            
        # novelty_duration_
        if not isinstance(self.novelty_duration, (int, float)):
            raise InvalidInputTypeError("Content of novelty_duration_ is type %s but should be a of type int or float." % type(self.novelty_duration))
        if self.novelty_duration < 0:
            raise InvalidInputValueError("Value of novelty_duration_ is negative (%s) but should be positive or zero." % str(self.novelty_duration))
            
        # novelty_impact_
        if not isinstance(self.novelty_impact, (int, float)):
            raise InvalidInputTypeError("Content of novelty_impact_ is type %s but should be a of type int or float." % type(self.novelty_impact))
            
        # seed_
        if self.seed:
            if not isinstance(self.seed, int):
                raise InvalidInputTypeError("Content of seed_ is type %s but should be a of type int." % type(self.seed))          
                
    def _get_clean_data(self, times_=None):
        """ Get data without noise.
        """
        # times not given?
        if not times_:
            # get current time
            (seconds, _) = self._get_times()
        else:
            # get times since start
            (seconds, _) = times_
            
        # get current position in radiant degree
        x = 2 * np.pi * ((seconds%(1/self.channel_frequency)) / (1/self.channel_frequency))
        # compute y and rescale it
        y = self._rescale(np.sin(x))
        # return data
        return y
    
    def _get_noise(self, times_=None):
        """ Get the noise.
        """
        # times not given?
        if not times_:
            # get current time
            (seconds, _) = self._get_times()
        else:
            # get times since start
            (seconds, _) = times_
            
        # define output
        y = 0.0
        # is noise currently active?
        if (seconds%(1/self.novelty_frequency) <= self.novelty_duration):
            # generate random noise
            y = np.random.normal(scale=self.novelty_impact)
        # return output
        return y
    
    def get_data(self, times_=None):
        """ Get the data including the noise.
        """
        # time not given?
        if not times_:
            # get current time
            times_ = self._get_times()
        # get clean data
        y = self._get_clean_data(times_)
        # add noise
        y = y + self._get_noise(times_)
        # return data
        return y

    def get_payload(self):
        """ Get the data, including the noise, dump it into json and return it to NoveltyProducer
        """
        # get times
        times = self._get_times()
        # extract iso time
        (_, iso) = times
        # get payload
        data = {'timestamp':iso, self.channel_name:self.get_data(times)}
        # pack it into json
        jdata = json.dumps(data)
        # pass data
        return jdata

    def _get_times(self):
        """ Get current datetime and transform it to iso format as well as the seconds since this generator was initialized.
        """
        # get current datetime
        cdt = datetime.now()
        # get current datetime in iso
        iso = cdt.isoformat()
        # get time diff
        dt = cdt - self.basetime
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
        
    def _plant_a_seed(self, seed_=None):
        """ Set (or reset) a seed to the random noise generator.
        """
        # seed given?
        if seed_:
            np.random.seed(seed_)
        else:
            # replant seed from init
            if self.seed:
                np.random.seed(self.seed)
            else:
                # someone fucked up.
                raise SeedReplantError("Replanting of seed is not possible, since no seed has ever been planted before!")