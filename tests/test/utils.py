"""Testing utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

if TYPE_CHECKING:
    from collections.abc import Sequence

TEST_CASES: Sequence[tuple[Any, str]] = [
    ({"age": 30}, "True"),
    ({"age": -1}, "False"),
]
