"""LoopingSampler class."""

from __future__ import annotations

from octo_slample.clock import Clock
from octo_slample.constants import (
    DEFAULT_BPM,
    DEFAULT_CHANNEL_COUNT,
    DEFAULT_STEP_COUNT,
)
from octo_slample.pattern import Pattern
from octo_slample.pattern.json_pattern_bank import JsonPatternBank
from octo_slample.sampler.sampler import Sampler


class LoopingSampler(Sampler):
    """A sampler that plays a pattern in a loop.

    This implementation supports patterns and looping playback.
    """

    def __init__(
        self,
        channel_count: int = DEFAULT_CHANNEL_COUNT,
        bpm: int = DEFAULT_BPM,
        pattern: Pattern = None,
    ):
        """Initialize the sampler.

        Args:
            channel_count (int): The number of channels. Defaults to 8.
            bpm (int): The beats per minute.    Defaults to 120.
            pattern (Pattern): The pattern to play.  Defaults to None.
        """
        super().__init__(channel_count)

        self._clock = Clock(bpm=bpm)
        self._pattern = pattern

    @property
    def pattern(self) -> Pattern:
        """Get the pattern.

        Returns:
            Pattern: The pattern.
        """
        return self._pattern

    @pattern.setter
    def pattern(self, pattern: Pattern) -> None:
        """Set the pattern to play.

        Args:
            pattern (Pattern): The pattern to play.

        Returns:
            None
        """
        assert isinstance(pattern, Pattern), "pattern must be a Pattern"
        self._pattern = pattern

    def loop(self) -> None:
        """Play the pattern in a loop.

        Returns:
            None
        """
        assert self._pattern, "pattern must be set before playing"

        while True:
            for step in range(1, DEFAULT_STEP_COUNT + 1):
                for channel in range(1, self.channel_count() + 1):
                    if self._pattern.is_step_set(channel, step):
                        self.play_channel(channel)

                self._clock.beat()

    @classmethod
    def from_pattern_file(cls, filename: str, bpm: int = DEFAULT_BPM) -> LoopingSampler:
        """Create a sampler from a pattern file.

        Args:
            filename (str): The path to the pattern file.

        Returns:
            LoopingSampler: The sampler.
        """
        if not filename.endswith(".json"):
            raise NotImplementedError("Only JSON pattern files are supported")

        pattern_bank = JsonPatternBank.from_file(filename)

        sampler = cls(bpm=bpm)
        sampler.pattern(pattern_bank.pattern)
        sampler.bank(pattern_bank.bank)

        return sampler
