"""A class to represent a channel on the OctoSlample.

This module contains the Channel class that is used to represent a
channel on the OctoSlample.
"""


from pydub import AudioSegment
from pydub.playback import play

from octo_slample.constants import (
    FFMPEG_EXPORT_PARAMS,
    SQUID_SALMPLE_AUDIO_FORMAT,
    SQUID_SALMPLE_FILE_TEMPLATE,
)


class Channel:
    """A class to represent a channel on the OctoSlample."""

    def __init__(self, channel_number: int, sample: str = None):
        """Initialize the channel.

        Args:
            channel_number (int): The channel's name.
            sample (str): The channel's sample.
        """
        assert isinstance(channel_number, int), "channel_number must be an int"

        self._number = channel_number
        if sample is not None:
            self.sample = sample
        else:
            self._sample = None

    def play(self):
        """Play the channel's sound."""
        if self._sample is not None:
            play(self._sample)

    @property
    def number(self):
        """Return the channel's number.

        Returns:
            int: The channel's number.
        """
        return self._number

    def __str__(self):
        """Return the channel's number.

        This method is used to print the channel's number.

        Returns:
            str: The channel's number.
        """
        return f"{self.number}: {self.sample_path}"

    @property
    def sample(self):
        """Return the channel's sample.

        Returns:
            str: The channel's sample.
        """
        return self._sample

    @sample.setter
    def sample(self, sample_path: str):
        """Set the channel's sound.

        Args:
            sample_path (str): The path to the sample.

        Returns:
            None
        """
        assert isinstance(sample_path, str), "sample_path must be a string"

        self._sample = AudioSegment.from_wav(sample_path)
        self._sample_path = sample_path

    @property
    def sample_path(self):
        """Return the channel's sample path.

        Returns:
            str: The channel's sample path.
        """
        return self._sample_path

    def export(self) -> None:
        """Export the sample to 16-bit, 44.1kHz WAV file.

        This method converts the sample into the audio format required
        by the ALM Squid Salmple.
        """
        self.sample.export(
            SQUID_SALMPLE_FILE_TEMPLATE.format(self.number),
            format=SQUID_SALMPLE_AUDIO_FORMAT,
            parameters=FFMPEG_EXPORT_PARAMS,
        )