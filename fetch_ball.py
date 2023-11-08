import math
import numpy as np

near_edge_threshold = 0.1
center_threshold = 0.05
sensitivity = 0.5

frame_width = 1280 # in pixels
frame_height = 720 # in pixels
ball_diam_real = 0.0635  # in meters
camera_fov_deg = 120.0  # in degrees
sensor_width = 0.00645

frame_width_center = frame_width / 2
center_width = frame_width * center_threshold
center_left = frame_width_center - center_width / 2
center_right = frame_width_center + center_width / 2

catchable_ball_size = 0.15 * frame_width
catchable_ball_row = 0.85 * frame_height

def isInCenter(c):
    if c > center_left and c < center_right:
        return True
    else:
        return False
    
def isCatchable(c, r, s):
    if s > catchable_ball_size and isInCenter(c) and r > catchable_ball_row:
        return True
    else:
        return False
    
def close_arms():
    pass

def return_to_sender():
    pass

def send_uart(data):
    pass

input_file = open("ball_pos_data.txt", 'r')
output_file = open("out_pos.txt", "w")

c_values = []
r_values = []
s_values = []

x_values = []
y_values = []
r_values = []

last_c, last_r, last_s = -1, -1, -1

frames_caught = 0

# -1 y means continue with same lateral velocity
# x and y are in m's and r is in radians
x, y, r = 0, -1, 0

for line in input_file:
    values = line.strip().split(', ')
    c, r, s = map(int, values)

    last_c, last_r, last_s = c, r, s
    c_values.append(c)
    r_values.append(r)
    s_values.append(s)
    
    # if don't see ball
    if c == -1 and r == -1 and s == -1:
        # if didn't see ball on last frame
        if last_c == -1 and last_r == -1 and last_s == -1:
            # wait until see ball
            continue
        else:
            # if last ball pos is near left or right edge then move robot that direction
            if last_c <= near_edge_threshold * frame_width:
                # turn left
                r = -1 * sensitivity * camera_fov_deg
            elif last_c >= (1 - near_edge_threshold) * frame_width:
                # turn right
                r = sensitivity * camera_fov_deg
            else:
                # rotate towards last seen location of ball
                if x_values[-1] > frame_width_center:
                    r = math.pi / 2
                else:
                    r = -1 * math.pi / 2
    elif isCatchable(c, r, s):
        # close arms and verify ball has been caught
        close_arms()
        frames_caught += 1
        if frames_caught >= 3:
            # then start return to sender and stop ball detection
            return_to_sender()
    else:
        # prob make a simple linear function which will say how far to go based on r
        # zach wants x,y,r, which means I'm just going to be calculating where the ball is and going there


        # Calculate horizontal and vertical angles based on the camera's FOV
        alpha = math.radians((c - (frame_width / 2)) / (frame_width / 2) * (camera_fov_deg / 2))
        beta = math.radians((r - (frame_height / 2)) / (frame_height / 2) * (camera_fov_deg / 2))
        
        # Calculate distance to the ball based on the apparent size
        focal_len = sensor_width / 2 / math.tan(math.radians(camera_fov_deg / 2))
        focal_len = 0.00275
        # can also get focal len from when doing camera intrinsics
        D = ball_diam_real * focal_len / s
        # but focal_len should be about 1250. will need to measure this when get camera
        
        # Calculate x and y coordinates on the ground plane
        x = D * math.tan(alpha)
        y = D * math.tan(beta)
        # i'm pretty sure y should just be D

        # Calculate r, might just be alpha, or pi/2 - alpha
        r = alpha

    x_values.append(x)
    y_values.append(y)
    r_values.append(r)
    output_file.write(f"{x}, {y}, {r}\n")
    send_uart(x)

avg_x = np.mean(x_values)
avg_y = np.mean(y_values)
avg_r = np.mean(r_values)

print(f"Avg X: {avg_x}, Avg Y: {avg_y}, Avg R: {avg_r}")




# return to sender should be easy. prob can find online a library that will take all the IMU
# data and turn it into positions. then just send that initial pos to MCU


input_file.close()
output_file.close()