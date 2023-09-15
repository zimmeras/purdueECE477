import cv2 as cv
import numpy as np
import time

lower_pink = np.array([120, 50, 50])   # Lower bound for pink color in HSV
upper_pink = np.array([170, 255, 255])  # Upper bound for pink color in HSV

video = cv.VideoCapture("pink_ball.mov")

times = []
begin = time.time()

frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)
# out_video = cv.VideoWriter('ball60fps_detected.mp4', 
#                          cv.VideoWriter_fourcc(*'mp4'),
#                          60, size)

while True:
    start = time.time()
    ret, frame = video.read()
    if not ret: break

    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (17,17), 0)

    # circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.4, 5000, 
    #                         param1=100, param2=35, minRadius=0, maxRadius=200)
    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.4, 50, 
                            param1=140, param2=30, minRadius=0, maxRadius=250)
    
    if circles is not None:
        frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        circles = np.uint32(np.around(circles))

        for i in circles[0,:]:
            x, y, r = i[0], i[1], i[2]
            # cv.circle(frame, (x, y), r, (0, 255, 0), 3)
            factor = 0.6
            top = int(y - factor*r)
            bot = int(y + factor*r)
            left = int(x - factor*r)
            right = int(x + factor*r)

            if top < 0 or left < 0 or bot > frame_height or right > frame_width:
                continue

            circle_subset_of_frame = frame_hsv[top:bot, left:right, :]
            pink_mask = cv.inRange(circle_subset_of_frame, lower_pink, upper_pink)

            percent_pink = np.sum(pink_mask) /255 / pink_mask.size
            pink_threshold = 0.75

            if percent_pink >= pink_threshold:
                cv.circle(frame, (x, y), r, (0, 255, 0), 3)

    # out_video.write(frame)
    cv.imshow("frame with circle", frame)
    if cv.waitKey(1) & 0xFF == ord('q'): break
    
    end = time.time()
    times.append(end - start)

avg = np.mean(times)
fps = 1 / avg
print(f"FPS: {fps}")

end = time.time()
print(f"Video took: {end-begin} s")

video.release()
# out_video.release()
cv.destroyAllWindows()