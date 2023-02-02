from __future__ import annotations

from octo_slample.channel import Channel

CHANNEL_COUNT = 8


class Sampler:
    """8-channel virtual sampler."""

    def __init__(self):
        self.channels = []

        for x in range(1, CHANNEL_COUNT + 1):
            self.channels.append(Channel(x))

    def set_sound(self, channel: int, sound: str):
        """Set a channel's sound.

        Channels are 1-indexed."""
        assert channel > 0
        assert channel <= CHANNEL_COUNT

        self.channels[channel - 1].set_sound(sound)

    def play_channel(self, channel: int):
        """Play a channel.

        Channels are 1-indexed."""
        assert channel > 0
        assert channel <= CHANNEL_COUNT

        self.channels[channel - 1].play()


if __name__ == "__main__":
    sampler = Sampler()

    for x in range(1, CHANNEL_COUNT + 1):
        sampler.set_sound(x, f"wavs/chan-00{x}.wav")

    for x in range(1, CHANNEL_COUNT + 1):
        sampler.play_channel(x)
