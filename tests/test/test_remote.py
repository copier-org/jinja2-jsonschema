"""Tests for using remote schema files."""

from pathlib import Path
from typing import Any
from typing import Literal

import pytest

from jinja2_jsonschema.errors import SchemaFileNotFoundError
from tests.conftest import HTTPServerFactory
from tests.utils import SCHEMA
from tests.utils import build_file_tree
from tests.utils import create_env
from tests.utils import serialize

from .utils import TEST_CASES


@pytest.mark.parametrize(("data", "message"), TEST_CASES)
@pytest.mark.parametrize("data_format", ["json", "yaml"])
def test_basic(
    tmp_path: Path,
    http_server_factory: HTTPServerFactory,
    data_format: Literal["json", "yaml"],
    data: Any,
    message: str,
) -> None:
    """Test basic validation."""
    url = http_server_factory(tmp_path)
    build_file_tree(
        {
            (tmp_path / f"schema.{data_format}"): serialize(SCHEMA, data_format),
        }
    )

    env = create_env(tmp_path)
    tpl = env.from_string("{{ data is jsonschema(url + '/schema.' + data_format) }}")

    output = tpl.render(data=data, url=url, data_format=data_format)
    assert output == message


@pytest.mark.parametrize(("data", "message"), TEST_CASES)
@pytest.mark.parametrize("prefix", ["", "./"])
@pytest.mark.parametrize("data_format", ["json", "yaml"])
def test_ref_with_relative_path(
    tmp_path: Path,
    http_server_factory: HTTPServerFactory,
    data_format: Literal["json", "yaml"],
    prefix: str,
    data: Any,
    message: str,
) -> None:
    """Test remote reference resolution with relative paths."""
    url = http_server_factory(tmp_path)
    build_file_tree(
        {
            (tmp_path / "schema.yaml"): serialize(
                {"$ref": f"{prefix}sub/sub/schema.json"}, "yaml"
            ),
            (tmp_path / "schema.json"): serialize(
                {"$ref": f"{prefix}sub/schema.yaml"}, "json"
            ),
            (tmp_path / "sub" / "sub" / "schema.yaml"): serialize(
                {"$ref": f"{prefix}../schema.json"}, "yaml"
            ),
            (tmp_path / "sub" / "sub" / "schema.json"): serialize(
                {"$ref": f"{prefix}../schema.yaml"}, "json"
            ),
            (tmp_path / "sub" / "schema.yaml"): serialize(SCHEMA, "yaml"),
            (tmp_path / "sub" / "schema.json"): serialize(SCHEMA, "json"),
        }
    )

    env = create_env(tmp_path)
    tpl = env.from_string("{{ data is jsonschema(url + '/schema.' + data_format) }}")

    output = tpl.render(data=data, url=url, data_format=data_format)
    assert output == message


@pytest.mark.parametrize(("data", "message"), TEST_CASES)
@pytest.mark.parametrize("data_format", ["json", "yaml"])
def test_ref_with_absolute_path(
    tmp_path: Path,
    http_server_factory: HTTPServerFactory,
    data_format: Literal["json", "yaml"],
    data: Any,
    message: str,
) -> None:
    """Test remote reference resolution with absolute paths."""
    url = http_server_factory(tmp_path)
    build_file_tree(
        {
            (tmp_path / "schema.yaml"): serialize({"$ref": "/sub/schema.json"}, "yaml"),
            (tmp_path / "schema.json"): serialize({"$ref": "/sub/schema.yaml"}, "json"),
            (tmp_path / "sub" / "schema.yaml"): serialize(SCHEMA, "yaml"),
            (tmp_path / "sub" / "schema.json"): serialize(SCHEMA, "json"),
        }
    )

    env = create_env(tmp_path)
    tpl = env.from_string("{{ data is jsonschema(url + '/schema.' + data_format) }}")

    output = tpl.render(data=data, url=url, data_format=data_format)
    assert output == message


@pytest.mark.parametrize(("data", "message"), TEST_CASES)
@pytest.mark.parametrize("data_format", ["json", "yaml"])
def test_ref_with_url(
    tmp_path: Path,
    http_server_factory: HTTPServerFactory,
    data_format: Literal["json", "yaml"],
    data: Any,
    message: str,
) -> None:
    """Test remote reference resolution with absolute paths."""
    url = http_server_factory(tmp_path)
    build_file_tree(
        {
            (tmp_path / "schema.yaml"): serialize(
                {"$ref": f"{url}/sub/schema.json"}, "yaml"
            ),
            (tmp_path / "schema.json"): serialize(
                {"$ref": f"{url}/sub/schema.yaml"}, "json"
            ),
            (tmp_path / "sub" / "schema.yaml"): serialize(SCHEMA, "yaml"),
            (tmp_path / "sub" / "schema.json"): serialize(SCHEMA, "json"),
        }
    )

    env = create_env(tmp_path)
    tpl = env.from_string("{{ data is jsonschema(url + '/schema.' + data_format) }}")

    output = tpl.render(data=data, url=url, data_format=data_format)
    assert output == message


@pytest.mark.parametrize(("data", "message"), TEST_CASES)
@pytest.mark.parametrize("pointer", ["/definitions/person", "/definitions/personRef"])
@pytest.mark.parametrize("data_format", ["json", "yaml"])
def test_jsonpointer(
    tmp_path: Path,
    http_server_factory: HTTPServerFactory,
    data_format: Literal["json", "yaml"],
    pointer: str,
    data: Any,
    message: str,
) -> None:
    """Test JSON Pointer resolution in a remote schema file."""
    url = http_server_factory(tmp_path)
    build_file_tree(
        {
            (tmp_path / f"schema.{data_format}"): serialize(
                {
                    "definitions": {
                        "person": SCHEMA,
                        "personRef": {
                            "$ref": f"sub.{data_format}#/definitions/person",
                        },
                    }
                },
                data_format,
            ),
            (tmp_path / f"sub.{data_format}"): serialize(
                {
                    "definitions": {
                        "person": SCHEMA,
                    }
                },
                data_format,
            ),
        }
    )

    env = create_env(tmp_path)
    tpl = env.from_string(
        "{{ data is jsonschema(url + '/schema.' + data_format + '#' + pointer) }}"
    )

    output = tpl.render(data=data, url=url, data_format=data_format, pointer=pointer)
    assert output == message


@pytest.mark.parametrize(
    ("schema_file", "message"),
    [
        (
            "schema.json",
            'Schema file ".+" not found',
        ),
        (
            "../inaccessible-schema.json",
            'Schema file ".+" not found',
        ),
    ],
)
def test_schema_not_found(
    tmp_path: Path,
    http_server_factory: HTTPServerFactory,
    schema_file: str,
    message: str,
) -> None:
    """Test basic validation."""
    build_file_tree(
        {
            (tmp_path / "root" / "schema.json"): serialize(
                {"$ref": "../inaccessible-schema.json"}, "json"
            ),
            (tmp_path / "inaccessible-schema.json"): serialize(SCHEMA, "json"),
        }
    )
    url = http_server_factory(tmp_path / "root")

    env = create_env(tmp_path)
    tpl = env.from_string("{{ data is jsonschema(url + '/' + schema_file) }}")

    with pytest.raises(SchemaFileNotFoundError, match=message):
        tpl.render(data={"age": 30}, url=url, schema_file=schema_file)
