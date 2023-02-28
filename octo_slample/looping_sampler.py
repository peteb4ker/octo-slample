"""LoopingSampler class."""
from __future__ import annotations

from octo_slample.clock import Clock
from octo_slample.pattern import Pattern
from octo_slample.sampler import Sampler


class LoopingSampler(Sampler):
    """A sampler that plays a pattern in a loop."""

    def __init__(self):
        """Initialize the sampler."""
        super().__init__()

        self._clock = Clock()

    def set_pattern(self, pattern: Pattern) -> None:
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
            for step in range(1, 17):
                for channel in range(1, 9):
                    if self._pattern.is_step_set(channel, step):
                        self.play_channel(channel)

                self._clock.beat()

    @classmethod
    def from_pattern_file(cls, filename: str) -> LoopingSampler:
        """Create a sampler from a pattern file.

        Args:
            filename (str): The path to the pattern file.

        Returns:
            LoopingSampler: The sampler.
        """
        sampler = cls()
        sampler.set_pattern(Pattern.from_file(filename))

        return sampler
