"""A class to represent a channel on the OctoSlample.

This module contains the Channel class that is used to represent a
channel on the OctoSlample.
"""
from pathlib import Path

import numpy as np
import simpleaudio as sa
import soundfile as sf

LEFT_RIGHT_CHANNEL_COUNT = 2
SAMPLE_WIDTH = 2


class Channel:
    """A class to represent a channel on the OctoSlample."""

    def __init__(
        self,
        channel_number: int,
        name: str | None = None,
        sample_path: str | None = None,
        volume: float = 0,
    ):
        """Initialize the channel.

        Args:
            channel_number (int): The channel number.
                Zero-indexed.
            name (str): The channel's name. Optional.
                This is a convenience attribute for the user to
                identify the instrument of the voice.  This is not
                used by the Squid Salmple but helps to coordinate creating
                :class:`~octo_slample.sampler.sample_bank.SampleBank`
                and :class:`~octo_slample.pattern.Pattern` objects.
            sample_path (str): Path to the channel's sample. Optional.
                If provided, the sample will be loaded and the
                :class:`~octo_slample.sampler.channel.Channel` will be
                ready to play.
            volume (float): The channel's volume in decibels. Optional.
                Defaults to 0.
        """
        self.number = channel_number
        self.name = name
        self.volume = volume

        if sample_path is not None:
            self.sample = sample_path
        else:
            self._sample = None
            self._sample_path = None

    def play(self) -> None:
        """Play the channel's sound."""
        if self._sample is not None:
            sa.play_buffer(
                self._sample, LEFT_RIGHT_CHANNEL_COUNT, SAMPLE_WIDTH, self._sample_rate
            )

    @property
    def name(self) -> str | None:
        """Return the channel's name.

        Returns:
            str: The channel's name.
        """
        return self._name

    @name.setter
    def name(self, name: str | None) -> None:
        """Set the channel's name.

        Args:
            name (str): The channel's name.
                May be ``None``.

        Returns:
            None
        """
        self._name = name

    @property
    def number(self) -> int:
        """Return the channel's number.

        Returns:
            int: The channel's number.
        """
        return self._number

    @number.setter
    def number(self, number: int) -> None:
        """Set the channel's number.

        Args:
            number (int): The channel's number.

        Returns:
            None
        """
        assert isinstance(number, int), "number must be an int"

        self._number = number

    @property
    def volume(self) -> float:
        """Return the channel's volume in decibels.

        Returns:
            float: The channel's volume in decibels.
        """
        return self._volume

    @volume.setter
    def volume(self, volume: float) -> None:
        """Set the channel's volume in decibels.

        Args:
            volume (float): The channel's volume in decibels.

        Returns:
            None
        """
        assert isinstance(volume, (int, float)), "volume_db must be an int or float"

        self._volume = float(volume)

        if hasattr(self, "_original_sample"):
            # apply the new volume
            self._sample = self.apply_audio_volume(self._original_sample, volume)

    def __str__(self) -> str:
        """Return the channel's number.

        This method is used to print the channel's number.

        Returns:
            str: The channel's number.
        """
        if self.name:
            return f"{self.number + 1}: {self.name.rjust(10)} {self.sample_path}"
        else:
            return f"{self.number + 1}: {self.sample_path}"

    @property
    def sample(self) -> np.ndarray:
        """Return the channel's sample.

        Returns:
            str: The channel's sample.
        """
        return self._sample

    @sample.setter
    def sample(self, sample_path: str | None) -> None:
        """Set the channel's sample.

        This method will load the sample from the provided path and
        apply the channel's volume to the sample.

        Args:
            sample_path (str|None): The path to the sample.
                May be ``None`` to clear the sample.

        Returns:
            None
        """
        self._sample_path = sample_path

        if sample_path is None:
            self._sample = None
            return

        assert Path(sample_path).exists(), f"Sample {sample_path} does not exist"

        # read the sample
        (audio, sample_rate) = sf.read(sample_path, dtype="int16")

        self._original_sample = audio
        self._sample_rate = sample_rate

        # apply the new volume
        self._sample = self.apply_audio_volume(self._original_sample, self._volume)

    @classmethod
    def db_to_percent(self, db) -> float:
        """Convert decibels to a percentage.

        Args:
            db (float): The decibels to convert.

        Returns:
            float: The percentage.
        """
        return 10 ** (db / 10)

    def apply_audio_volume(self, audio: np.ndarray, volume: float) -> np.ndarray:
        """Apply the channel's volume to the audio.

        Args:
            audio (np.ndarray): The audio to apply the volume to.
            volume (float): The volume to apply.

        Returns:
            np.ndarray: The audio with the volume applied.
        """
        return (np.copy(audio) * self.db_to_percent(volume)).astype(np.int16)

    @property
    def sample_path(self) -> str | None:
        """Return the channel's sample path.

        Returns:
            str: The channel's sample path.
        """
        return self._sample_path
