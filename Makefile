deps-dev:
	pipenv install --dev

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {}  +

clean-build: clean-pyc
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

clean: clean-build clean-pyc

build: clean lint
	pipenv run python setup.py sdist bdist_wheel

pypi-test: build
	pipenv run twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi-prod: build
	pipenv run twine upload dist/*

#lint: deps-dev # deps-dev takes too long
lint:
	pipenv run flake8 --exclude=.tox --exclude=build/ --exclude=dist/

integration-test:
	./integration_tests.sh

virtual-env:
	pipenv --python 3.6 --site-packages
	pipenv install --dev
