import cv2 as cv
import numpy as np
import time

videoCapture = cv.VideoCapture(0)

times = []

while True:
    start = time.time()
    ret, frame = videoCapture.read()
    if not ret: break

    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (17,17), 0)

    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.4, 5000, 
                            param1=100, param2=40, minRadius=2, maxRadius=100)
    
    if circles is not None:
        circles = np.uint32(np.around(circles))
        cv.circle(frame, (circles[0,0,0], circles[0,0,1]), circles[0,0,2], (255, 0, 255), 3)

    cv.imshow("frame with circles", frame)
    if cv.waitKey(1) & 0xFF == ord('q'): break
    
    end = time.time()
    times.append(end - start)

avg = np.mean(times)
fps = 1 / avg
print(f"FPS: {fps}")

videoCapture.release()
cv.destroyAllWindows()
