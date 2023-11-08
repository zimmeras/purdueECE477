import math
import cv2 as cv

near_edge_threshold = 0.1
center_threshold = 0.05
sensitivity = 0.5
frame_width = 1280 # in pixels
frame_height = 720 # in pixels
catchable_ball_size = 0.15 * frame_width
ball_diam_real = 0.0635  # in meters
camera_fov_deg = 175.0  # in degrees
sensor_width = 0.00645

c, r, s = 542.7405475880053, 370.96088657105605, 20.189048239895698

# Calculate horizontal and vertical angles based on the camera's FOV
alpha = math.radians((c - (frame_width / 2)) / (frame_width / 2) * (camera_fov_deg / 2))

# Calculate distance to the ball based on the apparent size
dist_factor = 17
D = dist_factor / s

# Calculate x and y coordinates on the ground plane
x = D * math.tan(alpha)
y = D

# Calculate r, might just be alpha, or pi/2 - alpha
r = alpha

print(f"X: {x}, Y: {y}, R: {r}")

