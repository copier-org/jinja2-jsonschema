"""Tests for using inline schemas."""

from typing import Any

import pytest

from tests.utils import SCHEMA
from tests.utils import create_env

from .utils import TEST_CASES


@pytest.mark.parametrize(("data", "message"), TEST_CASES)
def test_basic(data: Any, message: str) -> None:
    """Test basic validation."""
    env = create_env()
    tpl = env.from_string("{{ data | jsonschema(schema) }}")

    output = tpl.render(data=data, schema=SCHEMA)
    assert output == message
