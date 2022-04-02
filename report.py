from datetime import date
from os import path
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



def write_csv_report(foot_velocity, stride_length, swing_time, stance_time):
    
    global process_velocity
    fieldnames = ["Date", "Foot_Velocity", "Stride_Length", "Swing_Time", "Stance_Time"]
    today = date.today()
    data ={
        "Date": today.strftime("%d/%m/%Y"),
        #"Knee_Angle": knee_angle,
        "Foot_Velocity": foot_velocity, 
        "Stride_Length": stride_length,
        "Swing_Time": swing_time,
        "Stance_Time": stance_time
    }
    is_exist = path.exists(f"average_report.csv")

    if is_exist:
        df = pd.read_csv('average_report.csv')
        # if the date is in the file 
        # then replace 
        if (df['Date'] == today.strftime("%d/%m/%Y")).any():
            # date is in file so we replace
            index = df.index[df['Date'] == today.strftime("%d/%m/%Y")].tolist()
            col = ["Foot_Velocity", "Stride_Length", "Swing_Time", "Stance_Time"]
            df.loc[index, col] = [foot_velocity, stride_length, swing_time, stance_time]
            # writing into the file
            df.to_csv("average_report.csv", index=False)
            print("replaced")
        else:
            #File exists but does not contain date
            with open('average_report.csv', 'a') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator = '\n')
                writer.writerow(data)
        
    else: #file does not exist so we have to add the header before adding data
        with open('average_report.csv', 'a') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator = '\n')
            writer.writeheader()
            writer.writerow(data)

        
def average_col(filename):
    df = pd.read_csv(f'data/{filename}.csv')
    return df.mean(axis=0)
    

def get_average_times(filename):
    # average swing time
    df = pd.read_csv(f'data/{filename}.csv')
    avg_swing = sum(df.Swing_Time)/(len(df.Swing_Time)-1)
    # average stance time
    avg_stance = sum(df.Stance_Time)/(len(df.Stance_Time)-1)
    return (avg_swing, avg_stance)


def get_average_velocity(filename):
    df = pd.read_csv(f'data/{filename}.csv')
    to_avg = []
    avg_list = []
    for vel in df.Foot_Velocity:
        if (vel != 0):
            to_avg.append(vel)
        elif (len(to_avg) > 0):
            avg_list.append(sum(to_avg)/len(to_avg))

    if (len(avg_list) > 0):
        return sum(avg_list)/len(avg_list)
    return ""


def get_average_stride(filename):
    df = pd.read_csv(f'data/{filename}.csv')
    to_avg = []
    avg_list = []
    for stride in df.Stride_Length:
        if (stride != 0):
            to_avg.append(stride)
        elif (len(to_avg) > 0):
            avg_list.append(sum(to_avg)/len(to_avg))

    if (len(avg_list) > 0):
        return sum(avg_list)/len(avg_list)
    return ""



def report_velocity(frame):
    df = pd.read_csv('average_report.csv')
    x = df.Date

    fig = Figure(figsize=(3,4), dpi=70)
    plot = fig.add_subplot(111)
    plot.plot(x, df.Foot_Velocity, color = 'b', marker='o')
    plot.set_title("Changes in Velocity Over Time")
    plot.set_xlabel('Date (day/month/year)')
    plot.set_ylabel('Velocity (m/s)')
    plot.set_xticklabels(plot.get_xticks(), rotation=0)
   

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().place(x=35, y=147, width=279, height=195)
    canvas.draw()

    '''
    # Load data
    df = pd.read_csv('average_report.csv'-)
    # Plot
    plt.figure(figsize=(6.8, 4.2))
    x = df.Date
    plt.plot(x, df.Foot_Velocity, color = 'b', marker='o')
    plt.xlabel('Date (day/month/year)')
    plt.ylabel('Velocity (m/s)')
    plt.title("Changes in Velocity Over Time")
    plt.show()
    '''


def report_stride_length(frame):
    
    df = pd.read_csv('average_report.csv')
    x = df.Date

    fig = Figure(figsize=(3,4), dpi=80)
    plot = fig.add_subplot(111)
    plot.plot(x, df.Stride_Length, color = 'b', marker='o')
    plot.set_title("Changes in Stride Length Over Time")
    plot.set_xlabel('Date (day/month/year)')
    plot.set_ylabel('Stride Length (m)')
    plot.set_xticklabels(plot.get_xticks(), rotation=0)
   

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().place(x=363, y=147, width=279, height=195)
    canvas.draw()




    '''
    # Load data
    df = pd.read_csv('average_report.csv')
    # Plot
    plt.figure(figsize=(6.8, 4.2))
    x = df.Date
    plt.plot(x, df.Stride_Length, color = 'b', marker='o')
    plt.xlabel('Date (day/month/year)')
    plt.ylabel('Stride Length (m)')
    plt.title("Changes in Stride Length Over Time")
    plt.show()
    '''

def report_swing_time(frame):
    df = pd.read_csv('average_report.csv')
    x = df.Date

    fig = Figure(figsize=(3,4), dpi=80)
    plot = fig.add_subplot(111)
    plot.plot(x, df.Swing_Time, color = 'b', marker='o')
    plot.set_title("Changes in Swing Time Over Time")
    plot.set_xlabel('Date (day/month/year)')
    plot.set_ylabel('Swing Time (s)')
    plot.set_xticklabels(plot.get_xticks(), rotation=0)
   
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().place(x=35, y=414, width=279, height=195)
    canvas.draw()


    '''
    plt.figure(figsize=(5.8, 4.2))
    x = df.Date
    plt.plot(x, df.Swing_Time, color = 'b', marker='o')
    plt.xlabel('Date (day/month/year)')
    plt.ylabel('Swing Time (s)')
    plt.title("Changes in Swing Time Over Time")
    plt.show()
    '''


def report_stance_time(frame):
    df = pd.read_csv('average_report.csv')
    x = df.Date

    fig = Figure(figsize=(3,4), dpi=80)
    plot = fig.add_subplot(111)
    plot.plot(x, df.Stance_Time, color = 'b', marker='o')
    plot.set_title("Changes in Stance Time Over Time")
    plot.set_xlabel('Date (day/month/year)')
    plot.set_ylabel('Stance Time (s)')
    plot.set_xticklabels(plot.get_xticks(), rotation=0)
   
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().place(x=363, y=414, width=279, height=195)
    canvas.draw()

    

    '''
    # Load data
    df = pd.read_csv('average_report.csv')
    # Plot
    plt.figure(figsize=(6.8, 4.2))
    x = df.Date
    plt.plot(x, df.Stance_Time, color = 'b', marker='o')
    plt.xlabel('Date (day/month/year)')
    plt.ylabel('Stance Time (s)')
    plt.title("Changes in Stance Time Over Time")
    plt.show()
    '''