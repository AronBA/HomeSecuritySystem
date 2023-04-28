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
import Messengers.SMS_Message as sms
import Messengers.Email_Message as email
import logging

# ------------------------important for development environment------------------------------------
env_debug = True  # True = debug information in console
env_local = True  # True = your own camera gets used and not those in the network
env_production = False  # True = you will actually send sms and email (this costs money)
# -------------------------------------------------------------------------------------------------

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


def play_sound():
    if not env_local:
        playsound(sound=path_sound)
    logging.debug('Played Sound')


def print_debug():
    logging.debug(f'''
    ----------------------------------
    |          Variables              |
    ----------------------------------
    env_debug: {env_debug}
    env_local: {env_local} 
    env_production: {env_production} 
    relais_on: {relais_on} 
    relais_on_duration: {relais_on_duration} seconds
    path_executable: {path_executable} 
    path_sound: {path_sound} 
    motion_detected: {motion_detected} 
    motion_detection_cooldown: {motion_detection_cooldown}
    motion_frame_counter: {motion_frame_counter} 
    motion_detection_threshold: {motion_detection_threshold} 
    motion_last_time: {motion_last_time} 
    motion_previous_time: {motion_previous_time} 
    url_relais_on: {url_relais_on}
    url_relais_off: {url_relais_off}
    url_open_website: {url_open_website}
    url_camera_1: {url_camera_1}
    url_camera_2: {url_camera_2}
    ----------------------------------
    ''')


def play_relais():
    global relais_on
    relais_on = True
    if not env_local:
        os.startfile(path_executable)
        requests.get(url_relais_on)
        webbrowser.open(url_open_website)
    logging.debug('Activated Relais')


# this will change some variables depended on the environment
if env_debug:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
if env_local:

    tkinter.messagebox.showwarning(title="Alert",
                                   message="You are using the local version! Only use for local development")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
else:
    if env_production:
        tkinter.messagebox.showwarning(title="Alert",
                                       message="You are using the Production version! Only use to demonstrate ALL functions")
    else:
        tkinter.messagebox.showwarning(title="Alert",
                                       message="You are using the Class version! Only use for in class development")
    cap = cv2.VideoCapture(url_camera_1)
    cap2 = cv2.VideoCapture(url_camera_2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

logging.info("Program starting..")

print_debug()

logging.info("Program running...")

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
                #logging.debug('Detected Motion') #only use for crazy debugging
                continue
            motion_detected = True

    # this will trigger all actions when a new motion is detected
    if motion_detected and time.time() > motion_previous_time + motion_detection_cooldown:
        logging.info("Detected a Motion")
        if not env_local and env_production:
            sms.sendSMS("", 2, "hi")
            logging.debug("Send SmS")
            email.sendemail(1, email.mainReceiver, email.mainSender, email.mainMsg,
                            "Motion detected by security system")
            logging.debug('Send Email')
        threading.Thread(target=play_sound, daemon=True).start()
        threading.Thread(target=play_relais, daemon=True).start()
        motion_previous_time = time.time()
        motion_detected = True
        continue
    # this will deactivate the relais after n amount of time
    if motion_previous_time + relais_on_duration <= time.time() and relais_on:
        relais_on = False
        if not env_local:
            requests.get(url_relais_off)
        logging.debug('Deactivated Relais')
    # this will break the loop
    if cv2.waitKey(1) == ord('q'):
        break

    motion_frame_counter += 1

logging.info("Program shutdown...")
cap.release()
cv2.destroyAllWindows()
