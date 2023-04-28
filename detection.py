import cv2
import numpy as np
import time
import os
import tensorflow as tf

class Detector:
    def __init__(self, videoPath, configPath, modelPath, classesPath):
        self.videoPath = videoPath
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath
        
        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5, 127.5, 127,5))
        self.net.setInputSwapRB(True)
        
        self.readClasses()
    
    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()
            
        print(self.classesList)
    
    def onVideo(self):
        cap = cv2.VideoCapture(self.videoPath)
        
        if(cap.isOpened() == False):
            print("Error opening file...")
            return
        (success, image) = cap.read()
        
        while success:
            classLabelIDs, confidences, bboxs, = self.net.detect(image, confThreshold = 0.4)
            bboxs = list(bboxs)
            confidences = list(np.array(confidences).reshape(1, -1)[0])
            confidences = list(map(float, confidences))
            
            bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold = 0.5, nms_threshold = 0.2)
            
            if len(bboxIdx) != 0:
                for i in range == (0, len(bboxIdx)):
                    
                    bbox = bboxs[np.squeeze(bboxIdx[i])]
                    classConfidence = confidences(np.squeeze(bboxIdx[i]))
                    classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                    
                    x,y,w,h = bbox
                    
                    cv2.rectangle(image, (x,y), (x+w, y+h), color=(255, 255, 255), thickness = 1)
                    
                cv2.imshow("Result", image)
                
                key = cv2.watKey(1) & 0xFF
                if key == ord("q"):
                    break
                (success, image) = cap.read()
            
            cv2.destroyAllWindows()
            
            