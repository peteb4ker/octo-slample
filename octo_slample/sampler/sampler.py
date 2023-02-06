"""8-channel virtual sampler.

This module contains the Sampler class.
"""


import threading

from octo_slample.bank.sample_bank import SampleBank
from octo_slample.constants import DEFAULT_CHANNEL_COUNT


class Sampler:
    """Multi-channel virtual sampler.

    Defaults to 8 channels.

    This implementation does not support patterns or looping playback
    and is intended as a base class for other implementations and for
    one-shot playback.
    """

    def __init__(self, channel_count: int = DEFAULT_CHANNEL_COUNT):
        """Initialize the sampler.

        Creates the sampler pattern and sample bank.
        """
        self._bank = SampleBank(channel_count)

    @property
    def bank(self):
        """Get the sample bank.

        Returns:
            SampleBank: The sample bank.
        """
        return self._bank

    @bank.setter
    def bank(self, bank):
        """Set the sample bank.

        Args:
            bank (SampleBank): The sample bank.
        """
        assert isinstance(bank, SampleBank), "bank must be a SampleBank"
        self._bank = bank

    def play_channel(self, channel: int):
        """Play a channel.

        This method is non-blocking.

        Channels are 1-indexed.
        """
        assert channel > 0
        assert channel <= self.channel_count()

        x = threading.Thread(target=self.bank.get_channel(channel).play)
        x.start()

    def channel_count(self):
        """Return the number of channels.

        This is a convenience method for the length of the channels list.

        Returns:
            int: The number of channels.
        """
        return self.bank.channel_count()
