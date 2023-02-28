from contextlib import nullcontext as does_not_raise

import pytest
from schema import Schema, SchemaError

from octo_slample.json_pattern_bank import JsonPatternBank
from octo_slample.pattern.text_pattern import TextPattern
from octo_slample.sampler.sample_bank import SampleBank


@pytest.fixture
def json_pattern_bank():
    """Get a JSON pattern bank."""
    return JsonPatternBank()


def test_json_pattern_bank_init(json_pattern_bank):
    """Test the JSON pattern bank initialization."""
    assert json_pattern_bank is not None
    assert isinstance(json_pattern_bank, JsonPatternBank)


def test_json_pattern_bank_schema(json_pattern_bank):
    """Test the JSON pattern bank schema."""
    schema = json_pattern_bank.schema
    assert schema is not None, "Schema is None"
    assert isinstance(schema, Schema), "Schema is not a Schema object"


@pytest.mark.parametrize(
    ("pattern", "exception"),
    [
        ("patterns/pattern_bank.json", does_not_raise()),
        ("patterns/pattern_bank_no_header.json", does_not_raise()),
        ("patterns/invalid_patterns/no_name.json", pytest.raises(SchemaError)),
        ("patterns/invalid_patterns/no_pattern.json", pytest.raises(SchemaError)),
        ("patterns/invalid_patterns/no_samples.json", pytest.raises(SchemaError)),
    ],
    ids=["valid", "valid_no_header", "no_name", "no_pattern", "no_samples"],
)
def test_json_pattern_bank_load(pattern, exception):
    with exception:
        json_pattern_bank = JsonPatternBank.from_file(pattern)

        assert json_pattern_bank.pattern is not None
        assert isinstance(json_pattern_bank.pattern, TextPattern)

        assert json_pattern_bank.bank is not None
        assert isinstance(json_pattern_bank.bank, SampleBank)
