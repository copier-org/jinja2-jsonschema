"""Testing utilities."""

from textwrap import dedent
from typing import Any
from typing import Sequence
from typing import Tuple

TEST_CASES: Sequence[Tuple[Any, str]] = [
    (
        {"age": 30},
        "",
    ),
    (
        {"age": -1},
        dedent(
            """
            -1 is less than the minimum of 0

            Failed validating 'minimum' in schema['properties']['age']:
                {'minimum': 0, 'type': 'integer'}

            On instance['age']:
                -1
            """
        ).strip(),
    ),
]
