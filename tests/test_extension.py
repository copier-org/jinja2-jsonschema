"""Tests for adding the extension to the Jinja2 environment."""
from re import escape
from typing import Any

import pytest
from jinja2 import Environment
from jinja2.ext import Extension

from jinja2_jsonschema import JsonSchemaExtension


def test_filter_name_conflict() -> None:
    """Test the behavior when a filter name conflict occurs."""

    def _fake_filter(data: Any) -> str:
        return ""

    class _TestExtension(Extension):
        def __init__(self, environment: Environment) -> None:
            super().__init__(environment)
            environment.filters["jsonschema"] = _fake_filter

    with pytest.warns(
        RuntimeWarning,
        match=escape(
            'A filter named "jsonschema" already exists in the Jinja2 environment'
        ),
    ):
        env = Environment(extensions=[_TestExtension, JsonSchemaExtension])

    assert env.filters["jsonschema"] == _fake_filter
