"""Clock module.

This module contains the clock function that is used to play the music.
"""


import time

from octo_slample.constants import DEFAULT_BPM, DEFAULT_STEP_COUNT, SECONDS_PER_MINUTE


class Clock:
    """The clock class.

    This class is used to iterate in time between beats.
    """

    def __init__(self, step_count: int = DEFAULT_STEP_COUNT, bpm: int = DEFAULT_BPM):
        """Initialize the clock with the given step count and beats per minute.

        The step count determines the number of steps per pattern, while BPM
        determines the speed of the clock.

        Args:
            step_count (int, optional): The number of steps per pattern.
                Defaults to `DEFAULT_STEP_COUNT`.
            bpm (int, optional): The beats per minute of the clock.
                Defaults to `DEFAULT_BPM`.
        """
        self._counter = 0
        self._step_count = step_count
        self._bpm = bpm
        self._steps_per_second = SECONDS_PER_MINUTE / bpm * self._step_count
        self._is_running = False

    def beat(self) -> None:
        """Go to the next beat of the clock.

        Wait until the next "beat" of the clock and then advance the counter.

        It uses the time.sleep() function to wait for a certain amount of time
        before advancing the counter. This is done to ensure that the clock is
        as accurate as possible.

        When the counter reaches the step count, it is reset to 0.

        Returns:
            None
        """
        if self._is_running is False:
            return self._counter

        time.sleep(
            1 / self._steps_per_second
            - time.time() * self._steps_per_second % 1 / self._steps_per_second
        )

        self._counter += 1
        if self._counter == self._step_count:
            self._counter = 0

        return self._counter

    @property
    def is_running(self) -> bool:
        """Get whether the clock is running.

        Returns:
            bool: True if the clock is running, False otherwise.
        """
        return self._is_running

    def start(self) -> None:
        """Start the clock.

        Returns:
            None
        """
        self._is_running = True

    def stop(self) -> None:
        """Stop the clock.

        Returns:
            None
        """
        self._is_running = False

    @property
    def bpm(self) -> int:
        """Get the beats per minute of the clock.

        Returns:
            int: The beats per minute of the clock.
        """
        return self._bpm
