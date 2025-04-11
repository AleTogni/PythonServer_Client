import tkinter as tk
import socket
import threading

# Connessione al server
server_address = ('127.0.0.1', 12345)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto(b'Ciao, mi voglio connettere', server_address)
simbolo = client_socket.recv(4096).decode()[-1]

# GUI Setup
root = tk.Tk()
root.title(f"Tris - Giocatore {simbolo}")
status_label = tk.Label(root, text="In attesa...", font=('Arial', 14))
status_label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack()

turno_mio = False

def invia_mossa(r, c):
    global turno_mio
    if not turno_mio:
        return
    if buttons[r][c]['text'] == '':
        client_socket.sendto(f"{r},{c}".encode(), server_address)
        turno_mio = False

buttons = []
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(button_frame, text='', font=('Arial', 40), width=3, height=1,
                        command=lambda r=i, c=j: invia_mossa(r, c))
        btn.grid(row=i, column=j, padx=5, pady=5)
        row.append(btn)
    buttons.append(row)

def ricevi():
    global turno_mio
    while True:
        try:
            data, _ = client_socket.recvfrom(4096)
            msg = data.decode()
            print("Ricevuto:", msg)

            if msg == "TOCCA A TE":
                turno_mio = True
                status_label.config(text="È il tuo turno!")
            elif msg == "ATTENDI":
                status_label.config(text="Aspetta l'altro giocatore...")
            elif msg.startswith("Mossa"):

                simbolo_mossa = msg.split()[1]
                coords = msg.split()[-1]
                r, c = map(int, coords.split(','))
                buttons[r][c].config(text=simbolo_mossa)
            elif "|" in msg or "-" in msg:
                pass
            elif msg.startswith("VITTORIA") or msg == "Pareggio!":
                status_label.config(text=msg)
                break
        except:
            break

threading.Thread(target=ricevi, daemon=True).start()

root.mainloop()
client_socket.close()
