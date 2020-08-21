from multiprocessing import Process
import os
import cv2
import argparse


def set_cam(cam_id, rtsp, fps):
    return {"CAM_ID": cam_id, "RTSP_URL": rtsp, "FPS": fps}


def get_evidence_cams():
    evidence_cams = dict()
    # CAM_ENTRANCE
    evidence_cams['CAM_ENTRANCE'] = set_cam(ID_CAM_ENTRANCE, RTSP_CAM_ENTRANCE, FPS_CAM_IP)
    # CAM_EXIT
    evidence_cams['CAM_EXIT'] = set_cam(ID_CAM_EXIT, RTSP_CAM_EXIT, FPS_CAM_IP)
    # CAM_WALL_01
    evidence_cams['CAM_LEFT'] = set_cam(ID_CAM_LEFT, RTSP_CAM_LEFT, FPS_CAM_IP)
    # CAM_WALL_02
    evidence_cams['CAM_RIGHT'] = set_cam(ID_CAM_RIGHT, RTSP_CAM_RIGHT, FPS_CAM_IP)
    return evidence_cams


def get_engine_cams():
    engine_cams = dict()
    # CAM_360
    engine_cams['CAM_360'] = set_cam(ID_CAM_360, RTSP_CAM_360, FPS_CAM_360)
    # CAM_SHELF_01
    engine_cams['CAM_SHELF_01'] = set_cam(ID_CAM_SHELF_01, RTSP_CAM_SHELF_01, FPS_CAM_IP)
    # CAM_SHELF_02
    engine_cams['CAM_SHELF_02'] = set_cam(ID_CAM_SHELF_02, RTSP_CAM_SHELF_02, FPS_CAM_IP)
    # CAM_SHELF_03
    engine_cams['CAM_SHELF_03'] = set_cam(ID_CAM_SHELF_03, RTSP_CAM_SHELF_03, FPS_CAM_IP)
    return engine_cams


def save_video(rtsp_url, cam_type, scenario_name):
    vid = cv2.VideoCapture(rtsp_url)
    if cam_type == 'CAM_360':
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    else:
        fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    output_path = scenario_name + '/' + cam_type + '.mp4'
    videoWriter = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    print('Recording video from {} to ./{}'.format(cam_type, output_path))
    while vid.isOpened():
        _, img = vid.read()
        videoWriter.write(img)
    videoWriter.release()
    vid.release()


# ID CAM ENGINE
ID_CAM_360 = 'b53729f9-d1b8-9d25-1fbc-8ee357e2d630'
ID_CAM_SHELF_01 = 'cbd3ca1e-df48-1ba9-ccc3-f6657a27cab3'
ID_CAM_SHELF_02 = '7fc151d9-8ece-3ddc-8365-575ab789284c'
ID_CAM_SHELF_03 = '22d517aa-94fe-df1f-6862-a45c688d67d2'

# ID CAM EVIDENCE
ID_CAM_ENTRANCE = '5f6bec33-bc41-e2ea-e885-eb5bbd11a60c'
ID_CAM_EXIT = 'e13dfbde-f765-cc39-e07c-3b17ebafe939'
ID_CAM_LEFT = '128c9a24-e1ab-ad72-d6c0-798f2ab7e4da'
ID_CAM_RIGHT = '0106d45f-4adc-d780-ff92-93a31c9d6c73'

# STREAM FPS
FPS_CAM_360 = 25
FPS_CAM_IP = 15

# RTSP CONFIG
RTSP_CAM_360 = 'rtsp://admin:123456a@@192.168.8.127:554/Streaming/Channels/2/'
RTSP_CAM_SHELF_01 = 'rtsp://admin:admin@192.168.8.122:554/stream2'
RTSP_CAM_SHELF_02 = 'rtsp://admin:admin@192.168.8.123:554/stream2'
RTSP_CAM_SHELF_03 = 'rtsp://admin:admin@192.168.8.124:554/stream2'
RTSP_CAM_ENTRANCE = 'rtsp://admin:admin@192.168.8.121:554/stream2'
RTSP_CAM_EXIT = 'rtsp://admin:admin@192.168.8.120:554/stream2'
RTSP_CAM_LEFT = 'rtsp://admin:admin@192.168.8.126:554/stream2'
RTSP_CAM_RIGHT = 'rtsp://admin:admin@192.168.8.125:554/stream2'

parser = argparse.ArgumentParser(description="Script for recording scenario of AWL Demo room in format <cam_type>.mp4")
parser.add_argument("scenario_dir", type=str, default='scenario01', help="The path to save <cam_type>.mp4 to dir")
args = parser.parse_args()
scenario_dir = args.scenario_dir
if not os.path.isdir(scenario_dir):
    os.mkdir(scenario_dir)

engine_cams = get_engine_cams()
evidence_cams = get_evidence_cams()
list_processes = []
for cam_type in engine_cams:
    rtsp_url = engine_cams[cam_type]['RTSP_URL']
    p = Process(target=save_video, args=(rtsp_url, cam_type, scenario_dir))
    list_processes.append(p)

for cam_type in evidence_cams:
    rtsp_url = evidence_cams[cam_type]['RTSP_URL']
    p = Process(target=save_video, args=(rtsp_url, cam_type, scenario_dir))
    list_processes.append(p)

print('Start recording scenario! Press Ctrl + C to stop recording ...')
for process in list_processes:
    process.start()

for process in list_processes:
    process.join()