"""Export banks and samples to the ALM Squid Salmple format.

This module contains a class that can be used to export banks and
samples to the ALM Squid Salmple format.

Instances of
:class:`~octo_slample.sampler.channel.Channel`,
:class:`~octo_slample.sampler.sample_bank.SampleBank`
and sets of :class:`~octo_slample.sampler.sample_bank.SampleBank`
can all be exported.

Squid Sample requires WAV files to have the following spec:

- 16 bit
- 44.1 kHz
- `Set {name}` folder name (optional)
-  `Bank {n}` folder name
    -  `chan-00{x}.wav` file format
"""

from pathlib import Path

import soundfile as sf

from octo_slample.directory import DirectoryMixin
from octo_slample.sampler.channel import Channel
from octo_slample.sampler.sample_bank import SampleBank

SQUID_SALMPLE_AUDIO_FORMAT = "WAV"
SQUID_SALMPLE_WAV_SAMPLE_RATE = 44100
SQUID_SALMPLE_WAV_SUBTYPE = "PCM_16"
FFMPEG_EXPORT_PARAMS = ["-ac", "1", "-ar", "44100", "-b:a", "16"]


class WavWriter(DirectoryMixin):
    """Export banks and samples to the ALM Squid Salmple format.

    This class contains class methods that can be used to export banks
    and samples to the ALM Squid Salmple format.
    """

    @classmethod
    def build_sample_output_path(
        cls, bank_output_path: str | Path, channel_number: int
    ) -> str:
        """Build the output path for a sample.

        This method converst the channel number from a zero-based index
        to a one-based index.

        Args:
            bank_output_path (str|Path): The output path for the bank.
            channel_number (int): The channel number.

        Returns:
            str: The output path for the bank.
        """
        return str(Path(bank_output_path, f"chan-00{channel_number + 1}.wav"))

    @classmethod
    def build_bank_output_path(
        cls, set_output_path: str | Path, bank_number: int
    ) -> str:
        """Build the output path for a bank.

        Args:
            set_output_path (str|Path): The output path for the set.
            bank_number (int): The bank number.

        Returns:
            str: The output path for the bank.
        """
        return str(Path(set_output_path, f"Bank {bank_number}"))

    @classmethod
    def write_channel(
        cls, channel: Channel, bank_output_path: str | Path
    ) -> str | ValueError:
        """Export the sample to 16-bit, 44.1kHz WAV file.

        This method converts the sample into the audio format required
        by the ALM Squid Salmple.

        Args:
            channel (Channel): The channel to export.
            bank_output_path (str|Path): The output path to write the sample to.

        Returns:
            str: The path to the exported file, or ValueError if the
                channel has no sample.
        """
        assert isinstance(
            channel, Channel
        ), f"channel must be a Channel. Got a {type(channel)}"
        assert isinstance(
            bank_output_path, (str, Path)
        ), "bank_output_path must be a string or Path"

        if channel.sample is None:
            return ValueError(f"Channel {channel} has no sample to export")

        full_path = cls.build_sample_output_path(bank_output_path, channel.number)
        cls.create_directory(bank_output_path)

        sf.write(
            full_path,
            channel.sample,
            SQUID_SALMPLE_WAV_SAMPLE_RATE,
            subtype=SQUID_SALMPLE_WAV_SUBTYPE,
            format=SQUID_SALMPLE_AUDIO_FORMAT,
        )

        return full_path

    @classmethod
    def write_bank(
        cls, bank: SampleBank, bank_number: int, set_output_path: str | Path
    ) -> list[str | ValueError]:
        """Export the bank to the ALM Squid Salmple format.

        The bank will be exported to a folder named `Bank {n}` within
        the `set_output_path` where `n` is the bank number.

        Args:
            bank (SampleBank): The sample bank to export.
            bank_number (int): The bank number.
            set_output_path (str): The output path to write the set to.

        Returns:
            list[str]: A list of paths of the exported files.
        """
        assert isinstance(bank, SampleBank), "bank must be a SampleBank"
        assert bank_number >= 1, "bank_number must be 1 or greater"
        assert isinstance(
            set_output_path, (str, Path)
        ), "set_output_path must be a string or Path"

        bank_output_path = cls.build_bank_output_path(set_output_path, bank_number)

        cls.create_directory(bank_output_path)

        output_paths = [
            cls.write_channel(channel, bank_output_path) for channel in bank._channels
        ]

        return output_paths
