
import serial 
from os import path
from time import sleep
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from drawnow import *
import re
import csv
import pandas as pd
import knee
import foot
from global_var import *
from plot import *
from report import *


from tkinter import *
from tkinter import ttk

plt.ion() #plots live data 
arduino_data_knee = serial.Serial('COM8', 115200)
arduino_data_foot = serial.Serial('COM9', 115200)

start_flag = False
previous_flag = False
current_flag = True
online_flag = False
is_calibrate = True
to_avg = []
online_index = 0
knee_joint_angle = 0
to_avg_knee = []
to_avg_shank = []
to_avg_thigh = []

foot_angle = 0
v_o = 0
stride_length = 0
stride_length_list = []
to_avg_velocity = []
to_avg_stride_length = []
process_velocity = 0
process_stride_length = 0
process_swing_time = 0
process_stance_time = 0


entry_is_disabled = False
entry_placeholder = ""
clicked = False

report_index = 0
reports = [0,1,2,3] ### change according to number of report graphs

def calibrate():
    print("Calibrating...")
    global_var.thigh_offset = -90 - sum(global_var.thigh_angles)/len(global_var.thigh_angles) 
    global_var.shank_offset = -90 - sum(global_var.shank_angles)/len(global_var.shank_angles) 
    global_var.foot_offset = sum(global_var.foot_angles)/len(global_var.foot_angles)
    global_var.thigh_angles = []
    global_var.shank_angles = []
    global_var.foot_angles = []
    global_var.calibrate = False

    
def write_csv(filename):

    global process_velocity

    is_exist = path.exists(f"data/{filename}.csv")
    with open(f'data/{filename}.csv', 'a') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator = '\n')
        data ={
            "Knee_Angle": global_var.process_data[-1],
            #knee_joint_angle,
            "Foot_Velocity": process_velocity,
            #"Foot Acceleration": float(data_foot[0]),
            "Stride_Length": process_stride_length,
            "Swing_Time": process_swing_time,
            "Stance_Time": process_stance_time,
            }

        if (not is_exist):
            writer.writeheader()
        writer.writerow(data)


def convert_arduino_data(arduino_data):
    
    arduino_string = str(arduino_data.readline().strip())
    # Create an array with 3 values 
    data = re.split(",|b'|'", arduino_string)
    data = list(filter(None, data))
    return data


def start_plot():
    global start_flag
    start_flag = True
    print("Button Clicked")


def stop_plot():
    global start_flag
    start_flag = False
    global file_to_write
    global frame2
    if (len(file_to_write) > 1):
        set_report_avg(global_var.file_to_write)


def clear():
    global graph_canvas
    for item in graph_canvas.get_tk_widget().find_all():
       graph_canvas.get_tk_widget().delete(item)


def moving_average_filter():
    global to_avg
    global process_data
    if (len(to_avg) < 4):
        to_avg.append(global_var.knee_angles[-1])
    else:
        process_data.append(sum(to_avg)/len(to_avg))
        to_avg = []


# must stop current graph to switch to a different plot
def set_previous():
    global previous_flag
    global current_flag
    global online_flag
    if (not start_flag):
        previous_flag = True
        current_flag = False
        online_flag = False
        print("Set to previous")
        display_filename_prompt()

def set_current():
    global previous_flag
    global current_flag
    global online_flag
    if (not start_flag):
        current_flag = True
        previous_flag = False
        online_flag = False
        print("Set to current")
        display_filename_prompt()

def set_online():
    global previous_flag
    global current_flag
    global online_flag
    if (not start_flag):
        online_flag = True
        previous_flag = False
        current_flag = False
        print("Set to online")
        display_filename_prompt()


def click_input(event):
    global entry0
    global clicked 
    entry0.config(state=NORMAL)
    entry0.delete(0, END)
    clicked = True
    print("Clicked!")


def set_input():
    global previous_flag
    global entry0
    global clicked
    global prev_text
    global saving_text

    #print (entry0.get())
    clicked = False
    
    if previous_flag:
        global_var.prev_file = entry0.get()
        prev_text["text"] = f"{global_var.prev_file}"
    else:
        global_var.file_to_write = entry0.get()
        saving_text["text"] = f"{global_var.file_to_write}"


def display_filename_prompt():
    global previous_flag
    global entry0
    global entry_is_disabled

    entry0.delete(0, END)
    
    if (previous_flag):
        #print("in previous flag")
        text =  "Enter filename to plot"
        entry0.insert(0,text)

    else:
        #print("in the else statement")
        text = "Enter filename to record data on"
        entry0.insert(0, text)

def set_report_avg(filename):
    
    avg_swing, avg_stance = get_average_times(filename)
    avg_vel = get_average_velocity(filename)
    avg_stride = get_average_stride(filename)
    
    write_csv_report(avg_vel, avg_stride, avg_swing, avg_stance)

