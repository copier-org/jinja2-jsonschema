"""Tests for adding the extension to the Jinja2 environment."""
from re import escape

import pytest
from jinja2 import Environment
from jinja2.ext import Extension

from jinja2_jsonschema import JsonSchemaExtension


def test_filter_name_conflict() -> None:
    """Test the behavior when a filter name conflict occurs."""

    class _TestExtension(Extension):
        def __init__(self, environment: Environment) -> None:
            super().__init__(environment)
            environment.filters["jsonschema"] = self

    with pytest.warns(
        RuntimeWarning,
        match=escape(
            'A filter named "jsonschema" already exists in the Jinja2 environment'
        ),
    ):
        env = Environment(extensions=[_TestExtension, JsonSchemaExtension])

    assert isinstance(env.filters["jsonschema"], _TestExtension)
