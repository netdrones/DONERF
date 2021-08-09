.ONESHELL:
SHELL=/bin/bash
ENV_NAME=donerf
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

install:
	conda env update -f environment.yml

house:
	python -m nerf_sh.train \
	  --train_dir ckpts/house \
	  --config nerf_sh/config/tt \
	  --data_dir data/house
