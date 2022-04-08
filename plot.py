from operator import index
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from py import process
import global_var
import pandas as pd
from time import sleep

def plot_knee_flexion():
    plt.subplot(211)
    plt.title("Gait Data: Knee Flex/Extension")
    plt.ylim(-10,200)
    plt.plot(global_var.knee_angles, 'bo-', label="knee angle")
    plt.grid(True)
    plt.ylabel("Knee Angle (deg)")
    plt.legend(loc='upper right')

    # plots the most recent data 
    if (len(global_var.knee_angles) > 50):
        global_var.knee_anglezzs.pop(0)


def plot_sagittal_angle():
    plt.subplot(212)
    plt.title("Gait Data: Thigh and Shank Sagittal Angle")
    plt.ylim(-90,90)
    plt.plot(global_var.sag_shank_angles, 'ro-', label="shank")
    plt.plot(global_var.sag_thigh_angles, 'go-', label="thigh")
    plt.grid(True)
    plt.ylabel("Sagittal Angle (deg)")
    plt.legend(loc='upper right')

     # plots the most recent data 
    if (global_var.cnt > 50):
        global_var.sag_shank_angles.pop(0)
        global_var.sag_thigh_angles.pop(0)


def plot():
    #plt.subplot(211)
    plt.title("Gait Data: Knee Flex/Extension")
    plt.ylim(0,90)
    plt.plot(global_var.process_data, 'bo-', label="knee angle")
    plt.grid(True)
    plt.ylabel("Knee Angle (deg)")
    plt.legend(loc='upper right')

    '''
    plt.subplot(212)
    plt.title("Gait Data: Thigh and Shank Sagittal Angle")
 
    plt.plot(process_sag_shank, 'ro-', label="shank")
    plt.plot(process_sag_thigh, 'go-', label="thigh")
    plt.grid(True)
    plt.ylabel("Sagittal Angle (deg)")
    plt.legend(loc='upper right')

    plt.tight_layout()
    '''

    # plots the most recent data 
    if (len(global_var.process_data) > 50):
        global_var.process_data.pop(0)
        #sag_shank_angles.pop(0)
        #sag_thigh_angles.pop(0)
        #global_var.process_sag_thigh.pop(0)
        #global_var.process_sag_shank.pop(0) 
        


# compares data we got from last time 
# filename must be a csv 
def compare_previous_plot():
  
    df = pd.read_csv(f'data/{global_var.prev_file}.csv')

    if (len(df.index-1) > global_var.df_index): 
        global_var.df_prev_angles.append(df.Knee_Angle[global_var.df_index])
        global_var.df_index+=1
        plt.title("Gait Data: Knee Flex/Extension")
        plt.ylabel("Knee Angle (deg)")
        plt.ylim(0,90)

        #plt.plot(knee_angles, 'bo-', label="knee angle")
        plt.plot(global_var.df_prev_angles, 'go-', label=f"{global_var.prev_file}")
        plt.grid(True)
        #plt.ylabel("Knee Angle (deg)")
        plt.legend(loc='upper right')

        if (len(global_var.df_prev_angles)> 50):
            global_var.df_prev_angles.pop(0)
    else:
        global_var.df_index = 1
        sleep(3)
    
    global_var.df_index = global_var.df_index


# Right now just plots current online plot
def compare_online():
    
    plt.title("Gait Data: Knee Flex/Extension")
    plt.ylim(0,90)
    plt.plot(global_var.plot_online_data, 'bo-', label="Online knee angle")
    plt.grid(True)
    plt.ylabel("Knee Angle (deg)")
    plt.legend(loc='upper right')

    plt.ylim(0,90)
    plt.plot(global_var.process_data, 'go-', label="Patient knee angle")
    plt.grid(True)
    plt.ylabel("Knee Angle (deg)")
    plt.legend(loc='upper right')


    # plots the most recent data 
    if (global_var.cnt > 50):
        global_var.knee_angles.pop(0)

    if (len(global_var.plot_online_data) > 50):
        global_var.plot_online_data.pop(0)
        
    if (len(global_var.process_data) > 50):
        global_var.process_data.pop(0)

