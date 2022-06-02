import cv2
from tkinter import *
from PIL import Image, ImageTk
from utils import *

win = Tk()
win.geometry("820x500+250+50")
win.title("Main Window")
win.configure(bg='white')

shade = StringVar()
shade.set("NO")

transparency = DoubleVar()
transparency.set(0.1)

frame1 = Frame(win, width=700, height=500)
frame1.pack(side=LEFT)
frame1.configure(bg='white')

frame2 = Frame(win, width=120, height=500)
frame2.pack(side=RIGHT, expand=True)
frame2.configure(bg='white')

T_image = Image.open("logo.png")
resize_Timage = T_image.resize((80, 80))
T_img = ImageTk.PhotoImage(resize_Timage)
T_label = Label(frame2, image=T_img)
T_label.image = T_img
T_label.grid(column=0, row=0, pady=(0, 50))
T_label.configure(background="white")

Button(master=frame2, height=1, width=2, bg="#f25555",
       command=lambda: shade.set("orange")).grid(column=0, row=1, padx=5, pady=5)
Button(master=frame2, height=1, width=2, bg="purple",
       command=lambda: shade.set("purple")).grid(column=0, row=3, padx=5, pady=5)
Button(master=frame2, height=1, width=2, bg="#fca7f2",
       command=lambda: shade.set("pink")).grid(column=0, row=4, padx=5, pady=5)
Button(master=frame2, height=1, width=2, bg="red",
       command=lambda: shade.set("red")).grid(column=0, row=7, padx=5, pady=5)
Button(master=frame2, height=1, width=2, bg="grey",
       command=lambda: shade.set("NO")).grid(column=0, row=8, padx=5, pady=5)

def update_transparency(values):
    transparency.set(scale.get()/100)

scale = Scale(frame2, from_= 0, to = 100, length = 100, command = update_transparency, orient= 'horizontal')
scale.grid(column = 0, row = 9 , pady= 5)

w = 700
h = 480
video_frame = Label(frame1, width=w, height=h)
video_frame.pack(side=TOP)

cap = cv2.VideoCapture(1)
while True:
    ret, img = cap.read()
    if ret:
        img = cv2.resize(img, (w, h))
        img = cv2.flip(img, 1)
        try:
            output = apply_lipstick(img, shade.get(), transparency.get())
        except:
            output = cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(output)
        finalImage = ImageTk.PhotoImage(image=image)
        video_frame.configure(image=finalImage)
    win.update()
