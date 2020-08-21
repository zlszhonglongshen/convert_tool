import argparse
import os
import os.path as osp
import cv2
import shutil

def extract_vid(src_path, out_dir, period=1):
    assert osp.exists(src_path), 'Source file not found !'
    vid = cv2.VideoCapture(src_path)
    if osp.exists(out_dir):
        shutil.rmtree(out_dir)
    os.mkdir(out_dir)
    cnt = 0
    while vid.isOpened():
        _, img = vid.read()
        if img is None: break
        if cnt % period == 0:
            img_name = '{:05n}.jpg'.format(cnt)
            img_path = osp.join(out_dir, img_name)
            cv2.imwrite(img_path, img)
            cnt += 1
    vid.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script for extract frames from video !')
    parser.add_argument("-i", "--video_input", type=str, default="CAM_360.mp4", help="Path to video source")
    parser.add_argument("-o", "--ouput_dir", type=str, default="./output", help="Path to output folder contains extracted frames")
    parser.add_argument("-p", "--period", type=str, default=1, help="Period to extract frame")
    args = parser.parse_args()
    extract_vid(args.video_input, args.ouput_dir, args.period)