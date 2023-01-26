from tkinter import font, messagebox
from tkinter import *
import random 

def obvio():
    messagebox.showinfo(message="Lo sabia", title="")

def button_hover(event):
    x = random.randint(10, 400)
    y = random.randint(10, 400)
    my_button_2.place(x=x, y=y)

def exit_(event):
    x = random.randint(10, 400)
    y = random.randint(10, 400)
    my_button_2.place(x=x, y=y)

    
root = Tk()
root.geometry("600x400")
root.configure(background="#FFC7FA")
root.title("RESPONDEME")

label_0 = Label(root, text="puedo buscar mas polola?", bg="#FFC7FA",fg="black", width=0,font=("BubbleGum",30))
label_0.place(x=90, y=60)

my_button_1 = Button(root, text="SI",width=2,height=1, font=("BubbleGum",30), bg="#FF4141", fg="white", command=obvio)
my_button_1.place(x=100, y=220)

my_button_2 = Button(root, text="NO", width=2, height=1, font=("BubbleGum",30), bg="#FF4141", fg="white")
my_button_2.place(x=350, y=220)

my_button_2.bind("<Enter>", button_hover)
my_button_2.bind("<Leave>", exit_)

root.mainloop()

