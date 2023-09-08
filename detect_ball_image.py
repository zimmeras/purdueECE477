import cv2 as cv
import numpy as np
import time

start = time.time()
frame = cv.imread('ordered_pink_balls.png')
# frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
blurFrame = cv.GaussianBlur(grayFrame, (17,17), 0)

circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.4, 5000, 
                            param1=100, param2=40, minRadius=0, maxRadius=200)

if circles is not None:
    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower_pink = np.array([100, 20, 20])   # Lower bound for pink color in HSV
    upper_pink = np.array([170, 255, 255])  # Upper bound for pink color in HSV

    x, y, r = int(circles[0,0,0]), int(circles[0,0,1]), circles[0,0,2]
    factor = 0.5
    top = int(y + factor*r)
    bot = int(y - factor*r)
    left = int(x - factor*r)
    right = int(x + factor*r)
    circle_subset_of_frame = frame[left:right, bot:top, :]

    x2 = x+20
    y2 = y+20
    print(frame[x,y,:])
    print(frame[x2,y2,:])

    cv.imshow("subset color frame", circle_subset_of_frame)
    cv.waitKey()

    pink_mask = cv.inRange(circle_subset_of_frame, lower_pink, upper_pink)
    cv.imshow("subset masked frame", pink_mask)
    cv.waitKey()

    percent_pink = np.sum(pink_mask) /255 / pink_mask.size
    pink_threshold = 0.75

    print(f"Percent pink: {percent_pink}")

    if percent_pink >= pink_threshold:
        circles = np.uint32(np.around(circles))
        cv.circle(frame, (circles[0,0,0], circles[0,0,1]), circles[0,0,2], (0, 255, 0), 3)

    end = time.time()
    print(f"time: {end-start}")

    # cv.imshow("pink frame", pink_mask)
    # cv.waitKey()

    # maybe
    # kernel = np.ones((5, 5), np.uint8)
    # pink_mask = cv.erode(pink_mask, kernel, iterations=1)
    # pink_mask = cv.dilate(pink_mask, kernel, iterations=1)

    # cv.imshow("pink frame", pink_mask)
    # cv.waitKey()

    # contours, _ = cv.findContours(pink_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # x, y = circles[0,0,0], circles[0,0,1]
    # for contour in contours:
    #     if cv.pointPolygonTest(contour, (x, y), False) >= 0:
    #         circles = np.uint32(np.around(circles))
    #         cv.circle(frame, (circles[0,0,0], circles[0,0,1]), circles[0,0,2], (255, 0, 255), 3)
    #         break

cv.imshow("circles", frame)
end = time.time()
print(f"time: {end-start}")
cv.waitKey()
cv.destroyAllWindows()