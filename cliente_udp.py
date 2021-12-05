import socket

HOST = '127.0.0.1'
PORT_UDP = 6000
BUFFER_SIZE = 1024

# Conexão com Servidor de Streaming por UDP na porta 6000
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
    udp.sendto(b'Hello from client', (HOST, PORT_UDP))
    data = udp.recv(BUFFER_SIZE)
print(data.decode('utf-8'))
