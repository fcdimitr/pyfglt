# pyfglt

[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat)](https://fcdimitr.github.io/pyfglt/)
[![PyPI](https://img.shields.io/pypi/v/pyfglt.svg)](https://pypi.org/project/pyfglt/)
[![Tests](https://github.com/fcdimitr/pyfglt/actions/workflows/test.yml/badge.svg)](https://github.com/fcdimitr/pyfglt/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/fcdimitr/pyfglt?include_prereleases&label=changelog)](https://github.com/fcdimitr/pyfglt/releases)
[![License](https://img.shields.io/github/license/fcdimitr/pyfglt)](https://github.com/fcdimitr/pyfglt/blob/main/LICENSE)

Python package/wrapper of Fast Graphlet Transform. See the [documentation
overview](https://fcdimitr.github.io/pyfglt/) for more information.

## Installation

Install this library using `pip`:
```bash
pip install pyfglt
```
## Usage

See the examples under:

- [Getting started](https://fcdimitr.github.io/pyfglt/tutorial/01-getting-started)
- [Advanced usage](https://fcdimitr.github.io/pyfglt/tutorial/02-graphlet-based-network-properties)

## Citation

If you use this package, please cite this paper:

```bibtex
@article{fglt,
    author = {Floros, Dimitris and Pitsianis, Nikos and Sun, Xiaobai},
    journal = {IEEE HPEC},
    pages = {1--8},
    title = {{Fast graphlet transform of sparse graphs}},
    year = {2020}
}
```

## Development/Contribution

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd pyfglt
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
python -m pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
