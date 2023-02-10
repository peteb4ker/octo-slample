"""LoopingSampler class."""

from __future__ import annotations

from octo_slample.bank.sample_bank import SampleBank
from octo_slample.clock import Clock
from octo_slample.constants import (
    DEFAULT_BPM,
    DEFAULT_CHANNEL_COUNT,
    DEFAULT_STEP_COUNT,
)
from octo_slample.json_pattern_bank import JsonPatternBank
from octo_slample.pattern import Pattern
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
        bank: SampleBank = None,
    ):
        """Initialize the sampler.

        Args:
            channel_count (int): The number of channels. Defaults to 8.
            bpm (int): The beats per minute.    Defaults to 120.
            pattern (Pattern): The pattern to play.  Defaults to None.
            bank (SampleBank): (Optional) The sample bank.  Defaults to None.
                If not provided, a new empty bank will be created.
        """
        super().__init__(channel_count)

        self._clock = Clock(bpm=bpm)
        self._pattern = pattern
        if bank is not None:
            self.bank = bank

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
        while self.clock.is_running:
            self._play_pattern()

    def _play_pattern(self) -> None:
        """Plays the entire pattern, one step at a time.

        Upon playing each channel, the clock beat is advanced.

        Returns:
            None
        """
        assert self._pattern, "pattern must be set before playing"

        for step in range(1, DEFAULT_STEP_COUNT + 1):
            for channel in range(1, len(self) + 1):
                if self.pattern.is_step_set(channel, step):
                    self.play_channel(channel)

            self.clock.beat()

    @property
    def clock(self) -> Clock:
        """Get the clock.

        Returns:
            Clock: The clock.
        """
        return self._clock

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
        return cls(bpm=bpm, pattern=pattern_bank.pattern, bank=pattern_bank.bank)
