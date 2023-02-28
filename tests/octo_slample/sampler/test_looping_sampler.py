import pytest

from octo_slample.bank.sample_bank import SampleBank
from octo_slample.clock import Clock
from octo_slample.constants import (
    DEFAULT_BPM,
    DEFAULT_CHANNEL_COUNT,
    DEFAULT_STEP_COUNT,
)
from octo_slample.json_pattern_bank import JsonPatternBank
from octo_slample.pattern import Pattern
from octo_slample.sampler.looping_sampler import LoopingSampler


@pytest.fixture
def looping_sampler(mock_sampler_play_channel) -> LoopingSampler:
    return LoopingSampler()


@pytest.fixture
def mock_sampler_play_channel(mocker):
    return mocker.patch("octo_slample.sampler.sampler.Sampler.play_channel")


@pytest.fixture
def mock_clock_beat(mocker):
    return mocker.patch("octo_slample.clock.Clock.beat")


@pytest.fixture
def pattern():
    """Create a pattern with every other step set to true."""
    p = Pattern()
    p._pattern = [
        [_ % 2 == 0] * DEFAULT_STEP_COUNT for _ in range(0, DEFAULT_STEP_COUNT)
    ]

    return p


@pytest.fixture
def mock_play_pattern(mocker):
    return mocker.patch(
        "octo_slample.sampler.looping_sampler.LoopingSampler._play_pattern"
    )


@pytest.fixture
def mock_clock_is_running(mocker):
    """Mocks a clock that runs for 4 beats and then stops."""

    return mocker.patch(
        "octo_slample.clock.Clock.is_running",
        new_callable=mocker.PropertyMock,
        side_effect=[True, True, True, True, False],
    )


@pytest.fixture
def mock_json_pattern_bank_from_file(mocker):
    m = mocker.patch("octo_slample.json_pattern_bank.JsonPatternBank.from_file")

    jpb = mocker.MagicMock(spec=JsonPatternBank)
    jpb.bank = mocker.MagicMock(spec=SampleBank)
    jpb.pattern = mocker.MagicMock(spec=Pattern)

    m.return_value = jpb

    return m


def test_looping_sampler(looping_sampler) -> None:
    assert isinstance(looping_sampler, LoopingSampler)

    assert len(looping_sampler) == DEFAULT_CHANNEL_COUNT

    assert isinstance(looping_sampler.clock, Clock)
    assert looping_sampler.clock.bpm == DEFAULT_BPM

    assert looping_sampler.pattern is None
    assert looping_sampler.bank is not None


def test_looping_sampler_pattern() -> None:
    pattern = Pattern()

    looping_sampler = LoopingSampler(pattern=pattern)
    looping_sampler._pattern = pattern
    assert looping_sampler.pattern is pattern


def test_looping_sampler_bank() -> None:
    bank = SampleBank()
    looping_sampler = LoopingSampler(bank=bank)

    assert looping_sampler.bank is bank


def test_looping_sampler_custom_bpm() -> None:
    bpm = 123

    looping_sampler = LoopingSampler(bpm=bpm)
    assert looping_sampler.clock.bpm == bpm


def test_pattern_(looping_sampler) -> None:
    pattern = Pattern()

    looping_sampler._pattern = pattern
    assert looping_sampler.pattern is pattern


def test_pattern_set(looping_sampler) -> None:
    pattern = Pattern()
    looping_sampler.pattern = pattern
    assert looping_sampler.pattern is pattern


def test_play_pattern_no_pattern_set(looping_sampler):
    with pytest.raises(AssertionError):
        looping_sampler._play_pattern()


def test_play_pattern(
    looping_sampler, pattern, mock_sampler_play_channel, mock_clock_beat
) -> None:
    looping_sampler.pattern = pattern
    looping_sampler.bank = SampleBank()

    looping_sampler._play_pattern()

    assert (
        mock_sampler_play_channel.call_count
        == (DEFAULT_STEP_COUNT * DEFAULT_CHANNEL_COUNT) / 2
    )
    assert mock_clock_beat.call_count == DEFAULT_STEP_COUNT


def test_loop_not_running(looping_sampler, mock_play_pattern) -> None:
    looping_sampler.clock.stop()
    looping_sampler.loop()

    assert not mock_play_pattern.called


def test_loop_running(
    looping_sampler, mock_play_pattern, mock_clock_is_running
) -> None:
    looping_sampler.clock.start()
    looping_sampler.loop()

    assert mock_play_pattern.call_count == 4
    assert mock_clock_is_running.call_count == 5


def test_from_pattern_file(mock_json_pattern_bank_from_file) -> None:
    looping_sampler = LoopingSampler.from_pattern_file(
        "tests/patterns/test_pattern.json"
    )

    assert isinstance(looping_sampler, LoopingSampler)

    mock_json_pattern_bank_from_file.assert_called_once_with(
        "tests/patterns/test_pattern.json"
    )

    assert isinstance(looping_sampler.pattern, Pattern)
    assert isinstance(looping_sampler.bank, SampleBank)


def test_from_non_json_pattern_file() -> None:
    with pytest.raises(NotImplementedError):
        LoopingSampler.from_pattern_file("tests/patterns/test_pattern.txt")
