import tkinter.messagebox
import cv2
import webbrowser
import time
import os
from configparser import ConfigParser
import numpy as np
import threading
from playsound import playsound
import requests
import Messangers.SMS_Message as sms
import Messangers.Email_Message as email

# variables
env_local = True
env_production = False

relais_on = False
relais_on_duration = 5
config = ConfigParser()

path_executable = ""
path_sound = "sound.mp3"

motion_detected = False
motion_detection_cooldown = 5
motion_frame_counter = 0
motion_detection_threshold = 10000
motion_last_time = 0
motion_previous_time = 0

url_relais_on = "http://192.168.1.4/30000/01"
url_relais_off = "http://192.168.1.4/30000/00"
url_open_website = "https://youtube.com"
url_camera_1 = "rtsp://admin:admin@192.168.1.96:554"
url_camera_2 = "rtsp://admin:admin@192.168.1.92:554"


# functions
def play_sound():
    if not env_local:
        playsound(sound=path_sound)
    print("sound played")


def play_relais():
    global relais_on
    relais_on = True
    if not env_local:
        os.startfile(path_executable)
        requests.get(url_relais_on)
        webbrowser.open(url_open_website)
    print("relais an")


# this will change some variables depended on the environment
if env_local:
    tkinter.messagebox.showwarning(title="Alert",
                                   message="You are ussing the Local version! Motiondetection will be logged but no action will be triggert")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
else:
    if env_production:
        tkinter.messagebox.showwarning(title="Alert",
                                       message="You are ussing the Production version! emails and sms messages will be sent")
    else:
        tkinter.messagebox.showwarning(title="Alert",
                                       message="You are ussing the School version! Only use this if you are in class")
    cap = cv2.VideoCapture(url_camera_1)
    cap2 = cv2.VideoCapture(url_camera_2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# main loop
while True:
    motion_detected = False

    if env_local:
        ret, frame = cap.read()
        cv2.imshow('Camera Feed', frame)
    else:
        ret, frame2 = cap2.read()
        ret, frame = cap.read()
        cv2.imshow('Camera Feed', np.concatenate((frame2, frame), 1))

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # this will reset the first frame after 30frames (improves accuracy)
    if motion_frame_counter == 0:
        first_frame = gray_frame
        motion_frame_counter += 1
        continue
    if motion_frame_counter == 30:
        first_frame = gray_frame
        motion_frame_counter = 0

    # this will compare two frames to determine if there is a motion
    if not motion_detected:
        frame_delta = cv2.absdiff(first_frame, gray_frame)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < motion_detection_threshold:
                continue
            motion_detected = True

    # this will trigger all actions when a new motion is detected
    if motion_detected and time.time() > motion_previous_time + motion_detection_cooldown:
        if not env_local and env_production:
            sms.sendSMS("+41779611539", 2, "hi")
            email.sendemail(1, email.mainReceiver, email.mainSender, email.mainMsg,
                            "Motion detected by security system")

        threading.Thread(target=play_sound, daemon=True).start()
        threading.Thread(target=play_relais, daemon=True).start()
        motion_previous_time = time.time()
        motion_detected = True
        print("Detected")
        continue
    # this will deactivate the relais after n amount of time
    if motion_previous_time + relais_on_duration <= time.time() and relais_on:
        relais_on = False
        if not env_local:
            requests.get(url_relais_off)
        print("deactivate relais")

    # this will break the loop
    if cv2.waitKey(1) == ord('q'):
        break

    motion_frame_counter += 1

# cleanup
cap.release()
cv2.destroyAllWindows()
