"""The sample bank.

This module contains the SampleBank class.
"""
from octo_slample.channel import Channel
from octo_slample.constants import DEFAULT_CHANNEL_COUNT


class SampleBank:
    """A bank of samples."""

    def __init__(self, channel_count: int = DEFAULT_CHANNEL_COUNT):
        """Initialize the sample bank.

        Args:
            channel_count (Optional): The number of channels. Defaults to 8.
        """
        self._channels = [Channel(x) for x in range(1, channel_count + 1)]

    def set_sample(self, channel: int, sample: str):
        """Set a channel's sample.

        Channels are 1-indexed.

        Args:
            channel (int): The channel number.
            sample (str): The path to the sample.
        """
        self._validate_channel(channel)
        self._channels[channel - 1].sample = sample

    def get_channel(self, channel: int):
        """Get a channel.

        Channels are 1-indexed.

        Args:
            channel (int): The channel number.

        Returns:
            Channel: The channel.
        """
        self._validate_channel(channel)

        return self._channels[channel - 1]

    def get_sample(self, channel: int):
        """Get a channel's sample.

        Channels are 1-indexed.

        Args:
            channel (int): The channel number.

        Returns:
            str: The path to the sample.
        """
        self._validate_channel(channel)

        return self._channels[channel - 1].sample

    def __len__(self):
        """Return the number of channels.

        This is a convenience method for the length of the samples list.

        Returns:
            int: The number of channels.
        """
        return len(self._channels)

    @property
    def samples(self):
        """Get all samples.

        Returns:
            list: A list of samples.
        """
        return [
            self.get_sample(channel) for channel in range(1, len(self._channels) + 1)
        ]

    @samples.setter
    def samples(self, new_samples: list[str]):
        """Set all samples.

        Args:
            samples (list): A list of samples.
        """
        assert len(new_samples) == len(self._channels)

        for channel in range(1, len(self._channels) + 1):
            self.set_sample(channel, new_samples[channel - 1])

    def _validate_channel(self, channel: int):
        """Validate a channel number.

        Args:
            channel (int): The channel number.

        Raises:
            AssertionError: If the channel number is invalid.
        """
        assert channel > 0, "Channel must be greater than 0"
        assert channel <= len(
            self
        ), "Channel must be less than or equal to the number of channels"

    def __str__(self):
        """Return a string representation of the sample bank.

        Returns:
            str: A string representation of the sample bank.
        """
        return "\n".join([str(channel) for channel in self._channels])
