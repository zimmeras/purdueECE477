import cv2 as cv
import numpy as np

videoCapture = cv.VideoCapture(0)
prevCircle = None
dist = lambda x1, y1, x2, y2: (x1-x2)**2 + (y1-y2)**2

while True:
    ret, frame = videoCapture.read()
    if not ret: break
    cv.imshow("circles", frame)

    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (17,17), 0)

    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.4, 5000, 
                            param1=100, param2=40, minRadius=2, maxRadius=100)
    
    if circles is not None:
        circles = np.uint32(np.around(circles))
        for i in circles[0, :]:
            cv.circle(frame, (i[0], i[1]), 1, (0,100,100), 3)
            cv.circle(frame, (i[0], i[1]), i[2], (255, 0, 255), 3)

    # cv.circle(frame, (circles[0,0], circles[0,1]), 1, (0,100,100), 3)
    # cv.circle(frame, (circles[0,0], circles[0,1]), circles[0,2], (255, 0, 255), 3)

    # chosen = None
    # if circles is not None:
    #     circles = np.uint32(np.around(circles))
    #     for i in circles[0, :]:
    #         if chosen is None: chosen = i
    #         if prevCircle is not None:
    #             if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) <= dist(i[0], i[1], prevCircle[0], prevCircle[1]):
    #                 chosen = i

    # cv.circle(frame, (chosen[0], chosen[1]), 1, (0,100,100), 3)
    # cv.circle(frame, (chosen[0], chosen[1]), chosen[2], (255, 0, 255), 3)

    # prevCircle = chosen

    cv.imshow("circles", frame)
    if cv.waitKey(1) & 0xFF == ord('q'): break

videoCapture.release()
cv.destroyAllWindows()

# elliptical transform
