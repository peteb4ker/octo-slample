from __future__ import annotations

from contextlib import nullcontext as does_not_raise

import pytest

from octo_slample.pattern import Pattern
from tests.octo_slample.fixtures import BEAT_OFFBEAT_LINES
from tests.octo_slample.fixtures import BEAT_OFFBEAT_RESULT
from tests.octo_slample.fixtures import FULL_PATTERN


@pytest.fixture
def pattern_fixture():
    return Pattern()


@pytest.mark.parametrize(
    "text_pattern, expected, exception",
    [
        (
            "x   x   x   x   \n  x   x   x   x \n",
            BEAT_OFFBEAT_LINES,
            does_not_raise(),
        ),
        (
            "X   X   X   X   \n  X   X   X   X \n",
            BEAT_OFFBEAT_LINES,
            does_not_raise(),
        ),
        (
            "1234123412341234\nx   x   x   x   \n  x   x   x   x \n",
            BEAT_OFFBEAT_LINES,
            does_not_raise(),
        ),
        (
            1,
            None,
            pytest.raises(AssertionError),
        ),
    ],
)
def test_pattern_text_to_lines(
    pattern_fixture, text_pattern, expected, exception
):
    with exception:
        assert pattern_fixture._pattern_text_to_lines(text_pattern) == expected


@pytest.mark.parametrize(
    "lines, exception",
    [
        (  # 2 lines
            BEAT_OFFBEAT_LINES,
            does_not_raise(),
        ),
        (  # uppercase lines are ok
            [line.upper() for line in BEAT_OFFBEAT_LINES],
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
        (  # 9 lines
            BEAT_OFFBEAT_LINES
            + BEAT_OFFBEAT_LINES
            + BEAT_OFFBEAT_LINES
            + BEAT_OFFBEAT_LINES
            + ["x   x   x   x   "],
            pytest.raises(AssertionError),
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
        "9 lines",
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
            BEAT_OFFBEAT_RESULT,
            does_not_raise(),
        ),
        (  # uppercase lines are ok
            [line.upper() for line in BEAT_OFFBEAT_LINES],
            BEAT_OFFBEAT_RESULT,
            does_not_raise(),
        ),
        (  # 4 lines
            BEAT_OFFBEAT_LINES + BEAT_OFFBEAT_LINES,
            BEAT_OFFBEAT_RESULT + BEAT_OFFBEAT_RESULT,
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
        (  # 9 lines
            BEAT_OFFBEAT_LINES
            + BEAT_OFFBEAT_LINES
            + BEAT_OFFBEAT_LINES
            + BEAT_OFFBEAT_LINES
            + ["x   x   x   x   "],
            None,
            pytest.raises(AssertionError),
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
        "9 lines",
        "1 line with 17 characters",
    ],
)
def test_convert_lines_to_pattern(pattern_fixture, lines, expected, exception):
    with exception:
        pattern_fixture._convert_lines_to_pattern(lines)
        assert pattern_fixture._pattern == expected


def test_from_file():
    pattern = Pattern.from_file("tests/pattern.txt")

    assert isinstance(pattern, Pattern)
    assert pattern.get_pattern() is not None
    assert pattern.get_pattern() == FULL_PATTERN
