import cv2 as cv 
import numpy as np
import time 

# this works with the raspberry pi camera but no the wide angle camera
# pipeline = (
#         "nvarguscamerasrc sensor_id=1 ! "
#         "video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)120/1 ! "
#         "nvvidconv flip-method=0 ! "
#         "video/x-raw, width=(int)1280, height=(int)720, format=(string)BGRx ! "
#         "videoconvert ! "
#         "video/x-raw, format=(string)BGR ! "
#         "appsink sync=false"
# )

# video = cv.VideoCapture(pipeline, cv.CAP_GSTREAMER)

# sudo service nvargus-daemon restart
# dmesg | grep imx
pipeline = (
        "nvarguscamerasrc sensor_id=0 ! nvoverlaysink"
        "video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, format=(string)NV12, framerate=(fraction)30/1 ! "
        "nvvidconv ! "
        "video/x-raw, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! "
        "appsink"
)

video = cv.VideoCapture(pipeline, cv.CAP_GSTREAMER)


if not video.isOpened():
    print("Camera not opened")
     
lower_pink = np.array([140, 100, 0])   # Lower bound for pink color in HSV
upper_pink = np.array([170, 255, 255])  # Upper bound for pink color in HSV

times = []
begin = time.time()

# frame_width = int(video.get(3))
# frame_height = int(video.get(4))
# size = (frame_width, frame_height)
# out_video = cv.VideoWriter('pink_ball2.mp4', cv.VideoWriter_fourcc(*'mp4v'), 60, size)

n = 0
while time.time()-begin < 10:
    # n += 1
    # if n != 60: continue
    # n = 0

    start = time.time()
    ret, frame = video.read()
    if not ret: break

    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    pink_mask = cv.inRange(frame_hsv, lower_pink, upper_pink)
    # cv.imshow("frame with circle", pink_mask)
    # cv.waitKey()

    blurFrame = cv.GaussianBlur(pink_mask, (17,17), 0)

    # circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.4, 5000,
    #                         param1=100, param2=35, minRadius=0, maxRadius=200)
    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.4, 5000,
                            param1=140, param2=30, minRadius=0, maxRadius=250)

    if circles is not None:
        circles = np.uint32(np.around(circles))
        for i in circles[0,:]:
            cv.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 3)

    # out_video.write(frame)
    cv.imshow("frame with circle", frame)
    if cv.waitKey(1) & 0xFF == ord('q'): break

    end = time.time()
    times.append(end - start)

video.release()
# out_video.release()
cv.destroyAllWindows()

avg = np.mean(times)
fps = 1 / avg
print(f"\nFPS: {fps}")

end = time.time()
print(f"Video took: {end-begin} s")
