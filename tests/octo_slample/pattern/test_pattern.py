from contextlib import nullcontext as does_not_raise

import pytest

from octo_slample.constants import DEFAULT_CHANNEL_COUNT, DEFAULT_STEP_COUNT
from octo_slample.pattern.pattern import Pattern


@pytest.fixture
def pattern_fixture():
    return Pattern()


def test_pattern_init(pattern_fixture):
    p = pattern_fixture.pattern

    assert (
        len(p) == DEFAULT_CHANNEL_COUNT
    ), f"Pattern should have {DEFAULT_CHANNEL_COUNT} channels"
    for channel in p:
        assert len(channel) == DEFAULT_STEP_COUNT, "Channel should have 16 steps"
        for step in channel:
            assert step is False


def test_pattern_init_negative_channel_count_fails():
    with pytest.raises(AssertionError):
        Pattern(-1)


def test_reset_negative_channel_count_fails(pattern_fixture):
    with pytest.raises(AssertionError):
        pattern_fixture.reset(-1)


def test_reset_initializes_empty_pattern(pattern_fixture):
    pattern_fixture._pattern[0][0] = True
    pattern_fixture.reset()
    p = pattern_fixture.pattern

    assert len(p) == DEFAULT_CHANNEL_COUNT
    for channel in p:
        assert len(channel) == DEFAULT_STEP_COUNT
        for step in channel:
            assert step is False


def test_channel_count_default(pattern_fixture):
    assert pattern_fixture.channel_count() == DEFAULT_CHANNEL_COUNT


def test_channel_count_custom(pattern_fixture):
    pattern_fixture.reset(channel_count=3)
    assert pattern_fixture.channel_count() == 3


def test_pattern_property_getter(pattern_fixture):
    p = pattern_fixture.pattern

    assert p == pattern_fixture._pattern


def test_is_step_set(pattern_fixture):
    pattern_fixture._pattern[0][0] = True
    assert pattern_fixture.is_step_set(0, 0) is True


def test_is_step_set_negative_channel_fails(pattern_fixture):
    with pytest.raises(AssertionError):
        pattern_fixture.is_step_set(-1, 1)


def test__getitem__(pattern_fixture):
    assert pattern_fixture[0] == pattern_fixture._pattern[0]


def test_channel_volumes__get(pattern_fixture):
    assert pattern_fixture.channel_volumes == pattern_fixture._channel_volumes


@pytest.mark.parametrize(
    "channel_volumes,exception",
    [
        ([1, 2, 3, 4, 5, 6, 7, 8], does_not_raise()),
        ([1, 2, 3], pytest.raises(AssertionError)),
    ],
    ids=["valid", "invalid"],
)
def test_channel_volumes__set(pattern_fixture, channel_volumes, exception):
    with exception:
        pattern_fixture.channel_volumes = channel_volumes
        assert pattern_fixture.channel_volumes == channel_volumes
