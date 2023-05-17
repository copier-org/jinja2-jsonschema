# Contributing

Contributions are always welcome and appreciated!

## Prerequisites

* A [Git][git] client.

* A GitHub account.

* A Python interpreter, ideally Python 3.7 (the minimum supported version by this project).

* The [Poetry][poetry-setup] package and dependency manager. We recommend configuring Poetry to create a new virtual environment inside the project's root directory in `.venv/`:

    ```shell
    poetry config virtualenvs.in-project true
    ```

* Create a [fork of this project][fork] in your personal namespace.

## Setup

1. Clone the fork to your local machine.

1. Install dependencies:

    ```shell
    poetry install --all-extras
    ```

1. Install pre-commit hooks:

    ```shell
    poetry run pre-commit install
    ```

## Development

1. Create a new branch:

    ```shell
    git checkout -b your-branch-name
    ```

1. Edit the code and don't forget to add tests.

1. Commit and push your changes to the fork.

    ```shell
    git add .
    git commit
    git push
    ```

    > **NOTE**: This project uses [conventional commits][conventional-commits] as a commit message format.

1. Submit a pull request to this project.

[conventional-commits]: https://www.conventionalcommits.org
[fork]: https://github.com/copier-org/jinja2-jsonschema/fork
[git]: https://git-scm.com
[poetry-setup]: https://python-poetry.org/docs/#installation
