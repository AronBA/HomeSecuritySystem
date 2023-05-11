import cv2
import time
import threading
import playsound
import requests

import Messengers.SMS_Message
import Messengers.Email_Message
import Relais


class Camera:
    amountofcameras = 0

    def __init__(self, camera_adress=0, path_sound_file="", relais=0, relais_active_duration=5, motion_detection_cooldown=5,
                 motion_detection_threshold=1000, mail_recipient="", sms_recipient="", sms_message="", email_message=""):

        self.sms_message = sms_message
        self.email_message = email_message
        self.sms_recipient = sms_recipient
        self.mail_recipient = mail_recipient
        Camera.amountofcameras += 1

        self.frame = None
        self.first_frame = 0
        self.motion_frame_counter = 0

        self.url_relais_on = f"http://192.168.1.4/30000/{relais}"
        self.url_relais_off = f"http://192.168.1.4/30000/{relais + 1}"

        self.id = Camera.amountofcameras
        self.camera_adress = camera_adress
        self.path_sound_file = path_sound_file
        self.relais = relais
        self.relais_active = False
        self.relais_active_duration = relais_active_duration

        self.motion_previous_time = 0
        self.motion_detection_cooldown = motion_detection_cooldown
        self.motion_detected = False
        self.motion_detection_threshold = motion_detection_threshold
        self.motion_last_time = 0

        self.cap = cv2.VideoCapture(camera_adress)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print(f"Created camera nr.{self.id}")

    def activateSound(self):
        # playsound.playsound(self.path_sound_file)
        print(f"Camera {self.id} played sound")

    def activateRelais(self):
        # requests.get(self.url_relais_on)
        print(f"Camera {self.id} activated relais")

    def deactivateRelais(self):
        # requests.get(self.url_relais_off)
        print(f"Camera {self.id} deactivated relais")

    def sendsms(self):
        # Messengers.SMS_Message.sendSMS()
        print(f"Camera {self.id} deactivated relais")

    def sendemail(self):
        # Messengers.Email_Message.sendemail()
        print(f"Camera {self.id} send email")

    def resetFrame(self):
        self.first_frame = self.gray_frame

    def checkmotion(self):
        motion_detected = False
        ret, self.frame = self.cap.read()

        gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        if self.motion_frame_counter == 0:
            self.first_frame = gray_frame
            self.motion_frame_counter += 1
            return

        if self.motion_frame_counter == 30:
            self.first_frame = gray_frame
            self.motion_frame_counter = 0

        # this will compare two frames to determine if there is a motion
        if not motion_detected:

            frame_delta = cv2.absdiff(self.first_frame, gray_frame)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                if cv2.contourArea(contour) < self.motion_detection_threshold:
                    continue
                motion_detected = True

        # this will trigger all actions when a new motion is detected
        if motion_detected and time.time() > self.motion_previous_time + self.motion_detection_cooldown:
            threading.Thread(target=self.activateSound, daemon=True).start()
            threading.Thread(target=self.activateRelais, daemon=True).start()
            threading.Thread(target=self.sendsms, daemon=True).start()
            threading.Thread(target=self.sendemail, daemon=True).start()

            self.motion_previous_time = time.time()
            self.motion_detected = True

        # this will deactivate the relais after n amount of time
        if self.motion_previous_time + self.relais_active_duration <= time.time() and self.relais_active:
            self.relais_active = False
            self.deactivateRelais()

        self.motion_frame_counter += 1
