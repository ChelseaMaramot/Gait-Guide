from tkinter import *


def btn_clicked():
    print("Button Clicked")


window = Tk()

window.geometry("1000x800")
window.configure(bg = "#3a4b53")
canvas_2 = Canvas(
    window,
    bg = "#3a4b53",
    height = 800,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas_2.place(x = 0, y = 0)

img0_2 = PhotoImage(file = f"gui/page2/img0.png")
b0 = Button(
    image = img0_2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 445, y = 651,
    width = 141,
    height = 57)

img1_2 = PhotoImage(file = f"gui/page2/img1.png")
b1_2 = Button(
    image = img1_2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b1_2.place(
    x = 628, y = 633,
    width = 118,
    height = 30)

img2_2 = PhotoImage(file = f"gui/page2/img2.png")
b2_2 = Button(
    image = img2_2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
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

window.resizable(False, False)
window.mainloop()
