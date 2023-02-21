from contextlib import nullcontext as does_not_raise

import pytest
from schema import Schema, SchemaError

from octo_slample.json import JsonMixin
from octo_slample.sampler.json_sample_bank import JsonSampleBank
from octo_slample.sampler.sample_bank import SampleBank


@pytest.fixture
def json_sample_bank():
    """Get a JSON sample bank."""
    return JsonSampleBank()


def test_json_sample_bank_init(json_sample_bank):
    """Test the JSON sample bank initialization."""
    assert json_sample_bank is not None
    assert isinstance(json_sample_bank, SampleBank)
    assert isinstance(json_sample_bank, JsonMixin)


def test_json_sample_bank_schema(json_sample_bank):
    """Test the JSON pattern bank schema."""
    schema = json_sample_bank.schema()
    assert schema is not None, "Schema is None"
    assert isinstance(schema, Schema), "Schema is not a Schema object"


@pytest.mark.parametrize(
    ("pattern", "exception"),
    [
        ("banks/sample_bank.json", does_not_raise()),
        (
            "banks/invalid/no_name.json",
            pytest.raises(SchemaError),
        ),
        (
            "banks/invalid/no_samples.json",
            pytest.raises(SchemaError),
        ),
    ],
    ids=["valid", "no_name", "no_samples"],
)
def test_json_sample_bank_load(pattern, exception):
    with exception:
        json_sample_bank = JsonSampleBank.from_file(pattern)

        assert json_sample_bank is not None
        assert isinstance(json_sample_bank, SampleBank)
