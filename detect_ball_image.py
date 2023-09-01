import cv2 as cv
import numpy as np

frame = cv.imread('ball2.jpeg')
frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
blurFrame = cv.GaussianBlur(grayFrame, (17,17), 0)

circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.4, 5000, 
                            param1=100, param2=40, minRadius=40, maxRadius=400)

if circles is not None:
    circles = np.uint32(np.around(circles))
else:
    exit()
for i in circles[0, :]:
    cv.circle(frame, (i[0], i[1]), 1, (0,100,100), 3)
    cv.circle(frame, (i[0], i[1]), i[2], (255, 0, 255), 3)

cv.imshow("circles", frame)
cv.waitKey()
cv.destroyAllWindows()