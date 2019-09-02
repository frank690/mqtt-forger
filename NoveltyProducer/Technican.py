#!/usr/bin/env python3

from NoveltyProducer.Generator import Generator
from datetime import datetime
import json

class InvalidInputTypeError(Exception):
    """The InvalidInputTypeError is raised whenever a specific input of a specific function has an invalid/unexpected type."""
    pass

class InvalidInputValueError(Exception):
    """The InvalidInputValueError is raised whenever a specific input of a specific function has an invalid/unexpected value."""
    pass

class Technican:
    """Class to manage multiple generator instances at once.
    """
    def __init__(self, generators_):
        """Pass the technican a dict of all generators (and their ids) he needs to take care of.
        """
        # store list locally
        self.generators = generators_
        # check input types
        self._check_input()
            
    def _check_input(self):
        """ Check the given input data for type.
        """
        # generators_
        if not isinstance(self.generators, dict):
            raise InvalidInputTypeError("The parameter generators_ is type %s but should be a of type dict." % type(self.generators))
        if not all(isinstance(gen, Generator) for key, gen in self.generators.items()):
            raise InvalidInputValueError("Not all values of generators are an instance of class NoveltyProducer.Generator.")
            
    def _get_overall_output(self, name_, time_=None):
        """Get the combined output of all generators.
        
        Parameters:
        :param name_: (Mandatory, string) Name of channel that the data should be extracted from.
        :param time_: (Optional, datetime) Timestamp that the data should be extracted from.
        """
        # no time given?
        if not time_:
            # get current time.
            time = datetime.now()
        else:
            time = time_
        
        # loop over each generator and get each output.
        each_y = [gen.get_data(time) for key, gen in self.generators.items() if gen.name == name_]
        # sum up each output and return it.
        return sum(each_y)
    
    def _get_unique_channels(self):
        """ Extract the unique channel namessince multiple generators can output on the same channel (name).
        """
        return list(set([gen.name for key, gen in self.generators.items()]))
            
    def get_payload(self):
        """ Gather the data of all generators and pack it into a nice json.
        """
        # get current time.
        time = datetime.now()
        # transform to iso
        iso = time.isoformat()
        # create payload template
        data = {'timestamp':iso}
        # get all channels
        chns = self._get_unique_channels()
        # loop over each unique channel and gather data.
        for chn in chns:
            data[chn] = self._get_overall_output(chn, time)
        # pack it into json
        jdata = json.dumps(data)
        # pass data
        return jdata