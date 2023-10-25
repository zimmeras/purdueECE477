import math

near_edge_threshold = 0.1
center_threshold = 0.05
sensitivity = 0.5
frame_width = 1280 # in pixels
frame_height = 720 # in pixels
catchable_ball_size = 0.15 * frame_width
ball_diam_real = 0.0635  # in meters
camera_fov_deg = 120.0  # in degrees
sensor_width = 0.00645

file = open("ball_pos_data.txt", 'r')

c_values = []
r_values = []
s_values = []

last_c, last_r, last_s = -1, -1, -1

# -1 y means continue with same lateral velocity
# x and y are in cm's and r is in degrees
x, y, r = 0, -1, 0

for line in file:
    values = line.strip().split(', ')
    c, r, s = map(int, values)
    
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
                r = -1 * sensitivity * 120
            elif last_c >= (1 - near_edge_threshold) * frame_width:
                # turn right
                r = sensitivity * 120
            else:
                # prob make a full rotation to try to find ball
                pass
    else:
        last_c, last_r, last_s = c, r, s
        c_values.append(c)
        r_values.append(r)
        s_values.append(s)

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

        # Calculate r, might just be alpha, or 90 - alpha
        r = alpha



# close arms and verify ball has been caught
# then start return to sender
# return to sender should be easy. prob can find online a library that will take all the IMU
# data and turn it into positions. then just send that initial pos to MCU
            

    # send data thru UART


file.close()