install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	# python3 -m pip install --user dist/*.whl
	python3 -m pip install --user --force-reinstall dist/*.whl

package-quick-inst:
	python3 -m pip install .

lint:
	poetry run flake8 -v brain_games