def next():
    global report_index
    if (report_index < len(reports)):
        report_index+=1
    else:
        report_index = 0
    print("pressed next")


def prev():
    global report_index
    if (report_index > 0):
        report_index-=1
    else:
        report_index = len(reports)-1
    print("pressed previous")


def display_report(frame): 
    global report_index

    if report_index == 0:
        report_velocity(frame)
    elif report_index == 1:
        report_stride_length(frame)
    elif report_index == 2:
        report_stance_time(frame)
    elif report_index == 3:
        report_swing_time(frame)



def main(): 
    global is_calibrate 
    global to_avg 
    global online_index
    global previous_flag
    global current_flag
    global online_flag
    global to_avg_knee
    global to_avg_shank 
    global to_avg_thigh 

    global v_o
    global stride_length
    global stride_length_list
    global to_avg_velocity
    global to_avg_stride_length
    global process_velocity
    global process_stride_length
    global process_swing_time
    global process_stance_time
    global foot_angle

    global entry0
    global clicked


    if (not clicked):
        display_filename_prompt()

    
    #entry0.bind("<Button-1>", click_input())
    #entry0.pack()
               
    if (start_flag and arduino_data_knee.inWaiting() != 0 and arduino_data_foot.inWaiting() != 0):
        # disablae changes in entry while running
        entry0.config(state=DISABLED)
           
        data_knee = convert_arduino_data(arduino_data_knee)
        data_foot = convert_arduino_data(arduino_data_foot)
        thigh_angles.append(float(data_knee[0]))
        shank_angles.append(float(data_knee[1]))
        foot_angles.append(float(data_foot[1]))
        foot_accel.append(float(data_foot[0]))

        # Calibration
        stop = True
        if (is_calibrate and len(thigh_angles) < 20):
            sleep(0.5)
            stop = False
            #print(shank_angles)
        elif (is_calibrate and len(thigh_angles) == 20):
            calibrate()
            is_calibrate = False
            print("Thigh offset: ", global_var.thigh_offset)
            print("Shank offset: ", global_var.shank_offset)
            print("Foot offset: ", global_var.foot_offset)
            print("End of calibration")
            sleep(5)
        
        if (stop):
            #print(data_knee)
            knee_joint_angle = knee.calculate_knee_angle(float(data_knee[0]), float(data_knee[1])) + global_var.shank_offset - global_var.thigh_offset
            #print("knee joint angle: ", knee_joint_angle)
            #thigh = knee.adjust_sensor_saggital(float(data_knee[0]))
            #shank = knee.adjust_sensor_saggital(float(data_knee[1]))
            global_var.knee_angles.append(knee_joint_angle) 
            #sag_shank_angles.append(shank)
            #sag_thigh_angles.append(thigh)

            foot_angle = float(data_foot[1]) - global_var.foot_offset
            #print("Foot angle: ", foot_angle)
        
            v_o = foot.velocity(v_o, float(data_foot[0]), 0.05)
            #print("v_0: ", v_o)
            # Add average filter to foot angles
            is_toe_off = foot.is_toe_off(foot_angle)
            is_heel_strike = foot.is_heel_strike(foot_angle)

        
            # Process data to compare with online data 
            process = False
            if (online_flag):
                if (len(to_avg) == 0 or abs(global_var.knee_angles[-1] - to_avg[0]) < 0.7 ):
                    to_avg.append(global_var.knee_angles[-1])
                    to_avg_velocity.append(v_o)

                else:
                    process_data.append(sum(to_avg)/len(to_avg))
                    process_velocity = sum(to_avg_velocity)/len(to_avg_velocity)
                    global_var.plot_online_data.append(online_knee_angle[online_index])
                    online_index+=5
                    if (online_index >= len(online_knee_angle)):
                        online_index = 0
                    to_avg = []
                    to_avg_velocity = []
                    process = True

                if (process):
                    drawnow(compare_online)
                    plt.pause(.00000001)

                knee_angle_display = round(process_data[-1],2) if (len(process_data)>0)  else round(knee_joint_angle,2)
                knee_angle_text["text"] = f"{knee_angle_display}"

                velocity_display = round(process_velocity, 2)
                velocity_text["text"] = f"{velocity_display}"


                process_stride_length += foot.stride_length(process_velocity, float(data_foot[0]), 0.04)
                if (v_o <= 0):
                    #stride_length_list.append(stride_length)
                    process_stride_length = 0;
                    process_stance_time = foot.stance_time(is_toe_off, is_heel_strike)
                else:
                    process_swing_time = foot.swing_time(is_toe_off, is_heel_strike)
                

                stride_length_display = round(process_stride_length, 2)
                stride_length_text["text"] = f"{stride_length_display}"

                swing_time_display = round(process_swing_time, 2)
                swing_time_text["text"] = f"{swing_time_display}"
            

            elif(current_flag):
    
                if (len(to_avg_knee) == 0 or abs(global_var.knee_angles[-1] - to_avg_knee[0]) < 0.7 ):
                    to_avg_knee.append(global_var.knee_angles[-1])
                    #to_avg_shank.append(shank)
                    #to_avg_thigh.append(thigh)
                    to_avg_velocity.append(v_o)
                else:
                    process_data.append(sum(to_avg_knee)/len(to_avg_knee))
                    #process_sag_shank.append(sum(to_avg_shank)/len(to_avg_shank))
                    #process_sag_thigh.append(sum(to_avg_thigh)/len(to_avg_thigh))
                    process_velocity = sum(to_avg_velocity)/len(to_avg_velocity)
                    #print(process_velocity)
                    process = True
                    to_avg_knee = []
                    #to_avg_shank = []
                    #to_avg_thigh = []
                    write_csv(f"{global_var.file_to_write}")

                if (process):
                    drawnow(plot)
                    plt.pause(.00000001)

                knee_angle_display = round(process_data[-1],2) if (len(process_data)>0)  else round(knee_joint_angle,2)
                knee_angle_text["text"] = f"{knee_angle_display}"

                velocity_display = round(process_velocity, 2)
                velocity_text["text"] = f"{velocity_display}"
                

                process_stride_length += foot.stride_length(process_velocity, float(data_foot[0]), 0.04)
                
                if (v_o <= 0):
                    #stride_length_list.append(stride_length)
                    process_stride_length = 0;
                    process_stance_time = foot.stance_time(is_toe_off, is_heel_strike)
                else:
                    process_swing_time = foot.swing_time(is_toe_off, is_heel_strike)

                stride_length_display = round(process_stride_length, 2)
                stride_length_text["text"] = f"{stride_length_display}"

                swing_time_display = round(process_swing_time, 2)
                swing_time_text["text"] = f"{swing_time_display}"

                stance_time_display = round(process_stance_time, 2)
                stance_time_text["text"] = f"{stance_time_display}"
            

            elif (previous_flag):
                drawnow(compare_previous_plot)
                plt.pause(.00000001)
                df = pd.read_csv(f'data/{global_var.prev_file}.csv')
                #print("fahfahfkahfka", len(df.Knee_Angle))
                #print(global_var.df_index-1)
                knee_angle_display = (round(df.Knee_Angle[global_var.df_index-1],3) if (len(df.Knee_Angle) > 1)  else 0)
                knee_angle_text["text"] = f"{knee_angle_display}"

                velocity_display = (round(df.Foot_Velocity[global_var.df_index-1], 5) if (len(df.Foot_Velocity) > 1)  else 0)
                
                velocity_text["text"] = f"{velocity_display}"

                stride_length_display = (round(df.Stride_Length[global_var.df_index-1], 3) if (len(df.Stride_Length) > 1)  else 0)
                stride_length_text["text"] = f"{stride_length_display}"

                swing_time_display = (round(df.Swing_Time[global_var.df_index-1], 3)  if (len(df.Swing_Time) > 1)  else 0)
                swing_time_text["text"] = f"{swing_time_display}"
    
                stance_time_display = (round(df.Stance_Time[global_var.df_index-1], 3)  if (len(df.Stance_Time) > 1)  else 0)
                stance_time_text["text"] = f"{stance_time_display}"
    elif not start_flag:
        display_report(frame2)

    
    window.after(1, main)


