import socket

HOST = ''
PORT = 6000
BUFFER_SIZE = 1024

#Servidor de Streaming na porta 6000 - teste
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
    udp.bind((HOST, PORT))

    while True:
        data, client = udp.recvfrom(BUFFER_SIZE)
        udp.sendto(b'Hello world', client)
        print(data.decode('utf-8'))