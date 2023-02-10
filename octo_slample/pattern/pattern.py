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
        self.reset_pattern(channel_count)

    def reset_pattern(self, channel_count: int = DEFAULT_CHANNEL_COUNT):
        """Reset the pattern.

        Args:
            channel_count (int): The number of channels. Defaults to 8.

        Raises:
            AssertionError: If the channel count is invalid.
        """
        self.__validate_channel_number(channel_count)

        self._pattern = [[False] * DEFAULT_STEP_COUNT for _ in range(0, channel_count)]

    def __len__(self) -> int:
        """Get the pattern length.

        Returns:
            The number of steps in the pattern.
        """
        return len(self._pattern)

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

        Returns True if the channel should be played on the step, False
        otherwise.

        Args:
            channel: The channel. 1-8.
            step: The step. 1-16.

        Returns:
            True if the channel should be played on the step, False otherwise.
        """
        self.__validate_channel_number(channel)

        assert (
            1 <= step <= DEFAULT_STEP_COUNT
        ), f"Invalid step. Expected 1-{DEFAULT_STEP_COUNT} but got {step}."

        return self._pattern[channel - 1][step - 1]

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
        assert 1 <= channel <= DEFAULT_CHANNEL_COUNT, (
            f"Invalid channel. Expected 1-{DEFAULT_CHANNEL_COUNT} "
            + f"but got {channel}."
        )
