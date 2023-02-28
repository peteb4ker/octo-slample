import pytest

from octo_slample.sampler.channel import LEFT_RIGHT_CHANNEL_COUNT, SAMPLE_WIDTH, Channel

DEFAULT_CHANNEL = 0
AUDIO_DATA = "audio_data"


@pytest.fixture
def sample_path(tmp_path):
    f = tmp_path / "sample.wav"
    f.touch()
    return f


@pytest.fixture
def sf_read_mock(mocker):
    a = mocker.patch("octo_slample.sampler.channel.sf.read")
    a.return_value = (AUDIO_DATA, 44100)

    return a


@pytest.fixture
def play_mock(mocker):
    return mocker.patch("octo_slample.sampler.channel.sa.play_buffer")


@pytest.fixture
def channel_fixture(sf_read_mock, play_mock, sample_path):
    return Channel(channel_number=DEFAULT_CHANNEL, sample_path=sample_path)


def test_channel_init(channel_fixture, sample_path):
    assert channel_fixture._number == DEFAULT_CHANNEL
    assert channel_fixture._name is None
    assert channel_fixture._sample_path == sample_path


def test_channel_init_no_sample():
    channel = Channel(DEFAULT_CHANNEL)
    assert channel._sample is None


def test_get_sample_default_is_audio_data(channel_fixture):
    assert channel_fixture.sample is not None
    assert channel_fixture.sample == AUDIO_DATA


def test_set_sample(channel_fixture, sf_read_mock, sample_path):
    channel_fixture.sample = sample_path
    assert sf_read_mock.called_once_with(sample_path)
    assert channel_fixture._sample == AUDIO_DATA


def test_set_sample_none_has_no_side_effect(channel_fixture, sf_read_mock):
    sf_read_mock.reset_mock()

    channel_fixture.sample = None

    assert channel_fixture._sample_path is None
    assert channel_fixture._sample is None

    sf_read_mock.assert_not_called()


@pytest.mark.parametrize(
    "sound",
    [
        (pytest.lazy_fixture("sample_path")),
        (None),
    ],
    ids=["valid_sample_path", "no_sample_path"],
)
def test_play(channel_fixture, play_mock, sound):
    if sound is None:
        channel_fixture._sample = None
        channel_fixture._sample_rate = None

    channel_fixture.play()

    if sound is not None:
        play_mock.assert_called_once_with(
            channel_fixture._sample,
            LEFT_RIGHT_CHANNEL_COUNT,
            SAMPLE_WIDTH,
            channel_fixture._sample_rate,
        )
    else:
        play_mock.assert_not_called()


def test_get_sample_path(channel_fixture, sample_path):
    assert channel_fixture.sample_path == sample_path


def test_str(channel_fixture, sample_path):
    assert str(channel_fixture) == f"{DEFAULT_CHANNEL + 1}: {sample_path}"
