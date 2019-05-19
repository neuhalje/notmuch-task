clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {}  +

clean-build: clean-pyc
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

build: clean-build
	python setup.py sdist bdist_wheel

pypi-test: build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi-prod: build
	twine upload dist/*

lint:
	flake8 --exclude=.tox

integration-test:
	./integration_tests.sh

virtual-env:
	pipenv --python 3.6 --site-packages
	pipenv install --dev
