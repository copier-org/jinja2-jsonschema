"""Testing utilities."""
from typing import Any
from typing import Sequence
from typing import Tuple

TEST_CASES: Sequence[Tuple[Any, str]] = [
    ({"age": 30}, "True"),
    ({"age": -1}, "False"),
]
