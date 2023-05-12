import datetime
import cv2
import time
import playsound
import requests
import vonage
import json
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib

path = os.path.dirname(os.getcwd()) + '/Files/haarcascade_upperbody.xml'
human_cascade = cv2.CascadeClassifier(path)

class Camera:
    amountofcameras = 0

    def __init__(self, camera_adress, path_sound_file, motion_detection_cooldown,motion_detection_threshold,camera_alarms, camera_name, dev, deviceturnoff=[]):
        self.gray = None
        self.ret = None
        self.relais_active_duration = 5
        self.camera_alarms = camera_alarms
        self.dev = dev
        Camera.amountofcameras += 1
        self.camera_name = camera_name
        self.frame = None
        self.first_frame = 0
        self.motion_frame_counter = 0

        self.id = Camera.amountofcameras
        self.camera_adress = camera_adress
        self.path_sound_file = path_sound_file

        self.data = json.load(open(os.path.dirname(os.getcwd()) + '/settings.json'))
        client = vonage.Client(key=self.data["sms"]["smsSecret"], secret=self.data["sms"]["smsSecret"])
        self.sms = vonage.Sms(client=client)
        self.Srecipient = self.data["sms"]["smsNumber"]
        self.Smsg = self.data["sms"]["smsText"]

        self.password = self.data["Email"]["password"]
        self.receiver = self.data["Email"]["receiver"]
        self.sender = "modul0426@gmail.com"
        self.msg = self.data["Email"]["content"]
        self.subject = self.data["Email"]["subject"]

        self.relais_active = False

        self.motion_previous_time = 0
        self.motion_detection_cooldown = int(motion_detection_cooldown)
        self.motion_detected = False
        self.motion_detection_threshold = int(motion_detection_threshold)
        self.motion_last_time = 0
        self.deviceturnoff = deviceturnoff
        self.cap = cv2.VideoCapture(camera_adress)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print(f"Created camera nr.{self.id}")
        print(f"Camera ip{self.camera_adress}")

    def activateSound(self):
        playsound("sus.mp3")
        print(f"Camera {self.id} played sound")

    def checkHuman(self):
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        # Detect humans in the frame using the Haar Cascade classifier
        humans = human_cascade.detectMultiScale(self.gray, scaleFactor=1.1, minNeighbors=1, minSize=(10, 10),
                                                maxSize=(10000, 10000))

        # Draw a bounding box around each detected human
        for (x, y, w, h) in humans:
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        return len(humans) > 0

    def sendemail(self, imgPath: str = ""):
        em = MIMEMultipart('alternative')
        em['from'] = self.sender
        em['To'] = self.receiver
        em['Subject'] = self.subject

        if imgPath != "":
            with open(os.path.dirname(os.getcwd()) + "/" + imgPath, "rb") as IF:
                try:
                    f = IF.read()
                    image = bytes(f)
                except Exception:
                    raise Exception

            text = MIMEText(f"""<p>*******************************************</p>
        <p>There was motion detected by {self.camera_name}</p>
        <p>*******************************************</p>
        <p>{self.msg}</p>
        <img src="cid:attachedImg">
        """, 'html')
            em.attach(text)
            img = MIMEImage(image)
            img.add_header('Content-ID', 'attachedImg')
            em.attach(img)
        else:
            text = MIMEText(f"""<p>*******************************************</p>
                <p>There was motion detected by {self.camera_name}</p>
                <p>*******************************************</p>
                <p>{self.msg}</p>
                """, 'html')
            em.attach(text)

        for cam in self.data["Cameras"]:
            if cam["name"] == self.camera_name:
                for alarms in cam["alarms"]:
                    for alarm in self.data["alarms"]:
                        if alarm["id"] == alarms:
                            if alarm["email"]:
                                context = ssl.create_default_context()

                                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                    smtp.login(self.sender, self.password)
                                    smtp.sendmail(self.sender, self.receiver, em.as_string())

    def sendSMS(self):
        params = {
            "from": "C.A.S",
            "to": self.Srecipient,
            "text": f"""
    ********************************
    Motion detected by {self.camera_name}
    ********************************
    {self.Smsg}
    """,
        }
        for cam in self.data["Cameras"]:
            if cam["name"] == self.camera_name:
                for alarms in cam["alarms"]:
                    for alarm in self.data["alarms"]:
                        if alarm["id"] == alarms:
                            if alarm["sms"]:
                                response = self.sms.send_message(params)

                                if response["messages"][0]["status"] == "0":
                                    print("Message Details: ", response)
                                    print("Message sent successfully.")
                                else:
                                    print(f"Message failed with error: {response['messages'][0]['error-text']}")

    def takePhoto(self):
        timestamp = str(datetime.datetime.now()).split(":")
        temp = timestamp
        timestamp = ""
        for i in temp:
            timestamp += i + "-"
        timestamp = timestamp[:-1]
        p = os.path.dirname(os.getcwd()) + f"{timestamp}_{self.camera_name}.png"
        val = cv2.imwrite(p, self.frame)
        print("took photo" + f" {val}")
        return timestamp

    def activateRelais(self,idrelais):
        requests.get(f"http://192.168.1.4/30000/0{idrelais}")
        print(f"Camera {self.id} activated relais")

    def deactivateRelais(self,idrelais):
        isroug = int(idrelais) - 1
        print(isroug)
        requests.get(f"http://192.168.1.4/30000/0{isroug}")
        print(f"Camera {self.id} deactivated relais")

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

            if self.checkHuman():
                for alarm in self.camera_alarms:
                    for did in alarm["devices"]:
                        for devices in self.dev:
                            if did == devices["id"]:
                                self.relais_active = True
                                timestamp = self.takePhoto()
                                self.activateRelais(devices["ip"])
                                self.sendemail(f"{timestamp}_{self.camera_name}.png")
                                self.sendSMS()
                                self.deviceturnoff.append([devices, time.time()])

            else:
                print("no human but motion")
            self.motion_previous_time = time.time()
            self.motion_detected = True

        # this will deactivate the relais after n amount of time
        if self.motion_previous_time + self.relais_active_duration <= time.time() and self.relais_active:
            self.relais_active = False
            for dev in self.deviceturnoff:
                if (time.time()+int(dev[0]["delay"])) > dev[1]:
                    self.deactivateRelais(dev[0]["ip"])

        self.motion_frame_counter += 1
        self.ret, self.frame = self.cap.read()

        # Convert the frame to grayscale for better human detection






        self.motion_frame_counter += 1
