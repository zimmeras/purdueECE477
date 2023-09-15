import cv2 as cv
import numpy as np
import time

lower_pink = np.array([100, 20, 20])   # Lower bound for pink color in HSV
upper_pink = np.array([170, 255, 255])  # Upper bound for pink color in HSV

start = time.time()
frame = cv.imread('ball_lab.jpeg')
# frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
blurFrame = cv.GaussianBlur(grayFrame, (17,17), 0)

circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.4, 50, 
                            param1=160, param2=40, minRadius=0, maxRadius=300)

if circles is not None:
    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    circles = np.uint32(np.around(circles))
    
    for i in circles[0,:]:
        x, y, r = i[0], i[1], i[2]
        # print(f"X,Y,R: {x}, {y}, {r}")
        cv.circle(frame, (x, y), r, (0, 255, 0), 3)
        factor = 0.6
        top = int(y - factor*r)
        bot = int(y + factor*r)
        left = int(x - factor*r)
        right = int(x + factor*r)

        # circle_subset_of_frame = frame[top:bot, left:right, :]
        # cv.imshow("subset color frame", circle_subset_of_frame)
        # cv.waitKey()

        circle_subset_of_frame = frame_hsv[top:bot, left:right, :]
        pink_mask = cv.inRange(circle_subset_of_frame, lower_pink, upper_pink)
        # cv.imshow("subset masked frame", pink_mask)
        # cv.waitKey()

        percent_pink = np.sum(pink_mask) /255 / pink_mask.size
        pink_threshold = 0.75

        print(f"Percent pink: {percent_pink}")

        if percent_pink >= pink_threshold:
            cv.circle(frame, (x, y), r, (0, 255, 0), 3)

end = time.time()
print(f"time: {end-start}")

cv.imshow("circles", frame)
cv.waitKey()
cv.destroyAllWindows()