window = Tk()
window.wm_attributes("-transparentcolor", 'gray')

window.geometry("1000x820")
window.configure(bg = "#ffffff")


notebook = ttk.Notebook(window)
notebook.pack()
frame1 = Frame(notebook, width=1000, height = 800, bg="blue")
frame2 = Frame(notebook, width=1000, height = 800, bg="#3A4B53")
frame1.pack(fill="both", expand=1)
frame2.pack(fill="both", expand=2)
notebook.add(frame1, text="Acquisition")
notebook.add(frame2, text="Analysis")


report_velocity(frame2)
report_stride_length(frame2)
report_swing_time(frame2)
report_stance_time(frame2)

canvas = Canvas(
    frame1,
    bg = "#3A4B53",
    height = 800,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"gui/background.png")
background = canvas.create_image(
    499.5, 400.0,
    image=background_img)


img0 = PhotoImage(file = f"gui/img0.png")
b0 = Button(
    frame1,
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = start_plot,
    relief = "flat")


b0.place(
    x = 19, y = 537,
    width = 225,
    height = 62)

img5 = PhotoImage(file = f"gui/img5.png")
b5 = Button(
    frame1,
    image = img5,
    borderwidth = 0,
    highlightthickness = 0,
    command = stop_plot,
    relief = "flat")
    
