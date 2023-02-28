from contextlib import nullcontext as does_not_raise

import pytest
from schema import Schema, SchemaError

from octo_slample.json import JsonMixin
from octo_slample.pattern.json_pattern import JsonPattern
from octo_slample.pattern.pattern import Pattern
from octo_slample.pattern.text_pattern import TextPattern


@pytest.fixture
def json_pattern():
    """Get a JSON pattern."""
    return JsonPattern()


def test_json_pattern_init(json_pattern):
    """Test the JSON pattern initialization."""
    assert json_pattern is not None
    assert isinstance(json_pattern, TextPattern)
    assert isinstance(json_pattern, JsonMixin)


def test_json_pattern_schema(json_pattern):
    """Test the JSON pattern schema."""
    schema = json_pattern.schema
    assert schema is not None, "Schema is None"
    assert isinstance(schema, Schema), "Schema is not a Schema object"


@pytest.mark.parametrize(
    ("pattern", "exception"),
    [
        ("tests/fixtures/patterns/pattern.json", does_not_raise()),
        ("tests/fixtures/patterns/pattern_no_header.json", does_not_raise()),
        ("tests/fixtures/patterns/invalid/no_name.json", pytest.raises(SchemaError)),
        ("tests/fixtures/patterns/invalid/no_pattern.json", pytest.raises(SchemaError)),
    ],
    ids=["valid", "valid_no_header", "no_name", "no_pattern"],
)
def test_json_pattern_load(pattern, exception):
    with exception:
        json_pattern = JsonPattern.from_file(pattern)

        assert json_pattern is not None
        assert isinstance(json_pattern, Pattern)
