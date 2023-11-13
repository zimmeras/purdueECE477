import numpy as np
import cv2 as cv
import time

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)
# our chessboard is a 10x7
objp = np.zeros((9*6,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

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

start = time.time()

# n = 0
while time.time()-start < 45:
	ret, img = video.read()
	if not ret: break

	# n += 1
	# if n != 60: continue
	# n = 0

	# cv.imshow("heksdfsd", img)
	# if cv.waitKey(1) & 0xFF == ord('q'): break
	# print(np.shape(img))
	
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	

	# Find the chess board corners
	ret2, corners = cv.findChessboardCorners(gray, (9,6), None)

	# If found, add object points, image points (after refining them)
	if ret2 == True:
		print("found")
		objpoints.append(objp)
		corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
		imgpoints.append(corners2)

		# Draw and display the corners
		cv.drawChessboardCorners(img, (9,6), corners2, ret)
		cv.imshow('img', img)
		cv.waitKey(500)
	else:
		print("not found")

video.release()
cv.destroyAllWindows()


# calibrate camera
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
w, h = 1280, 720
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

print(f"mtx: {mtx}\ndist: {dist}\nncm: {newcameramtx}\nroi: {roi}")
print(f"mtx: {np.shape(mtx)}\ndist: {np.shape(dist)}\nncm: {np.shape(newcameramtx)}\nroi: {np.shape(roi)}")
print(f"mtx: {type(mtx)}\ndist: {type(dist)}\nncm: {type(newcameramtx)}\nroi: {type(roi)}")

'''
# undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('calibresult.png', dst) # this is the new, undistorted image
'''

# how good is the calibration?
mean_error = 0
for i in range(len(objpoints)):
	imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
	error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
mean_error += error
print( "total error: {}".format(mean_error/len(objpoints)) )
