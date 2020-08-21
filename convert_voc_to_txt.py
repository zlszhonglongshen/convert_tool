# coding: utf-8
import xml.etree.ElementTree as ET
import argparse
import os.path as osp

def parse_xml(xml_path):
    tree = ET.parse(xml_path)
    img_path = xml_path.replace('Annotations', 'JPEGImages').replace('xml', 'jpg')
    height = tree.findtext("./size/height")
    width = tree.findtext("./size/width")

    objects = [img_path, width, height]

    for obj in tree.findall('object'):
        difficult = obj.find('difficult').text
        if difficult == '1':
            continue
        name = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = bbox.find('xmin').text
        ymin = bbox.find('ymin').text
        xmax = bbox.find('xmax').text
        ymax = bbox.find('ymax').text

        name = str(names_dict[name])
        objects.extend([name, float(xmin), float(ymin), float(xmax), float(ymax)])
    if len(objects) > 1:
        return objects
    else:
        return None

def gen_anno_txt(image_set, txt_name):
    lines = open(image_set, 'r').readlines()
    f = open(txt_name, 'w')
    basepath = osp.dirname(osp.dirname(osp.dirname(image_set)))
    img_index = 0
    for line in lines:
        line = line.strip()
        xml_path = osp.join(basepath, 'Annotations', line + '.xml')
        objects = parse_xml(xml_path)
        objects.insert(0, str(img_index))
        img_index += 1
        objects = ' '.join(objects) + '\n'
        f.write(objects)
    f.close()

def cls_to_dict(class_path):
    cls_dict = {}
    lines = open(class_path, 'r').readlines()
    cnt = 0
    for line in lines:
        line = line.strip()
        cls_dict[line] = cnt
        cnt += 1
    return cls_dict

if __name__ == '__main__':
    # Initiate argument parser
    parser = argparse.ArgumentParser(
        description="Parse XML in VOC format to file txt")
    parser.add_argument("-i",
                        "--image_set",
                        default='train.txt',
                        help="Path to the .txt set file are stored",
                        type=str)
    parser.add_argument("-n",
                        "--class_path",
                        default='coco.names',
                        help="Path to the class name file",
                        type=str)
    parser.add_argument("-o",
                        "--output_txt",
                        help="Name of output .txt file",
                        type=str)
    args = parser.parse_args()

    names_dict = cls_to_dict(args.class_path)

    assert osp.exists(args.image_set), 'Invalid image set path'

    if args.output_txt is None:
        txt_name = osp.basename(args.image_set) + '_yolo.txt'
    else: txt_name = args.output_txt
    gen_anno_txt(args.image_set, txt_name)






