#!/bin/bash

python utils/generate_poses.py house
python utils/data_loader.py house
python utils/jpg_to_png.py house/dense/images
rm -f house/dense/images/*.jpg
mkdir -p house/tmp
mv house/train/*.npz house/tmp
rm house/train/*
python utils/symlink.py house/dense/images house/train
mv house/tmp/* house/train
rm -rf house/tmp
gsutil cp gs://lucas.netdron.es/dataset_info.json house
python src/train.py -c configs/DONeRF_2_samples.ini --data house --logDir logs
