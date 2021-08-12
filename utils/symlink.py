import os
import sys

if __name__ == '__main__':

    image_dir = os.path.abspath(sys.argv[1])
    out_dir = sys.argv[2]

    images = os.listdir(image_dir)
    for im in images:
        os.symlink(os.path.join(image_dir, im), os.path.join(out_dir, im))
