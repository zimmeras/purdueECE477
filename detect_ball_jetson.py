import cv2 as cv 
import numpy as np
import time 

pipeline = (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)100/1 ! "
        "nvvidconv flip-method=2 ! "
        "video/x-raw, width=(int)1280, height=(int)720, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! "
        "appsink"
)

video = cv.VideoCapture(pipeline, cv.CAP_GSTREAMER)
if not video.isOpened():
    print("Camera not opened")
     
lower_pink = np.array([140, 130, 0])   # Lower bound for pink color in HSV
upper_pink = np.array([170, 255, 255])  # Upper bound for pink color in HSV

times = []
begin = time.time()

n = 0
while time.time()-begin < 5:
    # n += 1
    # if n != 60: continue
    # n = 0

    start = time.time()
    ret, frame = video.read()
    if not ret: break

    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    pink_mask = cv.inRange(frame_hsv, lower_pink, upper_pink)

    blurFrame = cv.GaussianBlur(pink_mask, (17,17), 0)
    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.4, 5000,
                            param1=140, param2=30, minRadius=0, maxRadius=250)

    if circles is not None:
        circles = np.uint32(np.around(circles))
        c, r, s = circles[0,0,0], circles[0,0,1], circles[0,0,2]
        print(f"{c}, {r}, {s}\n")

    end = time.time()
    times.append(end - start)

avg = np.mean(times)
fps = 1 / avg
print(f"FPS: {fps}")

end = time.time()
print(f"Video took: {end-begin} s")

video.release()
cv.destroyAllWindows()
