import socket


server_address = ('192.168.132.220', 12345)   # 192.168.81.220
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)

print(f"Server UDP in ascolto su {server_address[0]}:{server_address[1]}")

clients = []
griglia = [[" " for _ in range(3)] for _ in range(3)]
turno = 0  # 0 = client 1 (X), 1 = client 2 (O)

def check_vittoria(griglia, simbolo):
    for i in range(3):
        if all(griglia[i][j] == simbolo for j in range(3)) or all(griglia[j][i] == simbolo for j in range(3)):
            return True
    if all(griglia[i][i] == simbolo for i in range(3)) or all(griglia[i][2 - i] == simbolo for i in range(3)):
        return True
    return False

def griglia_piena(griglia):
    return all(griglia[i][j] != " " for i in range(3) for j in range(3))

def invia_a_tutti(msg):
    for c in clients:
        server_socket.sendto(msg.encode(), c)

def griglia_to_string(griglia):
    rows = []
    for r in griglia:
        rows.append(" | ".join(r))
    return "\n---------\n".join(rows)

print("In attesa di due giocatori...")

# Fase connessione giocatori
while len(clients) < 2:
    data, addr = server_socket.recvfrom(4096)
    if addr not in clients:
        clients.append(addr)
        print(f"Giocatore connesso: {addr}")
        server_socket.sendto(f"Sei il giocatore {'X' if len(clients)==1 else 'O'}".encode(), addr)

# Partita
invia_a_tutti("Inizio partita!")

simboli = ['X', 'O']

while True:
    current_client = clients[turno]
    other_client = clients[1 - turno]
    simbolo = simboli[turno]

    server_socket.sendto("TOCCA A TE".encode(), current_client)
    server_socket.sendto("ATTENDI".encode(), other_client)

    data, addr = server_socket.recvfrom(4096)
    try:
        r, c = map(int, data.decode().split(","))
        if griglia[r][c] != " ":
            server_socket.sendto("Mossa non valida".encode(), addr)
            continue
        griglia[r][c] = simbolo
    except:
        continue

    # Stampa la griglia aggiornata e invia a tutti i client
    invia_a_tutti(f"Mossa {simbolo} in {r},{c}")
    invia_a_tutti(griglia_to_string(griglia))

    if check_vittoria(griglia, simbolo):
        invia_a_tutti(f"VITTORIA di {simbolo}")
        break
    elif griglia_piena(griglia):
        invia_a_tutti("Pareggio!")
        break

    turno = 1 - turno

server_socket.close()
