import math

near_edge_threshold = 0.1
center_threshold = 0.05
frame_width = 1280
frame_height = 720
sensitivity = 0.5
catchable_ball_size = 0.15 * frame_width

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
        r_values.append(s)

        # could try some calculating of distance based on r, y, and how big r should be if on ground at that y
        # could wait to catch ball until ball stops or on ground (at least)
        # it will be very difficult to determine if ball is not bouncing since robot is moving
        # might want to write this expecting ball to not be bouncing, at least at first
        # so then directions will be turn to direction ball is on, and as much as the ball is far from center
        # wait to catch until ball is in reach which should depend on size and if in center
        # that's also depending on if our camera can see inside the arms

        # prob make a simple linear function which will say how far to go based on r
        # zach wants x,y,r, which means I'm just going to be calculating where the ball is and going there





def calculate_ball_position(ball_radius_real, r, c, s, camera_height, camera_fov_deg):
    # Calculate horizontal and vertical angles based on the camera's FOV
    alpha = math.radians((c - (frame_width / 2)) / (frame_width / 2) * (camera_fov_deg / 2))
    beta = math.radians((r - (frame_height / 2)) / (frame_height / 2) * (camera_fov_deg / 2))
    
    # Calculate distance to the ball based on the apparent size
    D = ball_radius_real / math.tan(math.radians(camera_fov_deg / 2)) / s

    # online says this formula for distance
    # D = FocalLength in mm * (Real object width in mm) / (Virtual object width in px)
    
    # Calculate x and y coordinates on the ground plane
    x = D * math.tan(alpha)
    y = D * math.tan(beta)

    return x, y

# Example usage
ball_radius_real = 0.0635  # Size of the ball in meters
r = 240  # Row
c = 320  # Column
s = 40  # Size of the ball in pixels
camera_height = 0.15  # Height of the camera above the ground in meters
camera_fov_deg = 120.0  # Camera's FOV in degrees

x, y = calculate_ball_position(ball_radius_real, r, c, s, camera_height, camera_fov_deg)
print(f"X: {x:.2f} meters, Y: {y:.2f} meters")






# close arms and verify ball has been caught
# then start return to sender
# return to sender should be easy. prob can find online a library that will take all the IMU
# data and turn it into positions. then just send that initial pos to MCU
            

    # send data thru UART


file.close()