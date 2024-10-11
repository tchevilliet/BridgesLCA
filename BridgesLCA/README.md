# BridgesLCA

[![PyPI](https://img.shields.io/pypi/v/BridgesLCA.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/BridgesLCA.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/BridgesLCA)][pypi status]
[![License](https://img.shields.io/pypi/l/BridgesLCA)][license]

[![Read the documentation at https://BridgesLCA.readthedocs.io/](https://img.shields.io/readthedocs/BridgesLCA/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/tchevilliet/BridgesLCA/actions/workflows/python-test.yml/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/tchevilliet/BridgesLCA/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/BridgesLCA/
[read the docs]: https://BridgesLCA.readthedocs.io/
[tests]: https://github.com/tchevilliet/BridgesLCA/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/tchevilliet/BridgesLCA
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## About the Project

This model aims to produce the estimated amount of the materials needed for building a bridge based on the user input of the bridge *lenght* and *Width* and optionally *Bridge Type* based on the data on built bridges across France. 

Estimated amount of materials include; Concrete (m³) for the foundation, piles, wall and abutments, piers, deck, and blinding. Structural Steel (kg) for piles, deck, railings, and Steel used for the concrete reinforcement.


## Installation

You can install _bridgeslca_ via [pip] from [PyPI]:

```console
$ pip install bridgeslca
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide][Contributor Guide].

## License

Distributed under the terms of the [MIT license][License],
_bridgeslca_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue][Issue Tracker] along with a detailed description.


<!-- github-only -->

[command-line reference]: https://BridgesLCA.readthedocs.io/en/latest/usage.html
[License]: https://github.com/tchevilliet/BridgesLCA/blob/main/LICENSE
[Contributor Guide]: https://github.com/tchevilliet/BridgesLCA/blob/main/CONTRIBUTING.md
[Issue Tracker]: https://github.com/tchevilliet/BridgesLCA/issues


## Building the Documentation

You can build the documentation locally by installing the documentation Conda environment:

```bash
conda env create -f docs/environment.yml
```

activating the environment

```bash
conda activate sphinx_BridgesLCA
```

and [running the build command](https://www.sphinx-doc.org/en/master/man/sphinx-build.html#sphinx-build):

```bash
sphinx-build docs _build/html --builder=html --jobs=auto --write-all; open _build/html/index.html
```