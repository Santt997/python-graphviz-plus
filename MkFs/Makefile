ENV_NAME=python-graphviz-plus
ENV_FILE=../YMLs/python-graph-viz.yml
ROOT_DIR=$(shell git rev-parse --show-toplevel)

.PHONY: create build check upload clean release

create:
	micromamba env create -f $(ENV_FILE) -n $(ENV_NAME) -y

build: clean
	cd $(ROOT_DIR) && micromamba run -n $(ENV_NAME) python -m build

check:
	cd $(ROOT_DIR) && micromamba run -n $(ENV_NAME) python -m twine check dist/*

upload:
	cd $(ROOT_DIR) && micromamba run -n $(ENV_NAME) python -m twine upload dist/*

release: build check upload

clean:
	cd $(ROOT_DIR) && rm -rf dist build *.egg-info