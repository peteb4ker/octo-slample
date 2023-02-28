from contextlib import nullcontext as does_not_raise

import pytest

from octo_slample.constants import DEFAULT_CHANNEL_COUNT
from octo_slample.sampler.channel import Channel
from octo_slample.sampler.sample_bank import SampleBank

SAMPLE = "sample"
SAMPLE_DICT = {"name": "foo", "path": SAMPLE}


@pytest.fixture
def mock_channel(mocker):
    return mocker.patch(
        "octo_slample.sampler.sample_bank.Channel.sample",
        new_callable=mocker.PropertyMock,
        return_value=SAMPLE,
    )


@pytest.fixture
def sample_bank():
    return SampleBank()


def test_sample_bank_default_args(sample_bank):
    assert len(sample_bank._channels) == DEFAULT_CHANNEL_COUNT

    for channel in range(0, DEFAULT_CHANNEL_COUNT):
        assert isinstance(sample_bank._channels[channel], Channel)


def test_sample_bank_custom_channel_count():
    sample_bank = SampleBank(4)

    assert len(sample_bank._channels) == 4

    for channel in range(0, 4):
        assert isinstance(sample_bank._channels[channel], Channel)


def test_sample_bank_set_samples_wrong_sample_count(sample_bank):
    samples = [SAMPLE_DICT] * 4

    with pytest.raises(AssertionError):
        sample_bank.samples = samples


def test_sample_bank_set_samples(sample_bank, mock_channel):
    samples = [SAMPLE_DICT] * DEFAULT_CHANNEL_COUNT

    sample_bank.samples = samples

    for channel in range(0, DEFAULT_CHANNEL_COUNT):

        mock_channel.assert_called_with(SAMPLE_DICT["path"])


@pytest.mark.parametrize(
    "channel_number, exception",
    [
        (0, does_not_raise()),
        (-1, pytest.raises(AssertionError)),
        (9, pytest.raises(AssertionError)),
    ],
    ids=["valid", "negative", "too high"],
)
def test_sample_bank__getitem__(sample_bank, channel_number, exception):
    with exception:
        channel = sample_bank[channel_number]

        assert isinstance(channel, Channel)
        assert channel.number == channel_number


def test_sample_bank_len(sample_bank):
    assert len(sample_bank) == DEFAULT_CHANNEL_COUNT


@pytest.mark.parametrize(
    "channel_number, exception",
    [
        (0, does_not_raise()),
        (-1, pytest.raises(AssertionError)),
        (9, pytest.raises(AssertionError)),
    ],
    ids=["valid", "negative", "too high"],
)
def test__validate_channel(sample_bank, channel_number, exception):
    with exception:
        sample_bank._validate_channel(channel_number)


def test_get_samples(sample_bank, mock_channel):
    samples = sample_bank.samples

    for _ in range(0, DEFAULT_CHANNEL_COUNT):
        mock_channel.assert_called()

    assert samples == [SAMPLE] * DEFAULT_CHANNEL_COUNT


def test_get_channel_volumes(sample_bank):
    volumes = sample_bank.channel_volumes

    assert isinstance(volumes, list)
    assert len(volumes) == DEFAULT_CHANNEL_COUNT
    assert volumes == [0.0] * DEFAULT_CHANNEL_COUNT
