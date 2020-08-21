import xml.etree.ElementTree as etree
import os
from glob import glob
import argparse


def main():
    parser = argparse.ArgumentParser(
                        description="XML-to-TXT converter")
    parser.add_argument("-i",
                        "--inputDir",
                        default="test",
                        help="Path to the folder where the input .xml files are stored",
                        type=str)
    parser.add_argument("-o",
                        "--outputDir",
                        default="groundtruths",
                        help="Path to the folder where the correspond output .txt file are stored", type=str)

    args = parser.parse_args()
    # path to annotations folder
    INPUT_PATH = args.inputDir
    # path to groundtruth folder
    OUTPUT_PATH = args.outputDir
    assert (os.path.isdir(args.inputDir))
    assert (os.path.isdir(args.outputDir))
    for annotation in glob(INPUT_PATH + '*.xml'):
        filename = annotation.replace(INPUT_PATH, '')
        filename = filename.replace('xml', 'txt')
        print(filename)
        res_path = os.path.join(OUTPUT_PATH, filename)
        res_file = open(res_path, 'w+')
        print(annotation)
        tree = etree.parse(annotation)
        root = tree.getroot()
        for country in root.findall('object'):
            name = country.find('name').text
            x_min = float(country.find('bndbox').find('xmin').text)
            y_min = float(country.find('bndbox').find('ymin').text)
            # w = float(country.find('bndbox').find('xmax').text) - float(country.find('bndbox').find('xmin').text)
            # h = float(country.find('bndbox').find('ymax').text) - float(country.find('bndbox').find('ymin').text)
            x_max = float(country.find('bndbox').find('xmax').text)
            y_mmax = float(country.find('bndbox').find('ymax').text)
            if name == 'person':
                line = 'person {} {} {} {}'.format(x_min, y_min, x_max, y_mmax)
                res_file.write(line + os.linesep)

    print('Successfully converted xml to txt.')

if __name__ == "__main__":
    main()


