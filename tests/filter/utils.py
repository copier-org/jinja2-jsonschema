"""Testing utilities."""

from __future__ import annotations

from typing import Any
from typing import Sequence

from pychoir import Matchable
from pychoir import MatchesRegex

TEST_CASES: Sequence[tuple[Any, Matchable]] = [
    (
        {"age": 30},
        "",
    ),
    (
        {"age": -1},
        MatchesRegex(
            r"(?m)"
            r"-1 is less than the minimum of 0"
            r"\s+"
            r"Failed validating 'minimum' in schema\['properties'\]\['age'\]:"
            r"\s+"
            r"\{.+\}"
            r"\s+"
            r"On instance\['age'\]:"
            r"\s+"
            r"-1"
        ),
    ),
]
