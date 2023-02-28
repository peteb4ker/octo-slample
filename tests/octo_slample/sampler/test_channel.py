from contextlib import nullcontext as does_not_raise

import pytest

from octo_slample.sampler.channel import Channel

DEFAULT_CHANNEL = 1
DEFAULT_SOUND = "default_sample"
AUDIO_SEGMENT = "AudioSegment"


@pytest.fixture
def audio_segment_from_wav_mock(mocker):
    a = mocker.patch("octo_slample.sampler.channel.AudioSegment.from_wav")
    a.return_value = AUDIO_SEGMENT

    return a


@pytest.fixture
def play_mock(mocker):
    return mocker.patch("octo_slample.sampler.channel.play")


@pytest.fixture
def channel_fixture(audio_segment_from_wav_mock, play_mock):
    return Channel(DEFAULT_CHANNEL, DEFAULT_SOUND)


def test_channel_init(channel_fixture):
    assert channel_fixture._number == DEFAULT_CHANNEL
    assert channel_fixture._sample == AUDIO_SEGMENT


def test_channel_init_no_sample():
    channel = Channel(DEFAULT_CHANNEL)
    assert channel._sample is None


def test_get_sample(channel_fixture):
    assert channel_fixture.sample == AUDIO_SEGMENT


def test_set_sample(channel_fixture, audio_segment_from_wav_mock):
    channel_fixture.sample = DEFAULT_SOUND
    assert audio_segment_from_wav_mock.called_once_with(DEFAULT_SOUND)
    assert channel_fixture._sample == AUDIO_SEGMENT


def test_set_sample_none_fails(channel_fixture):
    with pytest.raises(AssertionError):
        channel_fixture.sample = None


@pytest.mark.parametrize(
    "sound,expected",
    [
        (DEFAULT_SOUND, does_not_raise()),
        (None, pytest.raises(AssertionError)),
    ],
)
def test_play(channel_fixture, play_mock, sound, expected):
    if sound is None:
        channel_fixture._sample = None

    channel_fixture.play()

    if sound is not None:
        play_mock.assert_called_once_with(channel_fixture._sample)
    else:
        play_mock.assert_not_called()


def test_get_sample_path(channel_fixture):
    assert channel_fixture.sample_path == DEFAULT_SOUND


def test_str(channel_fixture):
    assert str(channel_fixture) == f"{DEFAULT_CHANNEL}: {DEFAULT_SOUND}"
