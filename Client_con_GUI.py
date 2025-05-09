import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import socket
import threading

# Finestra per il nome
root = tk.Tk()
root.withdraw()
nome_utente = simpledialog.askstring("Nome Utente", "Inserisci il tuo nome:")
if not nome_utente:
    exit()
root.deiconify()

# Connessione
server_address = ('127.0.0.1', 12345)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto(f"NOME:{nome_utente}".encode(), server_address)
simbolo = client_socket.recv(4096).decode()[-1]

# GUI
root.title(f"Tris - {nome_utente} ({simbolo})")
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

# GRIGLIA
game_frame = tk.Frame(main_frame)
game_frame.grid(row=0, column=0, padx=10)

status_label = tk.Label(game_frame, text="In attesa...", font=('Arial', 14))
status_label.pack()

button_frame = tk.Frame(game_frame)
button_frame.pack()

buttons = []
turno_mio = False

def invia_mossa(r, c):
    global turno_mio
    if not turno_mio:
        return
    if buttons[r][c]['text'] == '':
        client_socket.sendto(f"{r},{c}".encode(), server_address)
        turno_mio = False

for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(button_frame, text='', font=('Arial', 40), width=3, height=1,
                        command=lambda r=i, c=j: invia_mossa(r, c))
        btn.grid(row=i, column=j, padx=5, pady=5)
        row.append(btn)
    buttons.append(row)

# CHAT
chat_frame = tk.Frame(main_frame)
chat_frame.grid(row=0, column=1, padx=10, sticky="n")

chat_log = scrolledtext.ScrolledText(chat_frame, width=30, height=20, state='disabled', wrap='word')
chat_log.pack(pady=(0, 5))

chat_entry = tk.Entry(chat_frame, width=30)
chat_entry.pack()

def invia_chat(event=None):
    msg = chat_entry.get()
    if msg:
        client_socket.sendto(f"CHAT:{nome_utente}: {msg}".encode(), server_address)
        chat_entry.delete(0, tk.END)
        aggiungi_chat(f"Tu: {msg}")

def aggiungi_chat(msg):
    chat_log['state'] = 'normal'
    chat_log.insert(tk.END, msg + '\n')
    chat_log['state'] = 'disabled'
    chat_log.yview(tk.END)

chat_entry.bind("<Return>", invia_chat)

# Ricezione
def ricevi():
    global turno_mio
    while True:
        try:
            data, _ = client_socket.recvfrom(4096)
            msg = data.decode()

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
            elif msg.startswith("VITTORIA") or msg == "Pareggio!":
                status_label.config(text=msg)
            elif msg.startswith("Vuoi giocare di nuovo?"):
                risposta = messagebox.askquestion("Partita finita", "Vuoi giocare di nuovo?")
                if risposta == "yes":
                    client_socket.sendto("S".encode(), server_address)
                    for row in buttons:
                        for btn in row:
                            btn.config(text="")
                else:
                    client_socket.sendto("N".encode(), server_address)
                    root.quit()
                    break
            elif msg.startswith("Fine partita"):
                messagebox.showinfo("Fine", msg)
                root.quit()
                break
            elif msg.startswith("CHAT:"):
                aggiungi_chat(msg[5:])
        except:
            break

threading.Thread(target=ricevi, daemon=True).start()
root.mainloop()
client_socket.close()
