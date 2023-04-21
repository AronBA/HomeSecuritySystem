import cv2
import webbrowser
import time
import os
from configparser import ConfigParser
import numpy as np
import threading
from playsound import playsound
import requests


relaisstate = False

config = ConfigParser()

in1 = 16

def sound():
    print("soundss")
    playsound(sound="sound.mp3")
def relais():
    global relaisstate
    relaisstate = True

    #os.startfile(filepath)
    print("relais an")
    requests.get("http://192.168.1.4/30000/01")


    # webbrowser.open("https://youtube.com")







config.read("settings.ini")


cap = cv2.VideoCapture("rtsp://admin:admin@192.168.1.96:554")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

cap2 = cv2.VideoCapture("rtsp://admin:admin@192.168.1.92:554")

cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

filepath = ""

motion_detected = False

motion_delay = 5
motion_counter = 0
motion_threshold = 10000
last_motion_time = 0
prev_motion_time = 0


while True:
    motion_detected = False




    ret, frame = cap.read()
    ret, frame2 = cap2.read()
    cv2.imshow('Camera Feed', np.concatenate((frame2,frame), 1))
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if motion_counter == 0:
        first_frame = gray_frame
        motion_counter += 1
        continue

    if motion_counter == 30:
        first_frame = gray_frame
        motion_counter = 0

    if not motion_detected:
        frame_delta = cv2.absdiff(first_frame, gray_frame)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < motion_threshold:
                continue
            motion_detected = True

    if motion_detected and time.time() > prev_motion_time + motion_delay:
        print("Detected")

        threading.Thread(target=sound, daemon=True).start()
        threading.Thread(target=relais, daemon=True).start()

        prev_motion_time = time.time()
        motion_detected = True
        continue






    if prev_motion_time + 5 <= time.time() and relaisstate:
        relaisstate = False
        print("deactivate relais")
        requests.get("http://192.168.1.4/30000/00")

    if cv2.waitKey(1) == ord('q'):

        break



    motion_counter += 1

cap.release()
cv2.destroyAllWindows()




