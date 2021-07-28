"""Use this module to compute the signals and create the payload for the mqtt pipeline"""

__all__ = [
    "Technician",
]

# import own libs
from transmitter.engine.generator import Generator
from transmitter.auxiliary.exceptions import (
    InvalidInputTypeError,
    InvalidInputValueError,
)

# import native libs
from datetime import datetime
from typing import Dict, Optional
import json


class Technician:
    """Class to manage multiple generator instances at once."""

    def __init__(self, generators_: Optional[Dict] = None):
        """Pass the Technician a dict of all generators (and their ids) he needs to take care of."""

        if generators_ is None:
            self.generators = {}
        else:
            self.generators = generators_

        self._check_input()

    def _check_input(self):
        """ Check the given input data for type."""
        if not isinstance(self.generators, dict):
            raise InvalidInputTypeError(
                "The parameter generators_ is type %s but should be a of type dict."
                % type(self.generators)
            )
        if not all(isinstance(gen, Generator) for key, gen in self.generators.items()):
            raise InvalidInputValueError(
                "Not all values of generators are an instance of "
                "class transmitter.engine.generator."
            )

    def _get_overall_output(self, name_, time_=None):
        """Get the combined output of all generators.

        Parameters:
        :param name_: (Mandatory, string) Name of channel that the data should be extracted from.
        :param time_: (Optional, datetime) Timestamp that the data should be extracted from.
        """
        if not time_:
            time = datetime.now()
        else:
            time = time_

        return sum(
            [
                gen.get_data(time)
                for key, gen in self.generators.items()
                if gen.name == name_
            ]
        )

    def _get_unique_channels(self):
        """Extract the unique channel names since multiple generators can output on the same channel (name)."""
        return list(set([gen.name for key, gen in self.generators.items()]))

    def get_payload(self) -> str:
        """
        Gather the data of all generators and pack it into a nice json.
        :return: current payload.
        """
        # get current time.
        time = datetime.now()
        iso = time.isoformat()
        # create payload template
        data = {"timestamp": iso}
        # get all channels
        chns = self._get_unique_channels()
        # loop over each unique channel and gather data.
        for chn in chns:
            data[chn] = self._get_overall_output(chn, time)
        return json.dumps(data)
