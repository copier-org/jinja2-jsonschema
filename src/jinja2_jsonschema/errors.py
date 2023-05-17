"""Error classes."""

__all__ = [
    "JsonSchemaExtensionError",
    "LoaderNotFoundError",
    "SchemaFileNotFoundError",
]


class JsonSchemaExtensionError(Exception):
    """Base class for all JSON Schema extension errors."""


class LoaderNotFoundError(JsonSchemaExtensionError):
    """Jinja2 loader could not be found."""

    def __init__(self) -> None:
        super().__init__("Jinja2 loader not found")


class SchemaFileNotFoundError(JsonSchemaExtensionError, FileNotFoundError):
    """JSON Schema file could not be found."""

    def __init__(self, schema_file: str) -> None:
        super().__init__(f'Schema file "{schema_file}" not found')
