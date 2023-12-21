install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl
	# python3 -m pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 -v gendiff

test:
	poetry run pytest -v

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

publish:
	poetry publish --dry-run

package-quick-inst:
	python3 -m pip install .

selfcheck:
	poetry check

check: selfcheck test lint

build-package: install build package-install

.PHONY: install build package lint test publish selfcheck check
