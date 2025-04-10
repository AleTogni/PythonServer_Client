import socket

server_address = ('127.0.0.1', 12345)
message = b'Ciao dal client UDP!'

client_socket = socket. socket(socket.AF_INET, socket. SOCK_DGRAM)
client_socket. sendto(message, server_address)

print(f"Inviato: {message.decode ()}")

data, server = client_socket.recvfrom (4096)
print(f"Ricevuto dal server: {data.decode()}")

client_socket.close()