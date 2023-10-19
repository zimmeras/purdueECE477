import cv2 as cv
import numpy as np
import time

lower_pink = np.array([140, 130, 0])   # Lower bound for pink color in HSV
upper_pink = np.array([170, 255, 255])  # Upper bound for pink color in HSV

frame = cv.imread('ball_lab.jpeg')

frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
pink_mask = cv.inRange(frame_hsv, lower_pink, upper_pink)

blurFrame = cv.GaussianBlur(pink_mask, (17,17), 0)

circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.4, 5000, 
                        param1=140, param2=30, minRadius=0, maxRadius=250)

if circles is not None:
    circles = np.uint32(np.around(circles))
    cv.circle(frame, (circles[0,0,0], circles[0,0,1]), circles[0,0,2], (0, 255, 0), 3)
    x, y, r = circles[0,0,0], circles[0,0,1], circles[0,0,2]
    cv.circle(frame, (200, 50), 50, (0, 255, 0), 3)


cv.imshow("circles", frame)
cv.waitKey()
cv.destroyAllWindows()