b5.place(
    x = 268, y = 537,
    width = 225,
    height = 62)



entry0 = Entry(
    frame1,
    bd = 0,
    bg = "#FFCD00",
    highlightthickness = 0,
    font=('Century 12'),
    justify="center")


entry0.place(
    x = 20, y = 622,
    width = 325,
    height = 57)

entry0.bind("<Button-1>", click_input)

img1 = PhotoImage(file = f"gui/img1.png")
b1 = Button(
    frame1,
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = set_input,
    relief = "flat")


b1.place(
    x = 351, y = 622,
    width = 141,
    height = 57)

img2 = PhotoImage(file = f"gui/img2.png")
b2 = Button(
    frame1,
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = set_previous,
    relief = "flat")


b2.place(
    x = 517, y = 535,
    width = 118,
    height = 30)



img3 = PhotoImage(file = f"gui/img3.png")
b3 = Button(
    frame1,
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = set_current,
    relief = "flat")


b3.place(
    x = 517, y = 591,
    width = 118,
    height = 30)


img4 = PhotoImage(file = f"gui/img4.png")
b4 = Button(
    frame1,
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = set_online,
    relief = "flat")


b4.place(
    x = 517, y = 650,
    width = 118,
    height = 30)


knee_angle_display = round(process_data[-1],2) if (len(process_data)>0)  else round(knee_joint_angle,2)
knee_angle_text = Label(frame1, text=f"{knee_angle_display}", font= ('Helvetica 18'), bg= '#FFCD00')
knee_angle_text.place(x=820, y=187)

velocity_display = round(process_velocity, 2)
velocity_text = Label(frame1, text=f"{velocity_display}", font= ('Helvetica 18'), bg= '#FFCD00')
velocity_text.place(x=820, y=309)

stride_length_display = round(process_stride_length, 2)
stride_length_text = Label(frame1, text=f"{stride_length_display}", font= ('Helvetica 18'), bg= '#FFCD00')
stride_length_text.place(x=820, y=441)

swing_time_display = round(process_swing_time, 2)
swing_time_text = Label(frame1, text=f"{swing_time_display}", font= ('Helvetica 18'), bg= '#FFCD00')
swing_time_text.place(x=820, y=561)

stance_time_display = round(process_stance_time, 2)
stance_time_text = Label(frame1, text=f"{stance_time_display}", font= ('Helvetica 18'), bg= '#FFCD00')
stance_time_text.place(x=820, y=673)


saving_text = Label(frame1, text=f"{global_var.file_to_write}", font= ('Helvetica 8'), bg= '#FFCD00')
saving_text.place(x=69, y=710.11)


prev_text = Label(frame1, text=f"{global_var.prev_file}", font= ('Helvetica 8'), bg= '#FFCD00')
prev_text.place(x=69, y=765.04)


####################################    PAGE2########################

canvas_2 = Canvas(
    frame2,
    bg = "#3a4b53",
    height = 800,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas_2.place(x = 0, y = 0)

img0_2 = PhotoImage(file = f"gui/page2/img0.png")
b0 = Button(
    frame2,
    image = img0_2,
    borderwidth = 0,
    highlightthickness = 0,
    #command = btn_clicked,
    relief = "flat")

b0.place(
    x = 445, y = 651,
    width = 141,
    height = 57)

img1_2 = PhotoImage(file = f"gui/page2/img1.png")
b1_2 = Button(
    frame2,
    image = img1_2,
    borderwidth = 0,
    highlightthickness = 0,
    command = prev,
    relief = "flat")

b1_2.place(
    x = 628, y = 633,
    width = 118,
    height = 30)

img2_2 = PhotoImage(file = f"gui/page2/img2.png")
b2_2 = Button(
    frame2,
    image = img2_2,
    borderwidth = 0,
    highlightthickness = 0,
    command = next,
    relief = "flat")

b2_2.place(
    x = 767, y = 633,
    width = 118,
    height = 30)

entry0_img_2 = PhotoImage(file = f"gui/page2/img_textBox0.png")
entry0_bg_2 = canvas_2.create_image(
    276.5, 679.5,
    image = entry0_img_2)

entry0_2 = Entry(
    frame2,
    bd = 0,
    bg = "#ffd939",
    highlightthickness = 0)

entry0_2.place(
    x = 114, y = 651,
    width = 325,
    height = 55)

background_img_2 = PhotoImage(file = f"gui/page2/background.png")
background_2 = canvas_2.create_image(
    499.0, 413.5,
    image=background_img_2)



window.after(1, main)

window.resizable(False, False)
window.mainloop()





