import cv2
import time
import threading
import playsound

human_cascade = cv2.CascadeClassifier('Files/haarcascade_upperbody.xml')


class Camera:
    amountofcameras = 0

    def __init__(self, camera_adress, path_sound_file, relais, relais_active_duration, motion_detection_cooldown,
                 motion_detection_threshold):
        self.gray = None
        self.ret = None
        Camera.amountofcameras += 1

        self.frame = None
        self.first_frame = 0
        self.motion_frame_counter = 0

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



        print(f"Camer {self.id} detected a human")
    def activateRelais(self):
        print(f"Camera {self.id} activated relais")

    def deactivateRelais(self):
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
                print("Human")
                threading.Thread(target=self.activateSound, daemon=True).start()
                threading.Thread(target=self.activateRelais, daemon=True).start()
                # threading.Thread(target=self.sendsms, daemon=True).start()
                # threading.Thread(target=self.sendemail, daemon=True).start()
            else:
                print("no human but motion")
            self.motion_previous_time = time.time()
            self.motion_detected = True


        # this will deactivate the relais after n amount of time
        if self.motion_previous_time + self.relais_active_duration <= time.time() and self.relais_active:
            self.relais_active = False
            self.deactivateRelais()

        self.motion_frame_counter += 1
        self.ret, self.frame = self.cap.read()

        # Convert the frame to grayscale for better human detection






        self.motion_frame_counter += 1
