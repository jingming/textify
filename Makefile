.PHONY: clean install 

venv:
	@python --version || (echo "Python is not installed, please install Python 2 or Python 3"; exit 1);
	virtualenv --python=python venv

install: venv
	. venv/bin/activate; pip install .

clean:
	rm -rf venv
