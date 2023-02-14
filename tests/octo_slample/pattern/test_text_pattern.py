from contextlib import nullcontext as does_not_raise

import pytest

from octo_slample.pattern.text_pattern import TextPattern
from tests.octo_slample.fixtures import (
    BEAT_OFFBEAT_LINES,
    BEAT_OFFBEAT_RESULT,
    EMPTY_PATTERN,
    EMPTY_RESULT,
)


@pytest.fixture
def pattern_fixture():
    return TextPattern()


@pytest.mark.parametrize(
    "lines, exception",
    [
        (  # 2 lines
            BEAT_OFFBEAT_LINES + (EMPTY_PATTERN * 6),
            does_not_raise(),
        ),
        (  # uppercase lines are ok
            [line.upper() for line in BEAT_OFFBEAT_LINES] + (EMPTY_PATTERN * 6),
            does_not_raise(),
        ),
        (  # 4 lines
            BEAT_OFFBEAT_LINES + BEAT_OFFBEAT_LINES,
            does_not_raise(),
        ),
        (  # not 'x' or ' '
            [
                "a   a   a   a  ",
            ],
            pytest.raises(AssertionError),
        ),
        (  # non-list
            1234,
            pytest.raises(AssertionError),
        ),
        (  # 8 lines
            BEAT_OFFBEAT_LINES
            + BEAT_OFFBEAT_LINES
            + BEAT_OFFBEAT_LINES
            + BEAT_OFFBEAT_LINES,
            does_not_raise(),
        ),
        (  # 1 line with 17 characters
            ["x   x   x   x    "],
            pytest.raises(AssertionError),
        ),
    ],
    ids=[
        "2 lines",
        "uppercase lines are ok",
        "4 lines",
        "not 'x' or ' '",
        "non-list",
        "8 lines",
        "1 line with 17 characters",
    ],
)
def test_validate_pattern_lines(pattern_fixture, lines, exception):
    with exception:
        pattern_fixture._validate_pattern_lines(lines)


@pytest.mark.parametrize(
    "lines, expected, exception",
    [
        (  # 2 lines
            BEAT_OFFBEAT_LINES,
            BEAT_OFFBEAT_RESULT + [EMPTY_RESULT] * 6,
            does_not_raise(),
        ),
        (  # uppercase lines are ok
            [line.upper() for line in BEAT_OFFBEAT_LINES],
            BEAT_OFFBEAT_RESULT + [EMPTY_RESULT] * 6,
            does_not_raise(),
        ),
        (  # 4 lines
            BEAT_OFFBEAT_LINES + BEAT_OFFBEAT_LINES,
            BEAT_OFFBEAT_RESULT + BEAT_OFFBEAT_RESULT + [EMPTY_RESULT] * 4,
            does_not_raise(),
        ),
        (  # not 'x' or ' '
            [
                "a   a   a   a  ",
            ],
            None,
            pytest.raises(AssertionError),
        ),
        (  # non-list
            1234,
            None,
            pytest.raises(AssertionError),
        ),
        (  # 8 lines
            BEAT_OFFBEAT_LINES
            + BEAT_OFFBEAT_LINES
            + BEAT_OFFBEAT_LINES
            + BEAT_OFFBEAT_LINES,
            BEAT_OFFBEAT_RESULT
            + BEAT_OFFBEAT_RESULT
            + BEAT_OFFBEAT_RESULT
            + BEAT_OFFBEAT_RESULT,
            does_not_raise(),
        ),
        (  # 1 line with 17 characters
            ["x   x   x   x    "],
            None,
            pytest.raises(AssertionError),
        ),
    ],
    ids=[
        "2 lines",
        "uppercase lines are ok",
        "4 lines",
        "not 'x' or ' '",
        "non-list",
        "8 lines",
        "1 line with 17 characters",
    ],
)
def test_convert_lines_to_pattern(pattern_fixture, lines, expected, exception):
    with exception:
        pattern_fixture._convert_lines_to_pattern(lines)
        assert pattern_fixture._pattern == expected


def test__build_pattern_header(pattern_fixture):
    result = pattern_fixture._build_pattern_header()
    assert result == "1   1.2 1.3 1.4 "


def test__build_pattern_header_2_bar_pattern():
    pattern_fixture = TextPattern(step_count=32)

    result = pattern_fixture._build_pattern_header()
    assert result == "1   1.2 1.3 1.4 2   2.2 2.3 2.4 "
