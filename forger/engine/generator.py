"""Use this module to interact with the Generator class. This class is the fundamental block to generate a signal."""

__all__ = [
    "Generator",
]

# import native libs
from datetime import datetime
from typing import List, Optional

# import 3rd party libs
import numpy as np

# import own libs
from forger.auxiliary.enums import ChannelTypes
from forger.auxiliary.exceptions import InvalidInputTypeError, SeedReplantError


class Generator:
    """
    Class to compute current value of an initialized channel.
    """

    def __init__(
        self,
        name: str,
        frequency: float,
        channel_type: str,
        dead_frequency: float,
        dead_period: float,
        scale: Optional[List],
        replay_data: Optional[List],
        seed: Optional[int] = None,
    ):
        """
        Initialize a new Generator instance.
        Besides setting the given variables, also make sure a seed is planted, replay_idx is reset and base_time is set.
        """
        # init parameters for this instance
        self.name = name  # name of current channel
        self.frequency = frequency  # frequency in that the data will repeat itself
        self.channel_type = (
            channel_type.lower()
        )  # type of data generation. make sure its lowercase string.
        self.dead_frequency = (
            dead_frequency  # frequency in that the channels output will drop to zero
        )
        self.dead_period = dead_period  # period (in seconds) of dead time
        self.scale = scale  # desired lower/upper limits of data
        self.limits = [-1, 1]
        self.replay_data = replay_data  # data to replay

        # indexing for replay of data
        self.replay_idx = 0
        self.base_time = datetime.now()
        self.seed = np.abs(seed) if seed is not None else None

        if self.seed:
            self._plant_a_seed()

        if self.replay_data:
            self.limits = [np.min(self.replay_data), np.max(self.replay_data)]

    def get_data(self, current_datetime: Optional[datetime] = None):
        """
        Get the data including the noise.

        :param current_datetime: Use given timestamp of initialization of generator.
        """
        seconds = self._seconds_since_init(current_datetime)

        if (self.dead_frequency != 0) and (
            seconds % (1 / self.dead_frequency) < self.dead_period
        ):
            return 0.0
        else:
            if self.channel_type in ChannelTypes.SIN.value:
                # get current position in radiant degree
                x = (
                    2
                    * np.pi
                    * ((seconds % (1 / self.frequency)) / (1 / self.frequency))
                )
                yr = np.sin(x)
            elif self.channel_type in ChannelTypes.RANDOM.value:
                yr = np.random.rand()
            elif self.channel_type in ChannelTypes.FIXED.value:
                yr = 1.0
            elif self.channel_type in ChannelTypes.REPLAY.value:
                # take sample
                yr = self.replay_data[self.replay_idx]
                self.replay_idx += 1
                # reset replay idx
                if self.replay_idx == len(self.replay_data):
                    self.replay_idx = 0
            else:
                raise InvalidInputTypeError(
                    f"Given channel_type ({self.channel_type}) is not implemented."
                )

            if self.scale:
                return self._rescale(yr)
            else:
                return yr

    def _seconds_since_init(self, current_datetime: Optional[datetime] = None) -> float:
        """
        Get seconds since init of this class.

        :param current_datetime: Use given timestamp of initialization of generator.
        :return: Seconds since init of class
        """
        if not current_datetime:
            current_datetime = datetime.now()

        dt = current_datetime - self.base_time
        seconds = dt.seconds + dt.microseconds / 1e6
        return seconds

    def _rescale(self, value: float) -> float:
        """
        Rescale value to new scale.

        :param value: Value to rescale.
        :return: Rescaled value.

        Note:
        - It is assumed that unscaled data is between [-1, 1]
        """
        max_scale = np.max(self.scale)
        min_scale = np.min(self.scale)
        max_limit = np.max(self.limits)
        min_limit = np.min(self.limits)

        return ((max_scale - min_scale) / (max_limit - min_limit)) * (
            value - min_limit
        ) + min_scale

    def _plant_a_seed(self, seed: Optional[int] = None):
        """
        Set (or reset) a seed to the random noise generator.
        Note that if negative integer is passed as seed, its absolute value is used.
        :param seed: Seed to use for random generators.
        """
        if seed:
            np.random.seed(np.abs(seed))
        else:
            if self.seed:
                np.random.seed(self.seed)
            else:
                raise SeedReplantError(
                    "Replanting of seed is not possible, "
                    "since no seed has ever been planted before!"
                )
