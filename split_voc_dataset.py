import os
import random
import argparse
import os.path as osp

def gen_image_set(dataset_path, trainval_percent = 0.9, train_percent = 0.9):
    # Default 90% of data into trainval set, 10% to testset
    # Default 90% of trainval data into train set, 10% into valset
    assert osp.isdir(dataset_path), 'Invalid dataset directory !'

    xmlfilepath = osp.join(dataset_path, 'Annotations')
    mainpath = osp.join(dataset_path, 'ImageSets', 'Main')
    os.makedirs(mainpath, exist_ok=True)
    total_xml = os.listdir(xmlfilepath)
    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)

    print("trainval size: ", tv)
    print("train size: ", tr)
    print("val size: ", tv - tr)
    print('test size: ', num - tv)

    ftrainval = open(osp.join(mainpath, 'trainval.txt'), 'w')
    ftest = open(osp.join(mainpath, 'test.txt'), 'w')
    ftrain = open(osp.join(mainpath, 'train.txt'), 'w')
    fval = open(osp.join(mainpath, 'val.txt'), 'w')

    for i in list:
        name = total_xml[i][:-4] + '\n'
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='Split trainval, train, test, val .txt VOC format !')
    parse.add_argument('-d', '--dataset_dir',
                       default='/home/anhvn/detectron2/datasets/VOC2007',
                       help='Path to dataset directory VOC format', type=str)
    parse.add_argument('-tvr', '--trainval_ratio',
                       default=0.8,
                       help='Trainval ratio of all annotations, test ratio is the remain. Default is 0.8, meaning 80% of total data into trainval set, 20% of total data into testset', type=float)
    parse.add_argument('-tr', '--train_ratio',
                       default=0.9,
                       help='Train ratio of trainval annotations, val ratio is the remain. Default is 0.9, meaning 90% of trainval data into trainset, 10% of trainval data in trainval into val set', type=float)
    args = parse.parse_args()
    gen_image_set(args.dataset_dir, args.trainval_ratio)