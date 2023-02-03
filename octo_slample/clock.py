"""Clock module.

This module contains the clock function that is used to play the music.
"""
from __future__ import annotations

import time

from octo_slample.sampler import Sampler

DIVISION = 8
NOTES = 16


def clock(sampler: Sampler):
    """Sampler clock.

    This function is used to play the music.

    Args:
        sampler (Sampler): The sampler to play the music on.

    Returns:
        None
    """
    counter = 0

    while counter < 60 * DIVISION:
        print(counter)
        time.sleep(1 / DIVISION - time.time() * DIVISION % 1 / DIVISION)

        if counter % 4 == 0:
            sampler.play_channel(1)

        if counter % 8 == 0:
            sampler.play_channel(3)

        sampler.play_channel(4)

        counter += 1
        if counter == NOTES:
            counter = 0
