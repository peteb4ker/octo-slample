"""A class for loading and storing a pattern.

This module contains the Pattern class that is used to load and store a pattern
from a file.

The file format is as follows:
1. The first line is th 16th notes and is ignored.
2. Lines 2-9 are the 8 channels.
3. Each channel line is 16 characters long.
4. Each character is either a space or an X.
5. An X indicates that the channel should be played on that beat.
6. A space indicates that the channel should not be played on that beat.

Example (this pattern uses the first 4 channels only):

    1234123412341234
    x   x   x   x
    x x   x
    x x x x x x x x
        x       x

This pattern would play the first channel on every beat, the second
channel on beats 4, 6, and 9, the third channel on every odd beat, and
the fourth channel on beats 5 and 13.

The pattern is stored in a list of lists. The outer list is the 8
channels. The inner list is the 16 beats. Each beat is a boolean
indicating whether or not the channel should be played on that beat.

"""
from __future__ import annotations

import os

STEP_COUNT = 16
PATTERN_HEADER = "1234123412341234"
STEP_RANGE = range(1, STEP_COUNT + 1)
VALID_PATTERN_CHARS = [" ", "x", "X", "."]


class Pattern:
    """16-step, multi-channel pattern.

    This class is used to load and store a pattern.
    """

    def __init__(self, channel_count: int = 8):
        """Initialize the pattern.

        Args:
            channel_count (Optional): The number of channels. Defaults to 8.
        """
        self._reset_pattern(channel_count)

    def set_pattern(self, text_pattern: str):
        """Set the pattern.

        The pattern is stored in a list of lists. The outer list is the 8
        channels. The inner list is the 16 beats. Each beat is a boolean
        indicating whether or not the channel should be played on that beat.

        Args:
            pattern: The pattern.
        """
        lines = self._pattern_text_to_lines(text_pattern)
        self._convert_lines_to_pattern(lines)

    def _pattern_text_to_lines(self, text_pattern: str):
        """Convert the pattern text to a list of lines.

        Args:
            text_pattern (str): The pattern text.

        Returns:
            The pattern lines.

        Raises:
            AssertionError: If the pattern is invalid.
        """
        assert isinstance(text_pattern, str), "Pattern must be a string."

        pattern_lines = text_pattern.splitlines()

        # remove the pattern header if it exists.
        if pattern_lines[0] == PATTERN_HEADER:
            pattern_lines.pop(0)

        # convert to lowercase and return
        return [line.lower() for line in pattern_lines]

    def _validate_pattern_lines(self, lines: list[str]):
        """Validate the pattern lines.

        Args:
            lines (list[str]): The lines to validate.

        Raises:
            AssertionError: If the lines are invalid.
        """
        assert isinstance(lines, list), "Invalid pattern. Expected a list."

        # Make sure there are up to 8 lines.
        assert len(lines) <= 8, "Invalid number of lines. Expected 8 lines."

        # Make sure each line is 16 characters long.
        for index, line in enumerate(lines):
            assert len(line) <= 16, (
                "Invalid line length. Expected up to 16 characters per line "
                + f"but got {len(line)} characters on line {index + 1}."
            )

            for char in line:
                assert char in VALID_PATTERN_CHARS, (
                    "Invalid character in pattern. Expected "
                    + "{' '.join(VALID_PATTERN_CHARS)} but got {char}."
                )

    def _reset_pattern(self, channel_count: int):
        """Reset the pattern.

        Args:
            channel_count (int): The number of channels.

        Raises:
            AssertionError: If the channel count is invalid.
        """
        assert isinstance(
            channel_count, int
        ), "Invalid channel count. Expected an integer."
        assert (
            1 <= channel_count
        ), "Invalid channel count. Expected a positive integer."

        self._pattern = [[False] * STEP_COUNT for _ in range(0, channel_count)]

    def _convert_lines_to_pattern(self, lines: list[str]):
        """Convert the lines to a pattern.

        If any of the lines are less than 16 characters long, they will be
        padded with spaces on the left to make their length 16.

        Args:
            lines (list[str]): The lines to convert.

        Raises:
            AssertionError: If the lines are invalid.
        """
        self._validate_pattern_lines(lines)

        for idx_i, line in enumerate(lines):
            for idx_j, char in enumerate(line.ljust(STEP_COUNT, ".")):
                self._pattern[idx_i][idx_j] = char.lower() == "x"

    def get_channel_count(self) -> int:
        """Get the number of channels.

        Channels are 1-indexed.

        Returns:
            The number of channels.
        """
        return len(self._pattern) + 1

    def load(self, file_path):
        """Load a pattern from a file.

        Args:
            file_path: The path to the file.

        Raises:
            AssertionError: If the file is invalid.
        """
        assert os.path.isfile(file_path)

        with open(file_path, "r") as f:
            lines = f.read()

        self.set_pattern(lines)

    def get_pattern(self):
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
        assert 1 <= channel <= self.get_channel_count(), (
            f"Invalid channel. Expected 1-{self.get_channel_count()} "
            + f"but got {channel}."
        )
        assert (
            1 <= step <= STEP_COUNT
        ), f"Invalid step. Expected 1-{STEP_COUNT} but got {step}."

        return self._pattern[channel - 1][step - 1]

    @classmethod
    def from_file(cls, file: str):
        """Load a pattern from a file.

        Create a new instance of the class and loads the pattern from the
        file.

        Args:
            file: The path to the file.

        Returns:
            The pattern.
        """
        pattern = Pattern()
        pattern.load(file)
        return pattern

    def _pattern_to_string(self) -> str:
        """Get the pattern as a string.

        Returns:
            The pattern as a string.
        """
        pattern_string = "  " + PATTERN_HEADER + "\n"
        for idx, channel in enumerate(self._pattern):
            pattern_string += (
                f"{idx} "
                + "".join(["x" if step else "." for step in channel])
                + "\n"
            )

        return pattern_string

    def __str__(self):
        """Get the pattern as a string.

        Returns:
            The pattern as a string.
        """
        return self._pattern_to_string()
