"""Testing utilities."""

from __future__ import annotations

from typing import Any
from typing import Sequence

TEST_CASES: Sequence[tuple[Any, str]] = [
    ({"age": 30}, "True"),
    ({"age": -1}, "False"),
]
