from tkinter import *


def start_plot():
    print("Button Clicked")


def enter_input():
    pass


window = Tk()

window.geometry("1440x1024")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 1024,
    width = 1440,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = start_plot,
    relief = "flat")

b0.place(
    x = 58, y = 789,
    width = 372,
    height = 72)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = enter_input,
    relief = "flat")

b1.place(
    x = 308, y = 907,
    width = 372,
    height = 57)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    244.5, 935.5,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#c4c4c4",
    highlightthickness = 0)

entry0.place(
    x = 59, y = 907,
    width = 371,
    height = 55)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    720.0, 482.0,
    image=background_img)

window.resizable(False, False)
window.mainloop()
