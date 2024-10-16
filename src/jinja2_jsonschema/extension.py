"""Jinja2 extension."""

from __future__ import annotations

import json
from collections.abc import Mapping
from http import HTTPStatus
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import urlopen
from warnings import warn

import jsonschema
from jinja2 import TemplateNotFound
from jinja2.ext import Extension

from .errors import JsonSchemaExtensionError
from .errors import LoaderNotFoundError
from .errors import SchemaFileNotFoundError

if TYPE_CHECKING:
    from _typeshed import Incomplete
    from jinja2 import Environment

__all__ = ["JsonSchemaExtension"]


class JsonSchemaExtension(Extension):
    """Jinja2 extension for using JSON Schema within Jinja2 templates."""

    def __init__(self, environment: Environment) -> None:
        super().__init__(environment)

        jsonschema_filter = _JsonSchemaFilter(environment)

        if "jsonschema" in environment.filters:
            warn(
                'A filter named "jsonschema" already exists in the Jinja2 environment',
                category=RuntimeWarning,
                stacklevel=2,
            )
        else:
            environment.filters["jsonschema"] = jsonschema_filter

        def jsonschema_test(data: Any, schema: str | _Schema) -> bool:  # noqa: ANN401
            return not jsonschema_filter(data, schema)

        if "jsonschema" in environment.tests:
            warn(
                'A test named "jsonschema" already exists in the Jinja2 environment',
                category=RuntimeWarning,
                stacklevel=2,
            )
        else:
            environment.tests["jsonschema"] = jsonschema_test


_Schema = Mapping[str, Any]


class _JsonSchemaFilter:
    """Jinja2 filter for validating data against a JSON Schema document."""

    def __init__(self, environment: Environment) -> None:
        self._environment = environment

    def __call__(
        self,
        data: Any,  # noqa: ANN401
        schema: str | _Schema,
    ) -> jsonschema.ValidationError | Literal[""]:
        """Validate data against a JSON Schema document.

        Args:
            data:
                The data to validate.
            schema:
                The schema object or an URI of the schema.

        Returns:
            An empty string if the validation was successful, or an error object
            if the validation failed.
        """
        if isinstance(schema, str):
            if schema.startswith(("http://", "https://")):
                schema = {"$ref": schema}
            else:
                if not schema.startswith("/"):
                    schema = f"/{schema}"
                schema = {"$ref": f"file://{schema}"}

        try:
            jsonschema.validate(
                data,
                schema,
                resolver=jsonschema.RefResolver(
                    "",
                    {},
                    handlers={
                        "file": self._resolve_local_schema,
                        "http": self._resolve_remote_schema,
                        "https": self._resolve_remote_schema,
                    },
                ),
            )
        except jsonschema.RefResolutionError as exc:
            if isinstance(exc.__context__, JsonSchemaExtensionError):
                raise exc.__context__ from None
            raise
        except jsonschema.ValidationError as exc:
            return exc

        return ""

    def _resolve_local_schema(self, uri: str) -> Incomplete:
        if not self._environment.loader:
            raise LoaderNotFoundError

        schema_file = urlparse(uri).path
        try:
            raw_schema, *_ = self._environment.loader.get_source(
                self._environment,
                schema_file,
            )
        except TemplateNotFound as exc:
            raise SchemaFileNotFoundError(schema_file) from exc

        return self._load(raw_schema)

    def _resolve_remote_schema(self, uri: str) -> Incomplete:
        try:
            with urlopen(uri) as response:  # noqa: S310
                raw_schema = response.read().decode("utf-8")
        except HTTPError as exc:
            if exc.code == HTTPStatus.NOT_FOUND:
                raise SchemaFileNotFoundError(uri) from exc
            raise
        return self._load(raw_schema)

    @staticmethod
    def _load(raw_schema: str) -> _Schema:
        schema: _Schema
        try:
            import yaml
        except ImportError:
            schema = json.loads(raw_schema)
        else:
            schema = yaml.safe_load(raw_schema)
        return schema
