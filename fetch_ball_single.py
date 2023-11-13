import math
import cv2 as cv

frame_width = 1280 # in pixels
camera_fov_deg = 175.0  # in degrees
dist_factor = 16.1

c, r, s = 542.7405475880053, 370.96088657105605, 20.189048239895698

# Calculate horizontal angle based on the camera's FOV
r = math.radians((c - (frame_width / 2)) / (frame_width / 2) * (camera_fov_deg / 2))

# Calculate distance to the ball based on the apparent size
y = dist_factor / s

print(f"Y: {y}, R: {r}")

