import socket

server_address = ('127.0.0.1', 12345)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)

print(f"Server UDP in ascolto su {server_address[0]}:{server_address[1]}")

while True:
    data, client_address = server_socket.recvfrom(4096)
    print(f"Ricevuto da {client_address}: {data.decode()}")

    response = data.upper()
    server_socket.sendto(response, client_address)
    print(f"Inviato a {client_address}: {response.decode()}")

