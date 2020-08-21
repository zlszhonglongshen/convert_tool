import os
import glob
import _init_paths
import os.path as osp


def gen_caltech_path(root_path):
    label_path = 'Caltech/data/labels_with_ids'
    real_path = os.path.join(root_path, label_path)
    image_path = real_path.replace('labels_with_ids', 'images')
    images_exist = sorted(glob.glob(image_path + '/*.png'))
    with open('../src/data/caltech.all', 'w') as f:
        labels = sorted(glob.glob(real_path + '/*.txt'))
        for label in labels:
            image = label.replace('labels_with_ids', 'images').replace('.txt', '.png')
            if image in images_exist:
                print(image[22:], file=f)
    f.close()

def gen_mot15_test_path(root_path):
    seq_root = '/mnt/ssd2/Users/anhvn/Public_tracking/MOT15/images/test'
    seqs = [s for s in os.listdir(seq_root)]
    with open('../src/data/mot15.test', 'w') as f:
        for seq in seqs:
            image_path = osp.join(seq_root, seq, 'img1')
            print(image_path)
            images_exist = sorted(glob.glob(image_path + '/*.jpg'))
            for label in images_exist:
                label = label.replace('/mnt/ssd2/Users/anhvn/Public_tracking/', '')
                print(label, file=f)
    f.close()

if __name__ == '__main__':
    root = '/mnt/ssd2/Users/anhvn/Public_tracking/'
    # gen_caltech_path(root)
    gen_mot15_test_path(root)