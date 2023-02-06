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
        self._channels[channel - 1].set_sample(sample)

    def set_samples(self, samples: list[str]):
        """Set all samples.

        Args:
            samples (list): A list of samples.
        """
        assert len(samples) == len(self._channels)

        for channel in range(1, len(samples) + 1):
            self.set_sample(channel, samples[channel - 1])

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

        return self._channels[channel - 1].get_sample()

    def channel_count(self):
        """Return the number of channels.

        This is a convenience method for the length of the samples list.

        Returns:
            int: The number of channels.
        """
        return len(self._channels)

    def get_samples(self):
        """Get all samples.

        Returns:
            list: A list of samples.
        """
        return self._samples

    def _validate_channel(self, channel: int):
        """Validate a channel number.

        Args:
            channel (int): The channel number.

        Raises:
            AssertionError: If the channel number is invalid.
        """
        assert channel > 0, "Channel must be greater than 0"
        assert (
            channel <= self.channel_count()
        ), "Channel must be less than or equal to the number of channels"
