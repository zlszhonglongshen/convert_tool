#!/usr/bin/python

# pip install lxml

import sys
import os
import json
import xml.etree.ElementTree as ET
import glob
import argparse
import os.path as osp
import shutil
import cv2

PRE_DEFINE_CATEGORIES = {'person': 1}
START_BOUNDING_BOX_ID = 1

# If necessary, pre-define category and its id
#  PRE_DEFINE_CATEGORIES = {"aeroplane": 1, "bicycle": 2, "bird": 3, "boat": 4,
#  "bottle":5, "bus": 6, "car": 7, "cat": 8, "chair": 9,
#  "cow": 10, "diningtable": 11, "dog": 12, "horse": 13,
#  "motorbike": 14, "person": 15, "pottedplant": 16,
#  "sheep": 17, "sofa": 18, "train": 19, "tvmonitor": 20}


def get(root, name):
    vars = root.findall(name)
    return vars


def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise ValueError("Can not find %s in %s." % (name, root.tag))
    if length > 0 and len(vars) != length:
        raise ValueError(
            "The size of %s is supposed to be %d, but is %d."
            % (name, length, len(vars))
        )
    if length == 1:
        vars = vars[0]
    return vars


def get_filename_as_int(filename):
    try:
        filename = filename.replace("\\", "/")
        filename = osp.splitext(os.path.basename(filename))[0]
        return int(filename)
    except:
        raise ValueError("Filename %s is supposed to be an integer." % (filename))


def get_categories(xml_files):
    """Generate category name to id mapping from a list of xml files.

    Arguments:
        xml_files {list} -- A list of xml file paths.

    Returns:
        dict -- category name to id mapping.
    """
    classes_names = []
    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall("object"):
            if member[0].text not in classes_names:
                classes_names.append(member[0].text)
    classes_names = list(set(classes_names))
    classes_names.sort()
    return {name: i for i, name in enumerate(classes_names)}


def convert(xml_files, json_file):
    json_dict = {"images": [], "type": "instances", "annotations": [], "categories": []}
    if PRE_DEFINE_CATEGORIES is not None:
        categories = PRE_DEFINE_CATEGORIES
    else:
        categories = get_categories(xml_files)
    print('CLASSES in {} set : {}'.format(osp.basename(json_file), categories))
    bnd_id = START_BOUNDING_BOX_ID
    cnt_small = 0
    cnt = 0
    for _image_id, xml_file in enumerate(xml_files):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        filename_xml = osp.basename(xml_file)
        filename = filename_xml.replace('xml', 'jpg')
        image_id = _image_id
        size = get_and_check(root, "size", 1)
        width = int(get_and_check(size, "width", 1).text)
        height = int(get_and_check(size, "height", 1).text)
        jpg_path = osp.join(voc_path, 'JPEGImages', filename)
        if osp.basename(json_file) == 'instances_test.json':
            shutil.copyfile(jpg_path, osp.join(coco_path, 'test', filename))
        img = cv2.imread(jpg_path)

        real_width, real_height = img.shape[1], img.shape[0]
        assert (width == real_width) and (height == real_height), 'Different shape between image and annotation !'
        image = {
            "file_name": filename,
            "height": height,
            "width": width,
            "id": image_id,
        }
        json_dict["images"].append(image)
        for obj in tree.findall('object'):
            category = obj.find('name').text
            if category != 'person': continue
            category_id = categories[category]
            xmin = float(obj.find('bndbox').find('xmin').text)
            ymin = float(obj.find('bndbox').find('ymin').text)
            xmax = float(obj.find('bndbox').find('xmax').text)
            ymax = float(obj.find('bndbox').find('ymax').text)
            assert (xmax > xmin) and (ymax > ymin), 'Invalid bounding box size !'
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            cnt += 1
            if o_height * o_width < 1024:
                cnt_small += 1
            ann = {
                "area": o_width * o_height,
                "iscrowd": 0,
                "image_id": image_id,
                "bbox": [xmin, ymin, o_width, o_height],
                "category_id": category_id,
                "id": bnd_id,
                "ignore": 0,
                "segmentation": [],
            }
            json_dict["annotations"].append(ann)
            bnd_id = bnd_id + 1

    for cate, cid in categories.items():
        cat = {"supercategory": "none", "id": cid, "name": cate}
        json_dict["categories"].append(cat)

    print("count_small / cnt: {}/{}".format(cnt_small, cnt))
    json_fp = open(json_file, "w")
    json_str = json.dumps(json_dict)
    json_fp.write(json_str)
    json_fp.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Pascal VOC annotation to COCO format."
    )
    parser.add_argument("voc_dir", help="path to dataset VOC format", type=str)
    parser.add_argument("coco_dir", help="path to output annotation dir of  COCO format", type=str)
    args = parser.parse_args()
    voc_path = args.voc_dir
    coco_path = args.coco_dir
    for img_set in glob.glob(osp.join(voc_path, 'ImageSets', 'Main', '*.txt')):
        with open(img_set, "r") as f:
            xml_files = f.read().splitlines()
        print("Number of xml files in {}: {}".format(osp.basename(img_set), len(xml_files)))
        xml_files = [osp.join(voc_path, 'Annotations', x + '.xml') for x in xml_files]
        json_file = 'instances_{}.json'.format(osp.basename(img_set)[:-4])
#        if osp.basename(img_set)[:-4] != 'test': continue
        convert(xml_files, osp.join(args.coco_dir, 'annotations', json_file))
        print("Successfully converted : {}".format(json_file))
