import cv2 as cv 
import numpy as np
import time

pipeline = (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)120/1 ! "
        "nvvidconv flip-method=0 ! "
        "video/x-raw, width=(int)1280, height=(int)720, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! "
        "appsink sync=false"
)

video = cv.VideoCapture(pipeline, cv.CAP_GSTREAMER)
if not video.isOpened():
    print("Camera not opened")

while True:
    ret, frame = video.read()
    if not ret:
        break
    cv.imshow("Camera Feed", frame)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv.destroyAllWindows()
