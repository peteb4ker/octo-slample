"""8-channel virtual sampler.

This module contains the Sampler class.
"""


import threading

from octo_slample.constants import DEFAULT_CHANNEL_COUNT
from octo_slample.sampler.sample_bank import SampleBank


class Sampler:
    """Multi-channel virtual sampler.

    Defaults to 8 channels.

    This implementation does not support patterns or looping playback
    and is intended as a base class for other implementations and for
    one-shot playback.

    Channels are 1-indexed to match the Squid Salmple's channel numbering.

    To play a channel, call the `play_channel` method with the channel
    number as an argument.

    The `SampleBank` object is dict-like, so channels can be accessed
    by index. They are one-indexed, so the first channel is at index 1.
    To access a channels sample:

    ```
    sample = sampler.bank[1].sample
    ```

    To get the number of channels, call `len(sampler)`.
    """

    def __init__(self, channel_count: int = DEFAULT_CHANNEL_COUNT):
        """Initialize the sampler.

        Creates the sampler pattern and sample bank.

        Args:
            channel_count (Optional): The number of channels. Defaults to 8.
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
        assert isinstance(channel, int), "channel must be an int"
        assert channel > 0 and channel <= len(
            self
        ), f"channel must be in range 1-{len(self)}"

        x = threading.Thread(target=self.bank[channel].play)
        x.start()

    def __len__(self):
        """Return the number of channels.

        This is a convenience method for the length of the channels list.

        Returns:
            int: The number of channels.
        """
        return len(self.bank)
