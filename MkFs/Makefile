ENV_NAME=python-graphviz-plus
ENV_FILE=../YMLs/python-graph-viz.yml

.PHONY: create build check upload clean release

create:
	micromamba env create -f $(ENV_FILE) -n $(ENV_NAME) -y

build: clean
	micromamba run -n $(ENV_NAME) python -m build

check:
	micromamba run -n $(ENV_NAME) python -m twine check dist/*

upload:
	micromamba run -n $(ENV_NAME) python -m twine upload dist/*

release: build check upload

clean:
	rm -rf dist build *.egg-info