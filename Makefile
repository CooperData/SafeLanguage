# Shell to use with Make
SHELL := /bin/bash

# Set important Paths
ENV_PATH=./setup
PROJECT_PATH=./
ENV=safelanguage

create_env:
	source deactivate
	set -ex
	conda env create -f ${ENV_PATH}/environment.yml

delete_env:
	conda remove --name ${ENV} --all

test:
