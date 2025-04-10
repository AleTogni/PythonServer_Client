import tkinter as tk
from tkinter import *
from tkinter import messagebox


root = tk.Tk()

root.geometry("300x350")
root.title("Tris game")
label = tk.Label(root, text="Giochiamo a tris!", font=("Arial", 20))
label.pack(padx=10, pady=10)

canvas = Canvas(root, width=600, height=500, bg="white")
linea_verticale1 = canvas.create_line(105,230,105,40, width=7, fill="black")
linea_verticale2 = canvas.create_line(175,230,175,40, width=7, fill="black")
linea_orizzontale1 = canvas.create_line(50,100,230,100, width=7, fill="black")
linea_orizzontale2 = canvas.create_line(50,170,230,170, width=7, fill="black")
canvas.pack()

root.mainloop()
