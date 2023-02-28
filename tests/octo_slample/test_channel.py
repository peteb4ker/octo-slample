from contextlib import nullcontext as does_not_raise

import pytest

from octo_slample.channel import Channel

DEFAULT_CHANNEL = 1
DEFAULT_SOUND = "default_sample"
AUDIO_SEGMENT = "AudioSegment"


@pytest.fixture
def audio_segment_from_wav_mock(mocker):
    a = mocker.patch("octo_slample.channel.AudioSegment.from_wav")
    a.return_value = AUDIO_SEGMENT

    return a


@pytest.fixture
def play_mock(mocker):
    return mocker.patch("octo_slample.channel.play")


@pytest.fixture
def channel_fixture(audio_segment_from_wav_mock, play_mock):
    return Channel(DEFAULT_CHANNEL, DEFAULT_SOUND)


def test_channel_init(channel_fixture):
    assert channel_fixture._number == DEFAULT_CHANNEL
    assert channel_fixture._is_loop is False
    assert channel_fixture._sample == AUDIO_SEGMENT


def test_channel_init_no_sample():
    channel = Channel(DEFAULT_CHANNEL)
    assert channel._sample is None


def test_set_sample(channel_fixture, audio_segment_from_wav_mock):
    channel_fixture.set_sample(DEFAULT_SOUND)
    assert audio_segment_from_wav_mock.called_once_with(DEFAULT_SOUND)
    assert channel_fixture._sample == AUDIO_SEGMENT


def test_set_sample_none_fails(channel_fixture):
    with pytest.raises(AssertionError):
        channel_fixture.set_sample(None)


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
