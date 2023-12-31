import cv2 as cv
import numpy as np
import time

lower_pink = np.array([140, 130, 0])   # Lower bound for pink color in HSV
upper_pink = np.array([170, 255, 255])  # Upper bound for pink color in HSV

video = cv.VideoCapture("pink_ball.mov")

times = []
begin = time.time()

# frame_width = int(video.get(3))
# frame_height = int(video.get(4))
# size = (frame_width, frame_height)
# out_video = cv.VideoWriter('pink_ball2.mp4', cv.VideoWriter_fourcc(*'mp4v'), 60, size)

# file = open("ball_pos_data.txt", 'w')

while True:
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
        # cv.circle(frame, (circles[0,0,0], circles[0,0,1]), circles[0,0,2], (0, 255, 0), 3)
        x, y, r = circles[0,0,0], circles[0,0,1], circles[0,0,2]

    #     # code to send ball position data to catch ball
    #     file.write(f"{x}, {y}, {r}\n")
    # else:
    #     file.write(f"-1, -1, -1\n")
    

    # out_video.write(frame)
    # cv.imshow("frame with circle", frame)
    # if cv.waitKey(1) & 0xFF == ord('q'): break
    
    end = time.time()
    times.append(end - start)

# file.close()

avg = np.mean(times)
fps = 1 / avg
print(f"FPS: {fps}")

end = time.time()
print(f"Video took: {end-begin} s")

video.release()
# out_video.release()
cv.destroyAllWindows()