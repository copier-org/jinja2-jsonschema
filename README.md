# JSON Schema Validation within Jinja2 Templates

[![Tests](https://img.shields.io/github/actions/workflow/status/copier-org/jinja2-jsonschema/tests.yml?branch=main&label=Tests&labelColor=333&logo=github&style=flat-square)](https://github.com/copier-org/jinja2-jsonschema/actions?query=branch%3Amain)
[![Python versions](https://img.shields.io/pypi/pyversions/jinja2-jsonschema?label=Python&logo=python&logoColor=%23959DA5&style=flat-square)](https://pypi.org/project/jinja2-jsonschema)
[![PyPI](https://img.shields.io/pypi/v/jinja2-jsonschema?label=PyPI&logo=pypi&logoColor=%23959DA5&style=flat-square)](https://pypi.org/project/jinja2-jsonschema)
[![Code style: Black](https://img.shields.io/badge/Code%20Style-Black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Linter: Ruff](https://img.shields.io/badge/-Ruff-261230.svg?labelColor=grey&logo=ruff&logoColor=D7FF64&style=flat-square)](https://github.com/charliermarsh/ruff)
[![Type-checker: mypy](https://img.shields.io/badge/mypy-strict-2A6DB2.svg?style=flat-square)](http://mypy-lang.org)

A [Jinja2 extension][jinja-extensions] providing a [Jinja2 filter][jinja-filter] and a [Jinja2 test][jinja-test] for validating data against a JSON/YAML schema within [Jinja2][jinja] templates.

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

The extension provides:

* A Jinja2 filter which receives a schema file path or schema object as input and returns a [`jsonschema.ValidationError`][python-jsonschema-validationerror] object when validation fails and an empty string (`""`) otherwise.
* A Jinja2 test which receives a schema file path or schema object as input and returns `False` when validation fails and `True` otherwise.

The [JSON Schema dialect][jsonschema-dialect] is inferred from the `$schema` field in the JSON Schema document and, when omitted, defaults to the [latest dialect supported by the installed `jsonschema` library][python-jsonschema-features]. Both local and remote schemas are supported including [schema references][jsonschema-ref] and [JSON Pointers][jsonschema-jsonpointer].

Local schema files are loaded via a [Jinja2 loader](https://jinja.palletsprojects.com/en/latest/api/#loaders) in which case configuring the Jinja2 environment with a loader is mandatory.

Some example usage of the JSON Schema validation filter and test is this:

```python
from jinja2 import Environment
from jinja2 import FileSystemLoader


env = Environment(
    # Register a loader (only necessary when using local schema files).
    loader=FileSystemLoader("/path/to/templates"),
    # Register the extension.
    extensions=["jinja2_jsonschema.JsonSchemaExtension"],
)

# Example using an inline schema object.
template = env.from_string("{{ age | jsonschema({'type': 'integer', 'minimum': 0}) }}")
template.render(age=30)  # OK
template.render(age=-1)  # ERROR
template = env.from_string("{{ age is jsonschema({'type': 'integer', 'minimum': 0}) }}")
template.render(age=30)  # --> `True`
template.render(age=-1)  # --> `False`

# Example using a local schema file.
template = env.from_string("{{ age | jsonschema('age.json') }}")
template.render(age=30)  # OK
template.render(age=-1)  # ERROR
template = env.from_string("{{ age is jsonschema('age.json') }}")
template.render(age=30)  # --> `True`
template.render(age=-1)  # --> `False`

# Example using a remote schema file.
template = env.from_string("{{ age | jsonschema('https://example.com/age.json') }}")
template.render(age=30)  # OK
template.render(age=-1)  # ERROR
template = env.from_string("{{ age is jsonschema('https://example.com/age.json') }}")
template.render(age=30)  # --> `True`
template.render(age=-1)  # --> `False`
```

## Usage with Copier

The extension integrates nicely with [Copier][copier], e.g. for validating complex JSON/YAML answers in the Copier questionnaire. For this, add the extension as a [Jinja2 extension in `copier.yml`][copier-jinja-extensions] and use the Jinja2 filter in the `validator` field of a Copier [question][copier-questions]. For instance:

```yaml
_jinja_extensions:
  - jinja2_jsonschema.JsonSchemaExtension

complex_question:
  type: json # or `yaml`
  validator: "{{ complex_question | jsonschema('schemas/complex.json') }}"
```

In this example, a local schema file `schemas/complex.json` is used whose path is relative to the template root. To prevent copying schema files to the generated project, they should be either [excluded][copier-exclude]

```diff
+_exclude:
+  - schemas/
 _jinja_extensions:
   - jinja2_jsonschema.JsonSchemaExtension
```

or the project template should be located in a [subdirectory][copier-subdirectory] such as `template/`:

```diff
+_subdirectory_: template
 _jinja_extensions:
   - jinja2_jsonschema.JsonSchemaExtension
```

Finally, template consumers need to install the extension along with Copier. For instance with `pipx`:

```shell
pipx install copier
pipx inject copier jinja2-jsonschema
```

## Contributions

Contributions are always welcome via filing [issues](https://github.com/copier-org/jinja2-jsonschema/issues) or submitting [pull requests](https://github.com/copier-org/jinja2-jsonschema/pulls). Please check the [contribution guide][contribution-guide] for more details.

[contribution-guide]: https://github.com/copier-org/jinja2-jsonschema/blob/main/CONTRIBUTING.md
[copier]: https://github.com/copier-org/copier
[copier-exclude]: https://copier.readthedocs.io/en/stable/configuring/#exclude
[copier-jinja-extensions]: https://copier.readthedocs.io/en/stable/configuring/#jinja_extensions
[copier-questions]: https://copier.readthedocs.io/en/stable/configuring/#questions
[copier-subdirectory]: https://copier.readthedocs.io/en/stable/configuring/#subdirectory
[jinja]: https://jinja.palletsprojects.com
[jinja-extensions]: https://jinja.palletsprojects.com/en/latest/extensions/
[jinja-filter]: https://jinja.palletsprojects.com/en/latest/templates/#filters
[jinja-test]: https://jinja.palletsprojects.com/en/latest/templates/#tests
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
