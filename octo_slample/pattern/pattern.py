"""Pattern module.

This module contains the Pattern class.
"""

from collections.abc import Sequence

from octo_slample.constants import DEFAULT_CHANNEL_COUNT, DEFAULT_STEP_COUNT


class Pattern:
    """16-step, multi-channel pattern.

    This class is used to load and store a pattern.
    """

    def __init__(
        self,
        channel_count: int = DEFAULT_CHANNEL_COUNT,
        step_count: int = DEFAULT_STEP_COUNT,
    ):
        """Initialize the pattern.

        Args:
            channel_count (Optional): The number of channels. Defaults to 8.
            step_count (Optional): The number of steps. Defaults to 16.
        """
        self.reset(channel_count, step_count)

    def reset(
        self,
        channel_count: int = DEFAULT_CHANNEL_COUNT,
        step_count: int = DEFAULT_STEP_COUNT,
    ):
        """Reset the pattern.

        Args:
            channel_count (int): The number of channels. Defaults to 8.

        Raises:
            AssertionError: If the channel count is invalid.
        """
        assert isinstance(
            channel_count, int
        ), f"Invalid channel count. Expected an integer but got {type(channel_count)}."
        assert (
            0 < channel_count
        ), f"Channel must be a positive integer, but got {channel_count}."

        self._pattern = [[False] * step_count for _ in range(0, channel_count)]
        self._channel_volumes = [0] * channel_count

    def __len__(self) -> int:
        """Get the pattern length.

        Returns:
            The number of steps in the pattern.
        """
        return len(self._pattern[0])

    def channel_count(self) -> int:
        """Get the number of channels.

        Returns:
            The number of channels.
        """
        return len(self._pattern)

    def __getitem__(self, channel: int) -> list:
        """Get the pattern for the given channel.

        Channels are 0-indexed.

        Args:
            channel: The channel. 0-7.

        Returns:
            The pattern for the given channel.
        """
        self.__validate_channel_number(channel)

        return self._pattern[channel]

    @property
    def pattern(self) -> list[list[bool]]:
        """Get the pattern.

        The pattern is stored in a list of lists. The outer list is the 8
        channels. The inner list is the 16 beats. Each beat is a boolean
        indicating whether or not the channel should be played on that beat.

        Returns:
            The pattern.
        """
        return self._pattern

    def is_step_set(self, channel: int, step: int) -> bool:
        """Get the step for the given channel.

        Channels are 0-indexed.

        Steps are 0-indexed.

        Returns True if the channel should be played on the step, False
        otherwise.

        Args:
            channel: The channel. 0-7.
            step: The step. 0-n.

        Returns:
            True if the channel should be played on the step, False otherwise.
        """
        self.__validate_channel_number(channel)

        assert (
            0 <= step < len(self)
        ), f"Invalid step. Expected 0-{len(self)-1} but got {step}."

        return self._pattern[channel][step]

    def __validate_channel_number(self, channel: int):
        """Validate the channel number.

        Args:
            channel (int): The channel number.

        Raises:
            AssertionError: If the channel number is invalid.
        """
        assert isinstance(
            channel, int
        ), f"Invalid channel number. Expected an integer but got {type(channel)}."
        assert 0 <= channel < self.channel_count(), (
            f"Invalid channel. Expected 0-{self.channel_count()-1} "
            + f"but got {channel}."
        )

    @property
    def channel_volumes(self) -> Sequence[float]:
        """Get the volumes for each channel.

        Returns:
            The volumes for each channel. 0-1.
        """
        return self._channel_volumes

    @channel_volumes.setter
    def channel_volumes(self, volumes: list[float | int]) -> None:
        """Set the volumes for each channel.

        Args:
            volumes (list[float | int]): The volumes for each channel. 0-1.

        Raises:
            AssertionError: If the volumes are invalid.
        """
        assert isinstance(
            volumes, list
        ), f"Invalid volumes. Expected a list but got {type(volumes)}."

        assert len(volumes) == self.channel_count(), (
            f"Invalid volumes. Expected {self.channel_count()} "
            + f"volumes but got {len(volumes)}."
        )

        self._channel_volumes = [float(volume) for volume in volumes]
