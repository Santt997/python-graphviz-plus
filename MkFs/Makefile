ENV_NAME=python-graphviz-plus
ENV_FILE=../YMLs/python-graph-viz.yml

.PHONY: env build check upload clean

env:
	micromamba env create -f $(ENV_FILE) -n $(ENV_NAME)

build:
	python -m build

check:
	python -m twine check dist/*

upload:
	python -m twine upload dist/*

clean:
	rm -rf dist build *.egg-info