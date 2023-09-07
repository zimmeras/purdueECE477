import cv2 as cv
import numpy as np
import time

video = cv.VideoCapture("ball60fps.mov")

times = []
begin = time.time()

# frame_width = int(video.get(3))
# frame_height = int(video.get(4))
# size = (frame_width, frame_height)
# out_video = cv.VideoWriter('ball60fps_detected.mp4', 
#                          cv.VideoWriter_fourcc(*'mp4'),
#                          60, size)

while True:
    start = time.time()
    ret, frame = video.read()
    if not ret: break

    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (17,17), 0)

    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.4, 5000, 
                            param1=100, param2=40, minRadius=0, maxRadius=200)
    
    if circles is not None:
        # now want to check if the ball color is correct
        # hot pink is about BGR: 180, 105, 255
        # normal pink is about BGR: 193, 182, 255
        # I think it could be good to say if the colors r within either a certain range or
        # percentage of the range, they r good to be the ball

        circles = np.uint32(np.around(circles))
        cv.circle(frame, (circles[0,0,0], circles[0,0,1]), circles[0,0,2], (255, 0, 255), 3)

    # out_video.write(frame)
    cv.imshow("frame with circles", frame)
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