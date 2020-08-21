import os
import os.path as osp
from glob import glob
import argparse
import cv2
import xml.etree.ElementTree as ET
import shutil

def xml_to_reid(xml_dir, img_dir):
    for xml_path in glob(osp.join(xml_dir, '*.xml')):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        img_path = xml_path.replace('.xml', '.jpg')
        img_name = osp.basename(img_path)[0:-4]
        img = cv2.imread(img_path)
        cnt = 0
        for member in root.findall('object'):
            if member[4].tag == 'difficult': idx = 5
            else: idx = 4
            label = member[0].text
            xmin = int(member[idx][0].text)
            ymin = int(member[idx][1].text)
            xmax = int(member[idx][2].text)
            ymax = int(member[idx][3].text)
            new_img = img[ymin:ymax, xmin:xmax]
            new_img_name = '_'.join([label, img_name, '{:02}'.format(cnt)]) + '.jpg'
            new_img_path = osp.join(img_dir, new_img_name)
            cv2.imwrite(new_img_path, new_img)
            cnt += 1

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='From VOC .xml & correspond .jpg file, to generate cropped image (has format name: <label>_<img_name>_<bbox_id> for ReID dataset !')
    parse.add_argument('-i', '--input_dir', help='Path to folder contains xml files', type=str)
    parse.add_argument('-o', '--output_dir', help='Path to output folder contains cropped bbox images from xml files', type=str)
    args = parse.parse_args()

    assert osp.isdir(args.input_dir), 'Input directory does not found !'
    if osp.isdir(args.output_dir): shutil.rmtree(args.output_dir)
    os.mkdir(args.output_dir)
    xml_to_reid(args.input_dir, args.output_dir)