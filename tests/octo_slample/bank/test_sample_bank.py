from contextlib import nullcontext as does_not_raise

import pytest

from octo_slample.bank.sample_bank import SampleBank
from octo_slample.channel import Channel
from octo_slample.constants import DEFAULT_CHANNEL_COUNT

SAMPLE = "sample"


@pytest.fixture
def mock_channel(mocker):
    return mocker.patch(
        "octo_slample.bank.sample_bank.Channel.sample",
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


@pytest.mark.parametrize(
    "channel, sample, exception",
    [
        (1, SAMPLE, does_not_raise()),
        (0, SAMPLE, pytest.raises(AssertionError)),
        (9, SAMPLE, pytest.raises(AssertionError)),
    ],
    ids=["channel1", "channel0", "channel9"],
)
def test_sample_bank_set_sample(sample_bank, mock_channel, channel, sample, exception):
    with exception:
        sample_bank.set_sample(channel, sample)

        mock_channel.assert_called_once_with(sample)


def test_sample_bank_set_samples_wrong_sample_count(sample_bank):
    samples = [SAMPLE] * 4

    with pytest.raises(AssertionError):
        sample_bank.samples = samples


def test_sample_bank_set_samples(sample_bank, mock_channel):
    samples = [SAMPLE] * DEFAULT_CHANNEL_COUNT

    sample_bank.samples = samples

    for channel in range(0, DEFAULT_CHANNEL_COUNT):
        mock_channel.assert_called_with(samples[channel])


@pytest.mark.parametrize(
    "channel_number, exception",
    [
        (1, does_not_raise()),
        (0, pytest.raises(AssertionError)),
        (9, pytest.raises(AssertionError)),
    ],
    ids=["channel1", "channel0", "channel9"],
)
def test_sample_bank_get_channel(sample_bank, channel_number, exception):
    with exception:
        channel = sample_bank.get_channel(channel_number)

        assert isinstance(channel, Channel)
        assert channel.number == channel_number


@pytest.mark.parametrize(
    "channel_number, exception",
    [
        (1, does_not_raise()),
        (0, pytest.raises(AssertionError)),
        (9, pytest.raises(AssertionError)),
    ],
    ids=["channel1", "channel0", "channel9"],
)
def test_sample_bank_get_sample(sample_bank, mock_channel, channel_number, exception):
    with exception:
        result = sample_bank.get_sample(channel_number)

        mock_channel.assert_called_once()
        assert result == SAMPLE


def test_channel_count(sample_bank):
    assert sample_bank.channel_count() == DEFAULT_CHANNEL_COUNT


@pytest.mark.parametrize(
    "channel_number, exception",
    [
        (1, does_not_raise()),
        (0, pytest.raises(AssertionError)),
        (9, pytest.raises(AssertionError)),
    ],
)
def test__validate_channel(sample_bank, channel_number, exception):
    with exception:
        sample_bank._validate_channel(channel_number)


def test_get_samples(sample_bank, mock_channel):
    samples = sample_bank.samples

    for _ in range(0, DEFAULT_CHANNEL_COUNT):
        mock_channel.assert_called_with()

    assert samples == [SAMPLE] * DEFAULT_CHANNEL_COUNT
