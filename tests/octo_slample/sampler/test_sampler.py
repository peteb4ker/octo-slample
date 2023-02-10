from contextlib import nullcontext as does_not_raise

import pytest

from octo_slample.constants import DEFAULT_CHANNEL_COUNT
from octo_slample.sampler.sample_bank import SampleBank
from octo_slample.sampler.sampler import Sampler


@pytest.fixture
def sampler(mock_threading_thread, mock_bank___getitem__):
    return Sampler()


@pytest.fixture
def mock_threading_thread(mocker):
    m = mocker.patch("octo_slample.sampler.sampler.threading.Thread")
    m.return_value = m

    return m


@pytest.fixture
def mock_bank___getitem__(mocker):
    return mocker.patch("octo_slample.sampler.sampler.SampleBank.__getitem__")


def test_sampler(sampler):
    assert len(sampler) == DEFAULT_CHANNEL_COUNT
    assert sampler.bank is not None
    assert isinstance(sampler._bank, SampleBank)


def test_sampler_bank_get(sampler):
    assert sampler.bank is not None
    assert isinstance(sampler.bank, SampleBank)


def test_sampler_bank_set(sampler):
    bank = SampleBank()
    sampler.bank = bank
    assert sampler.bank is bank
    assert sampler.bank is not None
    assert isinstance(sampler.bank, SampleBank)


@pytest.mark.parametrize(
    "channel,exception",
    [
        (0, pytest.raises(AssertionError)),
        (DEFAULT_CHANNEL_COUNT + 1, pytest.raises(AssertionError)),
        (None, pytest.raises(AssertionError)),
        (1, does_not_raise()),
    ],
)
def test_play_channel(
    sampler, mock_threading_thread, mock_bank___getitem__, channel, exception
):
    with (exception):
        sampler.play_channel(channel)

        mock_threading_thread.assert_called_once_with(
            target=mock_bank___getitem__(channel).play
        )
        mock_threading_thread.start.assert_called_once()
