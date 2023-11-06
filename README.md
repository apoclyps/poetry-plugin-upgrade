# Poetry Plugin: upgrade

![release](https://github.com/apoclyps/poetry-plugin-upgrade/actions/workflows/release.yml/badge.svg)
![publish](https://github.com/apoclyps/poetry-plugin-upgrade/actions/workflows/publish.yml/badge.svg)
![test](https://github.com/apoclyps/poetry-plugin-upgrade/actions/workflows/test.yml/badge.svg)
[![license](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
![python_version](https://img.shields.io/badge/Python-%3E=3.8-blue)
![poetry_version](https://img.shields.io/badge/Poetry-%3E=1.6-blue)

This package is a plugin that updates dependencies and bumps their versions in `pyproject.toml` file. The version constraints are respected, unless the `--latest` flag is passed, in which case dependencies are updated to the latest available compatible versions.

This plugin provides similar features as the existing `update` command with additional features.

## Installation

The easiest way to install the `upgrade` plugin is via the `self add` command of Poetry.

```shell
poetry self add poetry-plugin-upgrade
```

If you used `pipx` to install Poetry you can add the plugin via the `pipx inject` command.

```shell
pipx inject poetry poetry-plugin-upgrade
```

Otherwise, if you used `pip` to install Poetry you can add the plugin packages via the `pip install` command.

```shell
pip install poetry-plugin-upgrade
```

## Usage

The plugin provides an `upgrade` command to update dependencies

```shell
poetry upgrade --help
```

Update dependencies

```shell
poetry upgrade
```

Update dependencies to the latest available compatible versions

```shell
poetry upgrade --latest
```

Update the `foo` and `bar` packages

```shell
poetry upgrade foo bar
```

Update packages only in the `main` group

```shell
poetry upgrade --only main
```

Update packages but ignore the `dev` group

```shell
poetry upgrade --without dev
```

## Contributing

Contributions are welcome! See the [Contributing Guide](https://github.com/apoclyps/poetry-plugin-upgrade/blob/master/CONTRIBUTING.md).

## Issues

If you encounter any problems, please file an [issue](https://github.com/apoclyps/poetry-plugin-upgrade/issues) along with a
detailed description.
