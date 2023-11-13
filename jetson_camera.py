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

# undistorting image specs
mtx = np.array([[ 571.75864487, 0, 630.67238944 ],
       [ 0, 571.38160776, 356.21218923 ],
        [ 0, 0, 1]])
dist = np.array([[-0.28155159, 0.09339524, -0.00264697, -0.00076021, 0.06938456]])
ncm = np.array([[ 533.23010254, 0, 631.92690463],
        [ 0, 499.39093018, 353.75964042],
        [ 0, 0, 1]])
roi = (169, 139, 873, 432)

video = cv.VideoCapture(pipeline, cv.CAP_GSTREAMER)
if not video.isOpened():
    print("Camera not opened")

while True:
    ret, frame = video.read()
    if not ret:
        break

    # undistort and crop
    # frame = cv.undistort(frame, mtx, dist, None, ncm)
    # x, y, w, h = roi
    # frame = frame[y:y+h, x:x+w]

    cv.imshow("Camera Feed", frame)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv.destroyAllWindows()
