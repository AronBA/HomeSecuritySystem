import cv2
import Camera
import json
import os
from parser.fileParser import getProjFile

path = getProjFile('settings.json')
camerasettings = []
camerasinstances = []
f = open(path, "r")
data = json.load(f)

for cam in data["cameras"]:

    alarms = []
    alarmsid = cam["alarms"]
    devices = []

    for aid in alarmsid:
        for alarm in data["alarms"]:
            if aid == alarm["id"]:
                alarms.append(alarm)




    camera = [cam["ip"],cam["name"],alarms]


    camerasettings.append(camera)




for i in camerasettings:
    camerasinstances.append(Camera.Camera(camera_adress=i[0],camera_name=i[1],camera_alarms=i[2],dev=data["devices"],motion_detection_threshold=data["settings"]["threshold"],motion_detection_cooldown=data["settings"]["delay"],path_sound_file=""))

def showcamerastream():
    for camera in camerasinstances:
        cv2.imshow(f'Camera Feed {camera.id}', camera.frame)


while True:

    motion_detected = False

    for camera in camerasinstances:
        camera.checkmotion()
    showcamerastream()
    if cv2.waitKey(1) == ord('q'):
        break

for camera in camerasinstances:
    print(f"Camera {camera.id} destroyed")
    camera.cap.release()
    cv2.destroyAllWindows()
