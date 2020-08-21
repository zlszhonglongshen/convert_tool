# New xml file
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
from xml.dom import minidom
import os
import cv2

def prettify(elem):

    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def get_data(img,frame_name,width,height,trackers,des_folder):
    """Create dataset from detection and tracking with sort

            img: img_file after read by cv2.imread()
            frame_name: name of img and xml file( img and xml must be have same name)
            with, height: of img
            trackers: numpy array trackers in the current frame format [x_min,y_min,x_max,y_max, local_id]
            des_folder: path to the folder you want to save datasets

            """
    root = ET.Element('annotation')
    name = frame_name
    ET.SubElement(root, 'folder').text = '360_tracking_dataset'
    ET.SubElement(root, 'filename').text = name
    ET.SubElement(root, 'path').text = '/mnt/hdd10tb/Users/anhvn/360_tracking_dataset/images/' + name
    source = ET.SubElement(root, 'source')
    ET.SubElement(source, 'database').text = 'Unknown'
    size = ET.SubElement(root, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = '3'
    ET.SubElement(root, 'segmented').text = '0'
    for trk in trackers:
            member = ET.SubElement(root, 'object')
            ET.SubElement(member,'name').text = str(int(trk[4]))
            ET.SubElement(member,'pose').text = 'Unspecified'
            ET.SubElement(member,'truncated').text = '0'
            ET.SubElement(member,'difficult').text = '0'
            bndbox = ET.SubElement(member, 'bndbox')
            ET.SubElement(bndbox, 'xmin').text = str(trk[0])
            ET.SubElement(bndbox, 'ymin').text = str(trk[1])
            ET.SubElement(bndbox, 'xmax').text = str(trk[2])
            ET.SubElement(bndbox, 'ymax').text = str(trk[3])
    xml_file = os.path.join(des_folder,'{}.xml'.format(frame_name))
    img_file = os.path.join(des_folder,'{}.jpg'.format(frame_name))
    with open(xml_file, 'w') as f: f.write(prettify(root))
    cv2.imwrite(img_file,img)
