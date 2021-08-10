import os
import sys
import shutil
import subprocess
from extract_sfm import extract_all_to_dir
from normalize_cam_dict import normalize_cam_dict

def main(out_dir):
    mvs_dir = os.path.join(out_dir, 'dense')

    # extract camera parameters and undistorted images
    if os.path.exists(os.path.join(out_dir, 'posed_images')):
        shutil.rmtree(os.path.join(out_dir, 'posed_images'))
    os.mkdir(os.path.join(out_dir, 'posed_images'))
    extract_all_to_dir(os.path.join(mvs_dir, 'sparse'), os.path.join(out_dir, 'posed_images'))
    undistorted_img_dir = os.path.join(mvs_dir, 'images')
    normalize_cam_dict(os.path.join(out_dir, 'posed_images/cameras.json'),
                       os.path.join(out_dir, 'posed_images/cameras_normalized.json'))

if __name__ == '__main__':

    out_dir = sys.argv[1]
    main(out_dir)
