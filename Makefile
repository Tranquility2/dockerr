SHELL=/bin/bash
.MAIN: install-nox

install-nox:
	python3 -m pip install --upgrade nox

setup-dev:
	python3 -m pip install --editable '.[dev]'

pip-clean:
	python3 -m pip uninstall -y -r <(pip freeze)

check-format:
	python3 -m black --diff --check .
	python3 -m isort --diff --check .

fix-format:
	python3 -m black .
	python3 -m isort .

check-lint:
	python3 -m pylint --reports=True --recursive=y .

build:
	python3 -m pip install --upgrade build
	python3 -m build

 publish:
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*
