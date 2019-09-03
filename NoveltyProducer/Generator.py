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
    
    VALID_TYPES = ['sin', 'random', 'fixed']
    
    def __init__(self, name_, limits_, frequency_, type_='sin', dead_frequency_=1, dead_period_=0, seed_=None):
            # init parameters for this instance
            self.name=name_ # name of current channel
            self.limits=limits_ # lower/upper limits of data
            self.frequency=frequency_ # frequency in that the data will repeat itself
            self.type=type_ # type of data generation. default is sin.
            self.dead_frequency=dead_frequency_ # frequency in that the channels output will drop to zero
            self.dead_period=dead_period_ # period (in seconds) of dead time
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
        # name_
        if not isinstance(self.name, str):
            raise InvalidInputTypeError("Content of name_ is type %s but should be a of type string." % type(self.name))
            
        # limits_
        if not isinstance(self.limits, list):
            raise InvalidInputTypeError("Content of limits_ is type %s but should be a of type list." % type(self.limits))
        if not all(isinstance(x, (int, float)) for x in self.limits):
            raise InvalidInputValueError("Not all values of limits are of type int or float.")
        
        # frequency_
        if not isinstance(self.frequency, (int, float)):
            raise InvalidInputTypeError("Content of frequency_ is type %s but should be a of type int or float." % type(self.frequency))
        if self.frequency <= 0:
            raise InvalidInputValueError("Value of frequency_ is negative (%s) but should be positive." % str(self.frequency))
        
        # type_
        if not isinstance(self.type, str):
            raise InvalidInputTypeError("Content of type_ is type %s but should be a of type string." % type(self.type))
        if self.type not in self.VALID_TYPES:
            raise InvalidInputValueError("Value of type_ (%s) is not valid." % str(self.type))
        
        # dead_frequency_
        if not isinstance(self.dead_frequency, (int, float)):
            raise InvalidInputTypeError("Content of dead_frequency_ is type %s but should be a of type int or float." % type(self.dead_frequency))
        if self.dead_frequency <= 0:
            raise InvalidInputValueError("Value of dead_frequency_ is negative (%s) but should be positive." % str(self.dead_frequency))
        
        # dead_period_
        if not isinstance(self.dead_period, (int, float)):
            raise InvalidInputTypeError("Content of dead_period_ is type %s but should be a of type int or float." % type(self.dead_period))
        if self.dead_period < 0:
            raise InvalidInputValueError("Value of dead_period_ is negative (%s) but should be zero or positive." % str(self.dead_period))
        
        # seed_
        if self.seed:
            if not isinstance(self.seed, int):
                raise InvalidInputTypeError("Content of seed_ is type %s but should be a of type int." % type(self.seed))          
    
    def get_data(self, cdt_):
        """ Get the data including the noise.
        """
        # get times since start
        seconds = self._seconds_since_init(cdt_)
        # dead time currently active?
        if (seconds%(1/self.dead_frequency) < self.dead_period):
            y = 0
        else:
            # what data is generated?
            if self.type == 'sin':
                # get current position in radiant degree
                x = 2 * np.pi * ((seconds%(1/self.frequency)) / (1/self.frequency))
                # compute y and rescale it
                yr = np.sin(x)
            elif self.type == 'random':
                yr = np.random.rand()
            elif self.type == 'fixed':
                yr = 1
            # rescale data.
            y = self._rescale(yr)
        # return data
        return y
        
    def _seconds_since_init(self, cdt_=None):
        """ Get seconds since init of this class.
        """
        # no time given?
        if not cdt_:
            cdt_ = datetime.now()
        # get time diff
        dt = cdt_ - self.basetime
        # get seconds since basetime
        seconds = dt.seconds + dt.microseconds/1E6
        # return seconds since basetime and iso time
        return seconds

    def _rescale(self, value_):
        """ Rescale value to new scale.

        Parameters:
        value_ (mandatory, float): Value to rescale.

        Note:
        - Old scale is fixed to be [-1, 1]
        """
        # get lower/upper limit
        max = np.max(self.limits)
        min = np.min(self.limits)
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