import socket

HOST = ''
PORT = 6000

# Servidor de Streaming na porta 6000
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
    udp.bind((HOST, PORT))

    while True:
        data, client = udp.recvfrom(1024)
        udp.sendto(b'Hello world', client)
        print(data.decode('utf-8'))
