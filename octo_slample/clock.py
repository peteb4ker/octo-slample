"""Clock module.

This module contains the clock function that is used to play the music.
"""
from __future__ import annotations

import time


class Clock:
    """The clock class.

    This class is used to iterate in time between beats.
    """

    def __init__(self, step_count: int = 16, division: int = 8):
        """Initialize the clock.

        TODO convert division to BPM
        """
        self._counter = 0
        self._step_count = step_count
        self._division = division

    def beat(self):
        """Go to the next beat of the clock.

        Returns:
            None
        """
        time.sleep(
            1 / self._division
            - time.time() * self._division % 1 / self._division
        )

        self._counter += 1
        if self._counter == self._step_count:
            self._counter = 0
