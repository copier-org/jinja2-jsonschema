# JSON Schema Validation within Jinja2 Templates

[![CI](https://github.com/copier-org/jinja2-jsonschema/workflows/tests/badge.svg)](https://github.com/copier-org/jinja2-jsonschema/actions?query=branch%3Amain)
![Python versions](https://img.shields.io/pypi/pyversions/jinja2-jsonschema?logo=python&logoColor=%23959DA5)
[![PyPI](https://img.shields.io/pypi/v/jinja2-jsonschema?logo=pypi&logoColor=%23959DA5)](https://pypi.org/project/jinja2-jsonschema)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linter: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)
[![Type-checker: mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org)

A [Jinja2 extension][jinja-extensions] providing a [Jinja2 filter][jinja-filter] for validating data against a JSON/YAML schema within [Jinja2][jinja] templates.

## Installation

* With [`pip`](https://pip.pypa.io):

    ```shell
    pip install jinja2-jsonschema

    # ... or with YAML support
    pip install jinja2-jsonschema[yaml]
    ```

* With [`poetry`][poetry]:

    ```shell
    poetry add jinja2-jsonschema

    # ... or with YAML support
    poetry add jinja2-jsonschema -E yaml
    ```

* With [`pdm`][pdm]:

    ```shell
    pdm add jinja2-jsonschema

    # ... or with YAML support
    pdm add jinja2-jsonschema[yaml]
    ```

* With [`pipx`][pipx] (injected into the `pipx`-managed virtual env of a package):

    ```shell
    pipx inject PACKAGE jinja2-jsonschema

    # ... or with YAML support
    pipx inject PACKAGE jinja2-jsonschema[yaml]
    ```

## Usage

The extension provides a Jinja2 filter which receives a schema file path or schema object as input and returns a [`jsonschema.ValidationError`][python-jsonschema-validationerror] object when validation fails and an empty string (`""`) otherwise. The [JSON Schema dialect][jsonschema-dialect] is inferred from the `$schema` field in the JSON Schema document and, when omitted, defaults to the [latest dialect supported by the installed `jsonschema` library][python-jsonschema-features]. Both local and remote schemas are supported including [schema references][jsonschema-ref] and [JSON Pointers][jsonschema-jsonpointer].

Local schema files are loaded via a [Jinja2 loader](https://jinja.palletsprojects.com/en/latest/api/#loaders) in which case configuring the Jinja2 environment with a loader is mandatory.

Some example usage of the JSON Schema validation filter is this:

```python
from jinja2 import Environment
from jinja2 import FileSystemLoader


env = Environment(
    # Register a loader (only necessary when using local schema files).
    loader=FileSystemLoader("/path/to/templates"),
    # Register the extension.
    extensions=['jinja2_jsonschema.JsonSchemaExtension'],
)

# Example using an inline schema object.
template = env.from_string("{{ age | jsonschema({'type': 'integer', 'minimum': 0}) }}")
template.render(age=30)  # OK
template.render(age=-1)  # ERROR

# Example using a local schema file.
template = env.from_string("{{ age | jsonschema('age.json') }}")
template.render(age=30)  # OK
template.render(age=-1)  # ERROR

# Example using a remote schema file.
template = env.from_string("{{ age | jsonschema('https://example.com/age.json') }}")
template.render(age=30)  # OK
template.render(age=-1)  # ERROR
```

## Contributions

Contributions are always welcome via filing [issues](https://github.com/copier-org/jinja2-jsonschema/issues) or submitting [pull requests](https://github.com/copier-org/jinja2-jsonschema/pulls). Please check the [contribution guide][contribution-guide] for more details.

[contribution-guide]: https://https://github.com/copier-org/jinja2-jsonschema/blob/main/CONTRIBUTING.md
[jinja]: https://jinja.palletsprojects.com
[jinja-extensions]: https://jinja.palletsprojects.com/en/latest/extensions/
[jinja-filter]: https://jinja.palletsprojects.com/en/latest/templates/#filters
[jsonschema]: https://json-schema.org
[jsonschema-dialect]: https://json-schema.org/understanding-json-schema/reference/schema.html#schema
[jsonschema-ref]: https://json-schema.org/understanding-json-schema/structuring.html#ref
[jsonschema-jsonpointer]: https://json-schema.org/understanding-json-schema/structuring.html#json-pointer
[pdm]: https://pdm.fming.dev
[pip]: https://pip.pypa.io
[pipx]: https://pypa.github.io/pipx
[poetry]: https://python-poetry.org
[python-jsonschema-features]: https://python-jsonschema.readthedocs.io/en/stable/#features
[python-jsonschema-validationerror]: https://python-jsonschema.readthedocs.io/en/stable/api/jsonschema/exceptions/#jsonschema.exceptions.ValidationError
