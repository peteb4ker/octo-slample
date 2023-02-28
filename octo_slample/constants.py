"""Constants for the Octo Slample project.

This module contains constants for the Octo Slample project. These
constants are used throughout the project to ensure consistency and to
avoid magic numbers.
"""
DEFAULT_BPM = 120
DEFAULT_CHANNEL_COUNT = 8
SECONDS_PER_MINUTE = 60
DEFAULT_STEP_COUNT = 16

SQUID_SALMPLE_FILE_TEMPLATE = "chan-00{0}.wav"
SQUID_SALMPLE_AUDIO_FORMAT = "wav"
FFMPEG_EXPORT_PARAMS = ["-ac", "1", "-ar", "44100", "-b:a", "16"]
