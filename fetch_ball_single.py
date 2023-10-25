import math
from sshkeyboard import listen_keyboard
import cv2 as cv

near_edge_threshold = 0.1
center_threshold = 0.05
sensitivity = 0.5
frame_width = 1280 # in pixels
frame_height = 720 # in pixels
catchable_ball_size = 0.15 * frame_width
ball_diam_real = 0.0635  # in meters
camera_fov_deg = 120.0  # in degrees
sensor_width = 0.00645

c, r, s = 440, 260, 100

# Calculate horizontal and vertical angles based on the camera's FOV
alpha = math.radians((c - (frame_width / 2)) / (frame_width / 2) * (camera_fov_deg / 2))

# Calculate distance to the ball based on the apparent size
focal_len = sensor_width / 2 / math.tan(math.radians(camera_fov_deg / 2))
focal_len = 0.00275
focal_len = 1250
# can also get focal len from when doing camera intrinsics
D = ball_diam_real * focal_len / s
# but focal_len should be about 1250. will need to measure this when get camera

# Calculate x and y coordinates on the ground plane
x = D * math.tan(alpha)
y = D

# Calculate r, might just be alpha, or 90 - alpha
r = alpha

print(f"X: {x}, Y: {y}, R: {r}")

