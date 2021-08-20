.ONESHELL:
SHELL=/bin/bash
ENV_NAME=donerf
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

.PHONY: install house

install:
	conda env update -f environment.yml

house:
	if [ ! -d house ]; then gsutil -m cp -r gs://lucas.netdron.es/house .; fi
	sh +x bin/train.sh -i house

coffee:
	if [ ! -d coffee ]; then gsutil -m cp -r gs://lucas.netdron.es/coffee .; fi
	sh +x bin/train.sh -i coffee
