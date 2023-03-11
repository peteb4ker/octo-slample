"""The sample bank.

This module contains the SampleBank class.
"""
from octo_slample.constants import DEFAULT_CHANNEL_COUNT
from octo_slample.sampler.channel import Channel


class SampleBank:
    """A bank of samples.

    The Sample Bank is a collection of
    :class:`~octo_slample.sampler.channel.Channel` s.
    Each channel contains a sample.

    The class is dict-like, so channels can be accessed by index. They are
    one-indexed, so the first channel is at index 1. To access a channels sample:

    ```
    sample = sample_bank[1].sample
    ```
    """

    def __init__(
        self,
        channel_count: int = DEFAULT_CHANNEL_COUNT,
        name: str = None,
        description: str = None,
    ):
        """Initialize the sample bank.

        Args:
            channel_count (Optional): The number of channels. Defaults to 8.
            name (Optional): The name of the sample bank. Defaults to ``None``.
                If set, only the first 8 characters will be used to conform
                to the Squid Sample format.
            description (Optional): The description of the sample bank.
                Defaults to ``None``.
        """
        self._channels = [Channel(x) for x in range(0, channel_count)]
        self.name = name
        self.description = description

    @property
    def name(self):
        """The name of the sample bank.

        :getter: Get the name.
        :setter: Set the name.
            ``new_name`` must be a ``str``.

        Returns:
            str: The name of the sample bank.
        """
        return self._name

    @name.setter
    def name(self, new_name: str):
        """Set the name of the sample bank.

        Args:
            new_name (str): The new name. Only the first 8 characters will be used.
        """
        self._name = new_name[0:8] if new_name and len(new_name) > 8 else new_name

    @property
    def description(self):
        """The description of the sample bank.

        :getter: Get the description.
        :setter: Set the description.
            ``new_description`` must be a ``str``.

        Returns:
            str: The description of the sample bank.
        """
        return self._description

    @description.setter
    def description(self, new_description: str):
        """Set the description of the sample bank.

        Args:
            new_description (str): The new description.
        """
        self._description = new_description

    def __getitem__(self, channel: int):
        """Get a channel.

        Channels are 0-indexed.

        Args:
            channel (int): The channel number.

        Returns:
            Channel: The channel.
        """
        self._validate_channel(channel)

        return self._channels[channel]

    def __len__(self):
        """Return the number of channels.

        This is a convenience method for the length of the samples list.

        Returns:
            int: The number of channels.
        """
        return len(self._channels)

    @property
    def samples(self):
        """The list of samples in the sample bank.

        :getter: Get the list of samples.
        :setter: Set the list of samples.
            ``new_samples`` must be a ``list[dict[str, str]]``.

            with the following keys:
                * ``path``: The path to the sample file. Required, may be ``None``.
                * ``name``: The name of the sample. Optional.

        Returns:
            list: A list of samples.
        """
        return [self[channel].sample for channel in range(0, len(self._channels))]

    @samples.setter
    def samples(self, new_samples: list[dict[str, str]]):
        """Set all samples.

        Args:
            samples (list|dict). A `list`` of samples.
        """
        assert len(new_samples) == len(
            self._channels
        ), "samples must be the same length as the number of channels, "
        f"but got {len(new_samples)} samples and {len(self._channels)} channels"
        assert all(
            [isinstance(sample, dict) for sample in new_samples]
        ), f"samples must be a list of dicts, but got {new_samples}"

        for channel, new_sample in enumerate(new_samples):
            self[channel].sample = new_sample["path"]
            if "name" in new_sample:
                self[channel].name = new_sample["name"]

    def _validate_channel(self, channel: int):
        """Validate a channel number.

        Channel numbers are 0-indexed.

        Args:
            channel (int): The channel number.

        Raises:
            AssertionError: If the channel number is invalid.
        """
        assert channel >= 0 and channel < len(
            self
        ), f"channel must be between 0 and {len(self) - 1}, but got {channel}"

    def __str__(self):
        """Return a string representation of the sample bank.

        Returns:
            str: A string representation of the sample bank.
        """
        return "\n".join([str(channel) for channel in self._channels])

    @property
    def channel_volumes(self) -> list[float]:
        """Get the channel volumes.

        Returns:
            list[float]: The channel volumes.
        """
        return [channel.volume for channel in self._channels]

    @channel_volumes.setter
    def channel_volumes(self, new_volumes: list[float]):
        """Set the channel volumes.

        Args:
            new_volumes (list[float]): The new channel volumes.
        """
        assert len(new_volumes) == len(
            self._channels
        ), "new_volumes must be the same length as the number of channels, "
        f"but got {len(new_volumes)} volumes and {len(self._channels)} channels"

        for channel, volume in enumerate(new_volumes):
            self[channel].volume = volume
