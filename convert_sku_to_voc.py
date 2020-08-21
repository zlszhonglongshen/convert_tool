import pandas as pd
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.dom import minidom
import argparse
import os.path as osp
from glob import glob
import shutil
import os

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def split_data(mainpath, annotations_path):
    import os
    ftrainval = open(osp.join(mainpath, 'trainval.txt'), 'w')
    ftest = open(osp.join(mainpath, 'test.txt'), 'w')
    ftrain = open(osp.join(mainpath, 'train.txt'), 'w')
    fval = open(osp.join(mainpath, 'val.txt'), 'w')

    files = os.listdir(annotations_path)
    for file in files:
        name = file[:-4] + '\n'
        if 'train' in file:
            ftrainval.write(name)
            ftrain.write(name)
        elif 'test' in file:
            ftrainval.write(name)
            ftest.write(name)
        else: fval.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='Convert SKU110K to VOC format!')
    parse.add_argument('-d', '--dataset_dir',
                       default='/mnt/ssd2/datasets/PRODUCT/SKU110K_fixed',
                       help='Path to SKU110K dataset directory', type=str)
    parse.add_argument('-o', '--output_dir',
                       default='/mnt/ssd2/Users/anhvn/SKU110K',
                       help='Path to output SKU110K VOC format', type=str)
    args = parse.parse_args()

    assert osp.isdir(args.dataset_dir), 'Invalid dataset directory !'
    os.makedirs(args.output_dir, exist_ok=True)

    # Copy image
    image_path = osp.join(args.output_dir, 'JPEGImages')
    if osp.exists(image_path): shutil.rmtree(image_path)
    shutil.copytree(osp.join(args.dataset_dir, 'images'), image_path)

    # Create annotation & image set
    annotations_path = osp.join(args.output_dir, 'Annotations')
    os.makedirs(annotations_path, exist_ok=True)
    for csv_path in glob(osp.join(args.dataset_dir, 'annotations', '*.csv')):
        sku = pd.read_csv(csv_path, header=None)
        csv_name = osp.basename(csv_path).split('_')[-1][:-4]
        prev_name = ''
        for row in sku.itertuples():
            name = row[1]
            bbox = str(row[2]), str(row[3]), str(row[4]), str(row[5])
            tag = row[6]
            if (prev_name != name):
                if prev_name != '':
                    xml_name = prev_name.replace('jpg', 'xml')
                    with open(osp.join(annotations_path, xml_name), 'w') as f:
                        f.write(prettify(root))

                # New xml file
                root = ET.Element('annotation')
                ET.SubElement(root, 'folder').text = 'SKU_110K'
                ET.SubElement(root, 'filename').text = name
                ET.SubElement(root, 'path').text = osp.join(image_path, name)
                source = ET.SubElement(root, 'source')
                ET.SubElement(source, 'database').text = 'Unknown'
                size = ET.SubElement(root, 'size')
                ET.SubElement(size, 'width').text = str(row[7])
                ET.SubElement(size, 'height').text = str(row[8])
                ET.SubElement(size, 'depth').text = '3'
                ET.SubElement(root, 'segmented').text = '0'
                prev_name = name

            member = ET.SubElement(root, 'object')
            ET.SubElement(member,'name').text = tag
            ET.SubElement(member,'pose').text = 'Unspecified'
            ET.SubElement(member,'truncated').text = '0'
            ET.SubElement(member,'difficult').text = '0'
            bndbox = ET.SubElement(member, 'bndbox')
            ET.SubElement(bndbox, 'xmin').text = bbox[0]
            ET.SubElement(bndbox, 'ymin').text = bbox[1]
            ET.SubElement(bndbox, 'xmax').text = bbox[2]
            ET.SubElement(bndbox, 'ymax').text = bbox[3]

        xml_name = prev_name.replace('jpg', 'xml')
        with open(osp.join(annotations_path, xml_name), 'w') as f:
            f.write(prettify(root))

    # Split image set
    mainpath = osp.join(args.output_dir, 'ImageSets', 'Main')
    os.makedirs(mainpath, exist_ok=True)
    split_data(mainpath, annotations_path)
