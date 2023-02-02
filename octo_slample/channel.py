from __future__ import annotations

from pydub import AudioSegment
from pydub.playback import play


class Channel:
    """A class to represent a channel on the OctoSlample."""

    def __init__(self, name: int, sound: str = None, one_shot: bool = False):
        self.name = name
        self.one_shot = one_shot
        if sound:
            self.set_sound(sound)

    def play(self):
        """Play the channel's sound."""
        play(self.sound)

    def __str__(self):
        """Return the channel's name."""
        return self.name

    def __repr__(self):
        """Return the channel's name."""
        return self.name

    def set_sound(self, sound: str):
        """Set the channel's sound."""
        self.sound = AudioSegment.from_wav(sound)


if __name__ == "__main__":
    for x in range(1, 9):
        channel = Channel(x, f"wavs/chan-00{x}.wav")
        channel.play()
