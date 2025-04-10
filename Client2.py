import socket

server_address = ('127.0.0.1', 12345)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Handshake
client_socket.sendto(b'Ciao, mi voglio connettere', server_address)

data, _ = client_socket.recvfrom(4096)
print(data.decode())

while True:
    data, _ = client_socket.recvfrom(4096)
    msg = data.decode()
    print(msg)

    # Se è la griglia, stampala in modo visivo
    if "|" in msg or "-" in msg:
        print("\nGriglia aggiornata:")
        print(msg)

    if msg == "TOCCA A TE":
        r = int(input("Riga (0-2): "))
        c = int(input("Colonna (0-2): "))
        client_socket.sendto(f"{r},{c}".encode(), server_address)
    elif msg.startswith("VITTORIA") or msg == "Pareggio!":
        break

client_socket.close()
