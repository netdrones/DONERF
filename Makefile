.ONESHELL:
SHELL=/bin/bash
ENV_NAME=donerf
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

install:
	conda env update -f environment.yml

classroom:
	python src/train.py -c ./configs/DONeRF_2_samples.ini --data ./classroom --logDir ./results

