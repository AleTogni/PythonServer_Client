import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.geometry("300x400")
root.title("Tris game")

# Etichetta in alto
label = tk.Label(root, text="Giochiamo a tris!", font=("Arial", 20))
label.pack(pady=10)

# Contenitore per i bottoni
button_frame = tk.Frame(root)
button_frame.pack()

def on_click(row, col):
    print(f"Hai cliccato sulla cella {row},{col}")
    if buttons[row][col]['text'] == '':
        buttons[row][col].config(text='X')

buttons = []
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(button_frame, text='', font=('Arial', 20), width=5, height=2,
                        command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j, padx=2, pady=2)
        row.append(btn)
    buttons.append(row)

root.mainloop()
