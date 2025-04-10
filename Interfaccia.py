import tkinter as tk

root = tk.Tk()

root.geometry("600x500")
root.title("Tris game")
label = tk.Label(root, text="Giochiamo a tris!", font=("Arial", 20))
label.pack(padx=10, pady=10)

root.mainloop()
