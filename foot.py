import timeit
toe_off_time = 0
heel_strike_time = 0

def velocity(v_o, accel_y, t):
    accel_y*=-1
    if(abs(accel_y) < 0.01):
        accel_y = 0
        v_o = 0
    return v_o + accel_y * t

def stride_length(v_o, accel_y, t):
    accel_y*=-1
    return v_o *t + 1/2 * accel_y* pow(t,2)

def is_toe_off(foot_z):
    
    return foot_z > 10
    # and foot_z < 15

def is_heel_strike(foot_z):
    return foot_z <= -20

def swing_time(toe_off, heel_strike):
    global toe_off_time 
    global heel_strike_time

    if (toe_off):
        toe_off_time = timeit.default_timer()
    elif (heel_strike):
        heel_strike_time = timeit.default_timer()
    
    if (heel_strike_time > toe_off_time):
        return (heel_strike_time - toe_off_time)
    return 0

def stance_time(toe_off, heel_strike):
    global toe_off_time 
    global heel_strike_time

    if (toe_off):
        toe_off_time = timeit.default_timer()
    elif (heel_strike):
        heel_strike_time = timeit.default_timer()
    
    if (heel_strike_time < toe_off_time):
        return (toe_off_time - heel_strike_time) # return time in seconds
    return 0
