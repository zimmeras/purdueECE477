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

# pink thresholds
lower_pink = np.array([140, 100, 0])   # Lower bound for pink color in HSV
upper_pink = np.array([170, 255, 255])  # Upper bound for pink color in HSV

# undistorting image specs
mtx = np.array([[ 571.75864487, 0, 630.67238944 ],
       [ 0, 571.38160776, 356.21218923 ],
        [ 0, 0, 1]])
dist = np.array([[-0.28155159, 0.09339524, -0.00264697, -0.00076021, 0.06938456]])
ncm = np.array([[ 533.23010254, 0, 631.92690463],
        [ 0, 499.39093018, 353.75964042],
        [ 0, 0, 1]])
roi = (169, 139, 873, 432)

cs = []
rs = []
ss = []

times = []
begin = time.time()

# file = open("ball_pos_data.txt", 'w')

n = 0
while time.time()-begin < 30:
    start = time.time()
    ret, frame = video.read()
    if not ret: break

    # n += 1
    # if n != 60: continue
    # n = 0

    # undistort and crop
    # frame = cv.undistort(frame, mtx, dist, None, ncm)
    # x, y, w, h = roi
    # frame = frame[y:y+h, x:x+w]

    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    pink_mask = cv.inRange(frame_hsv, lower_pink, upper_pink)

    blurFrame = cv.GaussianBlur(pink_mask, (17,17), 0)
    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.4, 5000,
                            param1=140, param2=30, minRadius=0, maxRadius=250)
    # circles = None
    if circles is not None:
        circles = np.uint32(np.around(circles))
        c, r, s = circles[0,0,0], circles[0,0,1], circles[0,0,2]
        cs.append(c)
        rs.append(r)
        ss.append(s)
        # cv.circle(frame, (circles[0,0,0], circles[0,0,1]), circles[0,0,2], (0, 255, 0), 3)
        # print(f"{c}, {r}, {s}\n")
    #     file.write(f"{c}, {r}, {s}\n")
    # else:
    #     file.write(f"-1, -1, -1\n")

    # cv.imshow("frame with circle", frame)
    # if cv.waitKey(1) & 0xFF == ord('q'): break

    end = time.time()
    times.append(end - start)
    # print(end - start)

# file.close()
video.release()
cv.destroyAllWindows()

cavg = np.mean(cs)
ravg = np.mean(rs)
savg = np.mean(ss)

print(f"{cavg}, {ravg}, {savg}")

avg = np.mean(times)
fps = 1 / avg
print(f"\nFPS: {fps}")

end = time.time()
print(f"Video took: {end-begin} s")
