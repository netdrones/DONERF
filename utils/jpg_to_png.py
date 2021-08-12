import os
import sys
from PIL import Image

if __name__ == '__main__':

    image_dir = sys.argv[1]
    images = os.listdir(image_dir)

    for im in images:
        fname = im.split('.')[0] + '.png'
        img = Image.open(os.path.join(image_dir, im))
        img.save(os.path.join(image_dir, fname))
