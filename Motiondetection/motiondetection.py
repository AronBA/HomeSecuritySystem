import cv2
import Camera
import json

camerasettings = [0]
camerasinstances = []

for i in camerasettings:
    camerasinstances.append(Camera.Camera(camera_adress=i,path_sound_file="",relais=1,relais_active_duration=5,motion_detection_cooldown=5,motion_detection_threshold=1000))


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
