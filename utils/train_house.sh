#!/bin/bash

python utils/generate_poses.py house
python utils/data_loader.py house
python utils/jpg_to_png.py house/dense/images
rm -f house/dense/images/*.jpg
python utils/symlink.py house/dense/images house
gsutil cp gs://lucas.netdron.es/dataset_info.json house
python src/train.py -c configs/DONeRF_2_samples.ini --data house --logDir logs
