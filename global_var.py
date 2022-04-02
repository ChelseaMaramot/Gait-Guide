import scipy.io
from tkinter import *
from datetime import date

mat = scipy.io.loadmat('matlab/Subject15.mat')
online_knee_angle = mat['s'][0,0]['Data']['Ang'][0,0][6]
plot_online_data = []

shank_angles = []
thigh_angles = []
knee_angles = []
sag_shank_angles = []
sag_thigh_angles = []
fieldnames = ["Knee_Angle", "Foot_Velocity", "Stride_Length", "Swing_Time", "Stance_Time"]
#fieldnames = ["Foot Velocity", "Foot Acceleration", "Stride Length"]

cnt=0
df_index = 0
df_prev_angles = []

foot_angles = []
foot_accel = []
v_o = 0
stride_length = 0
stride_length_list= []

day = date.today().strftime("%b-%d-%Y")
file_to_write = day
prev_file = day


thigh_offset = 0
shank_offset = 0
foot_offset = 0

process_data = []
process_sag_shank = []
process_sag_thigh = []





#knee_angle_text = Label(text=f"{knee_joint_angle}")
#plot_flexion = False 