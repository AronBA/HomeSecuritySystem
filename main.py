import cv2
import webbrowser
import time
import os

rtsp_address = "rtsp://username:password@IP_address:port/stream"

cap = cv2.VideoCapture(0)


cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

filepath = rf"C:\Users\{os.getlogin()}\AppData\Local\Microsoft\WindowsApps\wt.exe"

motion_detected = False
motion_delay = 10
prev_motion_time = 0
motion_counter = 0
motion_threshold = 10000
last_motion_time = 0


while True:
    ret, frame = cap.read()
    cv2.imshow('Camera Feed', frame)


    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)


    if motion_counter == 0:
        first_frame = gray_frame
        motion_counter += 1
        continue

    frame_delta = cv2.absdiff(first_frame, gray_frame)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)


    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < motion_threshold:
            continue
        motion_detected = True

    if motion_counter == 30:
        first_frame = gray_frame
        motion_counter = 0


    if motion_detected and time.time() > prev_motion_time + motion_delay:
        webbrowser.open('http://example.com')
        motion_detected = False
        prev_motion_time = time.time()
        os.startfile(filepath)

    if cv2.waitKey(1) == ord('q'):
        break

    motion_counter += 1


cap.release()
cv2.destroyAllWindows()
