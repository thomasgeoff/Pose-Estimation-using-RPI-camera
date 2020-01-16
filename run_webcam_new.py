import logging
import sys
import time
import math
import cv2
import numpy as np
from openpose import pyopenpose as op

def run_webcam():
    print('starting')
    fps_time = 0

    params = dict()
    params["model_folder"] = "models/"

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
    count = 0
    print("OpenPose start")
    cap = cv2.VideoCapture("nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)1280, height=(int)720, "
        "format=(string)NV12, framerate=(fraction)60/1 ! "
        "nvvidconv flip-method=0 ! "
        "video/x-raw, width=(int)1280, height=(int)720, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink")
    while cap.isOpened() and count < 10:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out_video = cv2.VideoWriter('/tmp/output.avi', fourcc, 30.0,(640,480))
        ret_val, img = cap.read()
        if ret_val == True and count < 10:
            datum = op.Datum()
            imageToProcess = img
            datum.cvInputData = imageToProcess
            opWrapper.emplaceAndPop([datum])
            print("Body Key Points: \n" + str(datum.poseKeypoints))
            out_video.write(imageToProcess)
            count += 1
           # cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData)
           # key = cv2.waitKey(15)
           # if key == 27:
            #    break
    out_video.release()
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    run_webcam()
