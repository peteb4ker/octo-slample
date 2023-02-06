import pytest

from octo_slample.clock import Clock
from octo_slample.constants import DEFAULT_BPM, DEFAULT_STEP_COUNT, SECONDS_PER_MINUTE

TIME = 1234567890


@pytest.fixture
def clock():
    return Clock()


@pytest.fixture
def mock_sleep(mocker):
    return mocker.patch("octo_slample.clock.time.sleep")


@pytest.fixture
def mock_time(mocker):
    m = mocker.patch("octo_slample.clock.time.time")
    m.return_value = TIME

    return m


def test_clock_default_args(clock):
    assert clock._counter == 0
    assert clock._step_count == DEFAULT_STEP_COUNT
    assert clock._bpm == DEFAULT_BPM
    assert (
        clock._steps_per_second == SECONDS_PER_MINUTE / DEFAULT_BPM * DEFAULT_STEP_COUNT
    )


def test_clock_custom_args():
    clock = Clock(4, 120)

    assert clock._counter == 0
    assert clock._step_count == 4
    assert clock._bpm == 120
    assert clock._steps_per_second == SECONDS_PER_MINUTE / 120 * 4


def test_clock_beat(clock, mock_sleep, mock_time):
    counter = clock.beat()

    assert counter == 1
    mock_time.assert_called_once()
    mock_sleep.assert_called_once_with(0.125)


def test_clock_beat_reset(clock, mock_sleep, mock_time):
    for idx in range(0, DEFAULT_STEP_COUNT + 1):
        counter = clock.beat()

        assert counter == (idx + 1) % DEFAULT_STEP_COUNT
