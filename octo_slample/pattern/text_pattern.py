"""Text-based pattern class.

This class is used to create a pattern from a list of text strings.
"""
from octo_slample.constants import (
    BEATS_PER_BAR,
    DEFAULT_CHANNEL_COUNT,
    DEFAULT_STEP_COUNT,
    SIXTEENTHS_PER_BAR,
)
from octo_slample.pattern.pattern import Pattern

VALID_PATTERN_CHARS = [" ", "x", "X", "."]


class TextPattern(Pattern):
    """Text-based pattern class.

    This class is used to create a pattern from a list of text strings.
    """

    def __init__(
        self,
        channel_count: int = DEFAULT_CHANNEL_COUNT,
        step_count: int = DEFAULT_STEP_COUNT,
    ):
        """Initialize the pattern.

        Args:
            text (str): The pattern text.
            channel_count (int): The number of channels. Defaults to 8.
            step_count (int): The number of steps. Defaults to 16.

        Returns:
            None
        """
        super().__init__(channel_count, step_count)

    def _validate_pattern_lines(self, lines: list[str]) -> None:
        """Validate the pattern lines.

        Args:
            lines (list[str]): The lines to validate.

        Raises:
            AssertionError: If the lines are invalid.
        """
        assert isinstance(lines, list), "Invalid pattern. Expected a list."

        # Make sure there are up to 8 lines.
        assert len(lines) <= len(
            self
        ), f"Invalid number of lines. Expected 8 lines but got {len(lines)}."

        # Make sure each line is n characters long.
        for index, line in enumerate(lines):
            assert len(line) <= len(self), (
                f"Invalid line length. Expected up to {len(self)} characters per line "
                + f"but got {len(line)} characters on line {index + 1}."
            )

            for char in line:
                assert char in VALID_PATTERN_CHARS, (
                    "Invalid character in pattern. Expected one of "
                    + f"[{''.join(VALID_PATTERN_CHARS)}] but got {char}."
                )

    @Pattern.pattern.setter
    def pattern(self, pattern: list[str]) -> None:
        """Set the pattern.

        Args:
            pattern (list[str]): The pattern.

        Returns:
            None
        """
        self._convert_lines_to_pattern(pattern)

    def _convert_lines_to_pattern(self, lines: list[str]) -> None:
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
            for idx_j, char in enumerate(line.ljust(len(self), ".")):
                self._pattern[idx_i][idx_j] = char.lower() == "x"

    def __str__(self) -> str:
        """Get the pattern as a string.

        Returns:
            The pattern as a string.
        """
        pattern_string = f"  {self._build_pattern_header()}\n"
        for idx, channel in enumerate(self._pattern):
            pattern_string += (
                f"{idx} " + "".join(["x" if step else "." for step in channel]) + "\n"
            )

        return pattern_string

    def _build_pattern_header(self) -> str:
        """Get the pattern header.

        The pattern header has the following format:

            1   1.1  1.2  1.3  2   2.1  2.2  2.3

        Returns:
            The pattern header.
        """
        pattern_header = ""
        pattern_length = len(self.pattern[0])

        for bar in range(0, pattern_length // SIXTEENTHS_PER_BAR):
            for step in range(0, BEATS_PER_BAR):
                pattern_header += (
                    f"{bar + 1}{'.' + str(step + 1) if step > 0 else '  '} "
                )

        return pattern_header
