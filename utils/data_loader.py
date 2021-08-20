import os
import sys
import json
import shutil
import random
import cv2 as cv
import numpy as np
from sklearn.model_selection import train_test_split

TRAIN = 0.95

def load_json(jsonfile):
    with open(jsonfile) as f:
        data = json.load(f)

    return data

class Loader:

    def  __init__(self, workspace_dir):

        self.workspace_dir = workspace_dir
        self.dense_dir = os.path.join(self.workspace_dir, 'dense')
        self.train_dir = os.path.join(self.workspace_dir, 'train')
        self.test_dir  = os.path.join(self.workspace_dir, 'test')
        self.val_dir = os.path.join(self.workspace_dir, 'val')

        if os.path.exists(self.train_dir):
            shutil.rmtree(self.train_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.val_dir):
            shutil.rmtree(self.val_dir)

        os.mkdir(self.train_dir)
        os.mkdir(self.test_dir)
        os.mkdir(self.val_dir)

    def load(self):
        cams = load_json(os.path.join(workspace_dir, 'posed_images/cameras.json'))
        normalized_cams = load_json(os.path.join(workspace_dir, 'posed_images/cameras_normalized.json'))
        self.write_data(normalized_cams)
        self.write_transforms(normalized_cams)

    def read_write_intrinsics(self, cams):
        keys = list(cams.keys())
        K = cams[keys[0]]['K']
        K = K.reshape(4, 4)

    def read_array(self, path):
        with open(path, "rb") as fid:
            width, height, channels = np.genfromtxt(fid, delimiter="&", max_rows=1,
                                                    usecols=(0, 1, 2), dtype=int)
            fid.seek(0)
            num_delimiter = 0
            byte = fid.read(1)
            while True:
                if byte == b"&":
                    num_delimiter += 1
                    if num_delimiter >= 3:
                        break
                byte = fid.read(1)
            array = np.fromfile(fid, np.float32)
        array = array.reshape((width, height, channels), order="F")
        return np.transpose(array, (1, 0, 2)).squeeze()

    def write_data(self, data):
        frames = data['frames']

        for frame in frames:
            key = frame['file_path'].split('/')[-1]
            depth_map = self.read_array(os.path.join(self.dense_dir, f'stereo/depth_maps/{key}.jpeg.geometric.bin'))

            if 'train' in frame['file_path']:
                np.savez(os.path.join(self.train_dir, key.split('.')[0] + '_depth'), depth_map)
                os.symlink(os.path.abspath(os.path.join(self.dense_dir, f'images/{key}')), os.path.join(self.train_dir, key))
            elif 'test' in frame['file_path']:
                np.savez(os.path.join(self.test_dir, key.split('.')[0] + '_depth'), depth_map)
                os.symlink(os.path.abspath(os.path.join(self.dense_dir, f'images/{key}')), os.path.join(self.test_dir, key))
            elif 'val' in frame['file_path']:
                np.savez(os.path.join(self.val_dir, key.split('.')[0] + '_depth'), depth_map)
                os.symlink(os.path.abspath(os.path.join(self.dense_dir, f'images/{key}')), os.path.join(self.val_dir, key))

    def write_transforms(self, data):
        out_train_dict_file = os.path.join(self.workspace_dir, 'transforms_train.json')
        out_test_dict_file = os.path.join(self.workspace_dir, 'transforms_test.json')
        out_val_dict_file = os.path.join(self.workspace_dir, 'transforms_val.json')

        frames = data['frames']
        train, test, val = [], [], []
        for frame in frames:
            if 'train' in frame['file_path']:
                train.append(frame)
            elif 'test' in frame['file_path']:
                test.append(frame)
            else:
                val.append(frame)

        with open(out_train_dict_file, 'w') as fp:
            out_train_dict = {'frames': train}
            json.dump(out_train_dict, fp, indent=2, sort_keys=True)

        with open(out_test_dict_file, 'w') as fp:
            out_test_dict = {'frames': test}
            json.dump(out_test_dict, fp, indent=2, sort_keys=True)

        with open(out_val_dict_file, 'w') as fp:
            out_val_dict = {'frames': val}
            json.dump(out_val_dict, fp, indent=2, sort_keys=True)

if __name__ == '__main__':

    workspace_dir = sys.argv[1]
    loader = Loader(workspace_dir)
    loader.load()
