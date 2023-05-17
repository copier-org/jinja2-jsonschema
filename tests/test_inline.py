"""Tests for using inline schemas."""
from typing import Any

import pytest

from .utils import SCHEMA
from .utils import TEST_CASES
from .utils import create_env


@pytest.mark.parametrize(("data", "message"), TEST_CASES)
def test_basic(data: Any, message: str) -> None:
    """Test basic validation."""
    env = create_env()
    tpl = env.from_string("{{ data | jsonschema(schema) }}")

    output = tpl.render(data=data, schema=SCHEMA)
    assert output == message
