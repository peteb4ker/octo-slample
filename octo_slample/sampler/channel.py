"""A class to represent a channel on the OctoSlample.

This module contains the Channel class that is used to represent a
channel on the OctoSlample.
"""
from pathlib import Path

import simpleaudio as sa
import soundfile as sf

LEFT_RIGHT_CHANNEL_COUNT = 2
SAMPLE_WIDTH = 2


class Channel:
    """A class to represent a channel on the OctoSlample."""

    def __init__(self, channel_number: int, name: str = None, sample_path: str = None):
        """Initialize the channel.

        Args:
            channel_number (int): The channel number.
                Zero-indexed.
            name (str): The channel's name. Optional.
                This is a convenience attribute for the user to
                identify the instrument of the voice.  This is not
                used by the Squid Salmple but helps to coordinate creating
                :class:`~octo_slample.sampler.sample_bank.SampleBank`
                and :class:`~octo_slample.pattern.Pattern` objects.
            sample_path (str): Path to the channel's sample. Optional.
        """
        self.number = channel_number
        self.name = name

        if sample_path is not None:
            self.sample = sample_path
        else:
            self._sample = None
            self._sample_path = None

    def play(self):
        """Play the channel's sound."""
        if self._sample is not None:
            sa.play_buffer(
                self._sample, LEFT_RIGHT_CHANNEL_COUNT, SAMPLE_WIDTH, self._sample_rate
            )

    @property
    def name(self):
        """Return the channel's name.

        Returns:
            str: The channel's name.
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Set the channel's name.

        Args:
            name (str): The channel's name.

        Returns:
            None
        """
        self._name = name

    @property
    def number(self):
        """Return the channel's number.

        Returns:
            int: The channel's number.
        """
        return self._number

    @number.setter
    def number(self, number: int):
        """Set the channel's number.

        Args:
            number (int): The channel's number.

        Returns:
            None
        """
        assert isinstance(number, int), "number must be an int"

        self._number = number

    def __str__(self):
        """Return the channel's number.

        This method is used to print the channel's number.

        Returns:
            str: The channel's number.
        """
        if self.name:
            return f"{self.number + 1}: {self.name.rjust(10)} {self.sample_path}"
        else:
            return f"{self.number + 1}: {self.sample_path}"

    @property
    def sample(self):
        """Return the channel's sample.

        Returns:
            str: The channel's sample.
        """
        return self._sample

    @sample.setter
    def sample(self, sample_path: str):
        """Set the channel's sound.

        Args:
            sample_path (str): The path to the sample.

        Returns:
            None
        """
        self._sample_path = sample_path

        if sample_path is None:
            self._sample = None
            return

        assert Path(sample_path).exists(), f"Sample {sample_path} does not exist"

        (self._sample, self._sample_rate) = sf.read(self._sample_path, dtype="int16")

    @property
    def sample_path(self):
        """Return the channel's sample path.

        Returns:
            str: The channel's sample path.
        """
        return self._sample_path
