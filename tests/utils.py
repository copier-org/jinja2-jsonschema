"""Testing utilities."""

from __future__ import annotations

import json
from textwrap import dedent
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal

import yaml
from jinja2 import Environment
from jinja2 import FileSystemLoader

from jinja2_jsonschema import JsonSchemaExtension

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "age": {
            "type": "integer",
            "minimum": 0,
        },
    },
}


def serialize(
    data: Any,
    data_format: Literal["json", "yaml"],
    indent: int | None = None,
) -> str:
    """Serialize data to a JSON or YAML string.

    Args:
        data:
            The data to serialize.
        data_format:
            The serialization format.
        indent:
            The indentation size.

    Returns:
        The serialized data.
    """
    return (
        json.dumps(data, indent=indent)
        if data_format == "json"
        else yaml.safe_dump(data, indent=indent)
    )


def create_env(templates_root: Path | None = None) -> Environment:
    """Create a new Jinja2 test environment.

    The Jinja2 environment is pre-configured with the JSON Schema extension and
    an optional filesystem loader.

    Args:
        templates_root:
            The root path of the templates for the filesystem loader.

    Returns:
        The Jinja2 environment.
    """
    return Environment(
        loader=None if templates_root is None else FileSystemLoader(templates_root),
        extensions=[JsonSchemaExtension],
    )


def build_file_tree(spec: Mapping[Path, str]) -> None:
    """Build a file tree based on a specification.

    Args:
        spec:
            A mapping from filesystem paths to file contents.
    """
    for path, contents in spec.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as f:
            f.write(dedent(contents))
