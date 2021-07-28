"""Use this module to generate multiple signals"""

__all__ = [
    "Generator",
]

# import own libs
from transmitter.auxiliary.constants import VALID_SIGNAL_TYPES
from transmitter.auxiliary.exceptions import (
    InvalidInputTypeError,
    InvalidInputValueError,
    SeedReplantError,
)

# import 3rd party libs
import numpy as np

# import native libs
from datetime import datetime
from typing import Optional


class Generator:
    """
    Class to compute current value of an initialized channel.
    """

    def __init__(
        self,
        name_,
        frequency_=0.1,
        type_="sin",
        dead_frequency_=1,
        dead_period_=0,
        limits_=None,
        replay_data_=None,
        seed_=None,
    ):
        # init parameters for this instance
        self.name = name_  # name of current channel
        self.frequency = frequency_  # frequency in that the data will repeat itself
        self.type = type_  # type of data generation. default is sin.
        self.dead_frequency = (
            dead_frequency_  # frequency in that the channels output will drop to zero
        )
        self.dead_period = dead_period_  # period (in seconds) of dead time
        self.limits = limits_  # lower/upper limits of data
        self.replay_data = replay_data_  # data to replay
        self.seed = seed_  # random number seed

        # indexing for replay of data
        self.replay_idx = 0
        self.basetime = datetime.now()
        self._check_input()

        if self.seed:
            self._plant_a_seed()

    def _check_input(self):
        """
        Check the given input data for type.
        """
        if not isinstance(self.name, str):
            raise InvalidInputTypeError(
                "Content of name_ is type %s but should be a of type string."
                % type(self.name)
            )

        if not isinstance(self.frequency, (int, float)):
            raise InvalidInputTypeError(
                "Content of frequency_ is type %s but should be a of type int or float."
                % type(self.frequency)
            )
        if self.frequency <= 0:
            raise InvalidInputValueError(
                "Value of frequency_ is negative (%s) but should be positive."
                % str(self.frequency)
            )

        if not isinstance(self.type, str):
            raise InvalidInputTypeError(
                "Content of type_ is type %s but should be a of type string."
                % type(self.type)
            )
        if self.type not in VALID_SIGNAL_TYPES:
            raise InvalidInputValueError(
                "Value of type_ (%s) is not valid." % str(self.type)
            )

        if not isinstance(self.dead_frequency, (int, float)):
            raise InvalidInputTypeError(
                "Content of dead_frequency_ is type %s but should be a of type int or float."
                % type(self.dead_frequency)
            )
        if self.dead_frequency <= 0:
            raise InvalidInputValueError(
                "Value of dead_frequency_ is negative (%s) but should be positive."
                % str(self.dead_frequency)
            )

        if not isinstance(self.dead_period, (int, float)):
            raise InvalidInputTypeError(
                "Content of dead_period_ is type %s but should be a of type int or float."
                % type(self.dead_period)
            )
        if self.dead_period < 0:
            raise InvalidInputValueError(
                "Value of dead_period_ is negative (%s) but should be zero or positive."
                % str(self.dead_period)
            )

        if self.limits:
            if not isinstance(self.limits, list):
                raise InvalidInputTypeError(
                    "Content of limits_ is type %s but should be a of type list."
                    % type(self.limits)
                )
            if not all(isinstance(x, (int, float)) for x in self.limits):
                raise InvalidInputValueError(
                    "Not all values of limits are of type int or float."
                )

        if self.replay_data:
            if not isinstance(self.replay_data, list):
                raise InvalidInputTypeError(
                    "Content of data_ is type %s but should be of type list."
                    % type(self.replay_data)
                )

        if self.seed:
            if not isinstance(self.seed, int):
                raise InvalidInputTypeError(
                    "Content of seed_ is type %s but should be a of type int."
                    % type(self.seed)
                )

    def get_data(self, current_datetime: Optional[datetime] = None):
        """
        Get the data including the noise.

        :param current_datetime: (optional, datetime) Use given timestamp of initialization of generator.
        """
        seconds = self._seconds_since_init(current_datetime)

        if seconds % (1 / self.dead_frequency) < self.dead_period:
            return 0
        else:
            if self.type == "sin":
                # get current position in radiant degree
                x = (
                    2
                    * np.pi
                    * ((seconds % (1 / self.frequency)) / (1 / self.frequency))
                )
                # compute y and rescale it
                yr = np.sin(x)
            elif self.type == "random":
                yr = np.random.rand()
            elif self.type == "fixed":
                yr = 1
            elif self.type == "replay":
                # take sample
                yr = self.replay_data[self.replay_idx]
                self.replay_idx += 1
                # reset replay idx
                if self.replay_idx == len(self.replay_data):
                    self.replay_idx = 0
            else:
                raise InvalidInputTypeError("Given channel_type is unknown.")

            if self.limits:
                return self._rescale(yr)
            else:
                return yr

    def _seconds_since_init(self, current_datetime: Optional[datetime] = None):
        """
        Get seconds since init of this class.

        :param current_datetime: (optional, datetime) Use given timestamp of initialization of generator.
        """
        if not current_datetime:
            current_datetime = datetime.now()

        dt = current_datetime - self.basetime
        seconds = dt.seconds + dt.microseconds / 1e6
        return seconds

    def _rescale(self, value: float):
        """
        Rescale value to new scale.

        Parameters:
        value_ (mandatory, float): Value to rescale.

        Note:
        - Old scale is fixed to be [-1, 1]
        """
        max_value = np.max(self.limits)
        min_value = np.min(self.limits)
        return ((max_value - min_value) / (1 - (-1))) * (value - (-1)) + min_value

    def _plant_a_seed(self, seed: Optional[int] = None):
        """
        Set (or reset) a seed to the random noise generator.

        :param seed: (optional, int) Seed to use for random generators.
        """
        if seed:
            np.random.seed(seed)
        else:
            # replant seed from init
            if self.seed:
                np.random.seed(self.seed)
            else:
                # someone fucked up.
                raise SeedReplantError(
                    "Replanting of seed is not possible, "
                    "since no seed has ever been planted before!"
                )
