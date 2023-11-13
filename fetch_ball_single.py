import math
import cv2 as cv

frame_width = 1280 # in pixels
camera_fov_deg = 175.0  # in degrees
dist_factor = 16.1

c, r, s = 542.7405475880053, 370.96088657105605, 20.189048239895698

# Calculate horizontal angle based on the camera's FOV
alpha = math.radians((c - (frame_width / 2)) / (frame_width / 2) * (camera_fov_deg / 2))

# Calculate distance to the ball based on the apparent size
D = dist_factor / s

# Calculate x and y coordinates on the ground plane
x = D * math.tan(alpha)
y = D

# Calculate r, might just be alpha, or pi/2 - alpha
r = alpha

print(f"X: {x}, Y: {y}, R: {r}")

