"""Pattern module.

This module contains the Pattern class.
"""

from octo_slample.constants import DEFAULT_CHANNEL_COUNT, DEFAULT_STEP_COUNT


class Pattern:
    """16-step, multi-channel pattern.

    This class is used to load and store a pattern.
    """

    def __init__(self, channel_count: int = DEFAULT_CHANNEL_COUNT):
        """Initialize the pattern.

        Args:
            channel_count (Optional): The number of channels. Defaults to 8.
        """
        self.reset(channel_count)

    def reset(self, channel_count: int = DEFAULT_CHANNEL_COUNT):
        """Reset the pattern.

        Args:
            channel_count (int): The number of channels. Defaults to 8.

        Raises:
            AssertionError: If the channel count is invalid.
        """
        self.__validate_channel_number(channel_count - 1)

        self._pattern = [[False] * DEFAULT_STEP_COUNT for _ in range(0, channel_count)]

    def __len__(self) -> int:
        """Get the pattern length.

        Returns:
            The number of steps in the pattern.
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
    def pattern(self):
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
            step: The step. 0-15.

        Returns:
            True if the channel should be played on the step, False otherwise.
        """
        self.__validate_channel_number(channel)

        assert (
            0 <= step < DEFAULT_STEP_COUNT
        ), f"Invalid step. Expected 0-{DEFAULT_STEP_COUNT-1} but got {step}."

        return self._pattern[channel][step]

    def __validate_channel_number(self, channel: int):
        """Validate the channel number.

        Args:
            channel (int): The channel number.

        Raises:
            AssertionError: If the channel number is invalid.
        """
        assert isinstance(channel, int), (
            "Invalid channel number. Expected an integer but got " + f"{type(channel)}."
        )
        assert 0 <= channel < DEFAULT_CHANNEL_COUNT, (
            f"Invalid channel. Expected 0-{DEFAULT_CHANNEL_COUNT-1} "
            + f"but got {channel}."
        )
