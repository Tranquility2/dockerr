
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/) [![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint) [![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

[![PyPI - Version](https://img.shields.io/pypi/v/dockerr.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/dockerr/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dockerr.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/dockerr/) [![Coverage Status](https://coveralls.io/repos/github/Tranquility2/dockerr/badge.svg?branch=master)](https://coveralls.io/github/Tranquility2/dockerrr?branch=master)

# dockerr

> [!IMPORTANT]
> Happy to update that I got this framework cabablities merged into [testcontainers-python](https://github.com/testcontainers/testcontainers-python)
> (Checkout the [PR](https://github.com/testcontainers/testcontainers-python/pull/585))  
> This Repo will hopefully (oneday) be reporposed into something new 😃

## Description

This is a python framwork for running docker containers in order to test them.
Fox example: you can run a container, test something while its still running and the framework will take care of cleaning up afterwards.
It's designed to be simple and easy to use.

## Installation

```bash
pip install dockerr
```

## Usage

```python
from dockerr.runner import DockerRunner

with DockerRunner(tag, name, ports, path, dockerfile=DOCKER_FILE):
    # Do something
```

## Status
~~This is an early version of the framework and it's still under development.~~

**Deprecated** - please see note above

## Examples
Please checkout the samples folder for more examples.
