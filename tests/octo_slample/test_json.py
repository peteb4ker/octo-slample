import pytest

from octo_slample.json import JsonMixin


@pytest.fixture
def json_mixin(mocker):
    """Get a JSON mixin."""
    mocker.patch.multiple(JsonMixin, __abstractmethods__=set())

    return JsonMixin()


def test_json_mixin_has_schema_method(json_mixin):
    assert hasattr(json_mixin, "schema")

    json_mixin.schema()


def test_json_mixin_has__load_method(json_mixin):
    assert hasattr(json_mixin, "_load")

    json_mixin._load({})
