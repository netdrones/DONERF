import os
import sys

if __name__ == '__main__':

    image_dir = os.path.abspath(sys.argv[1])
    workspace_dir = sys.argv[2]
    train_dir = os.path.join(workspace_dir, 'train')
    test_dir = os.path.join(workspace_dir, 'test')
    val_dir = os.path.join(workspace_dir, 'val')

    images = os.listdir(image_dir)
    for im in images:
        basename = im.split('.')[0]
        if basename in os.listdir(train_dir):
            os.remove(os.path.join(train_dir, basename))
            os.symlink(os.path.join(image_dir, im), os.path.join(train_dir, im))
        elif basename in os.listdir(test_dir):
            os.remove(os.path.join(test_dir, basename))
            os.symlink(os.path.join(image_dir, im), os.path.join(test_dir,im))
        elif basename in os.listdir(val_dir):
            os.remove(os.path.join(val_dir, basename))
            os.symlink(os.path.join(image_dir, im), os.path.join(val_dir, im))
