import os
import sys
import json
import shutil
import random
import cv2 as cv
import numpy as np
from sklearn.model_selection import train_test_split

TRAIN = 0.95
VAL_SIZE = 10

def load_cameras(jsonfile):
    with open(jsonfile) as f:
        data = json.load(f)

    # Generate train/test/val splits
    keys = list(data.keys())
    train, test = train_test_split(keys, test_size=(1-TRAIN))
    val = np.random.choice(test, 10, replace=False)

    return data, train, test, val

def write_txt(keys, data, out_dir):
    rgb_dir = os.path.join(out_dir, 'rgb')
    pose_dir = os.path.join(out_dir, 'pose')
    parent_dir = os.path.join(out_dir, '../dense')
    intrinsic_dir = os.path.join(out_dir, 'intrinsics')

    if os.path.exists(rgb_dir):
        shutil.rmtree(rgb_dir)
    os.mkdir(rgb_dir)
    if os.path.exists(pose_dir):
        shutil.rmtree(pose_dir)
    os.mkdir(pose_dir)
    if os.path.exists(intrinsic_dir):
        shutil.rmtree(intrinsic_dir)
    os.mkdir(intrinsic_dir)

    for key in keys:
        fname = key.split('.')[0] + '.txt'
        intrinsics = np.array(data[key]['K'])
        pose = np.array(data[key]['W2C'])
        np.savetxt(os.path.join(intrinsic_dir, fname), intrinsics)
        np.savetxt(os.path.join(pose_dir, fname), pose)
        os.symlink(os.path.abspath(os.path.join(parent_dir, f'images/{key}')), os.path.join(rgb_dir, key))

if __name__ == '__main__':

    workspace_dir = sys.argv[1]
    train_dir = os.path.join(workspace_dir, 'train')
    test_dir = os.path.join(workspace_dir, 'test')
    val_dir = os.path.join(workspace_dir, 'validation')

    dir_list = [train_dir, test_dir, val_dir]
    for d in dir_list:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.mkdir(d)

    data, train, test, val = load_cameras(os.path.join(workspace_dir, 'posed_images/cameras_normalized.json'))

    write_txt(train, data, train_dir)
    write_txt(test, data, test_dir)
    write_txt(val, data, val_dir)
