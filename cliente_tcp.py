import socket
import random
import time

HOST = '127.0.0.1'
PORT_TCP = 5000

#Conexão com Servidor Gerenciador de Serviço por TCP na porta 5000
id = random.randint(1, 100)
message = 'Oi, eu sou o cliente ' + str(id)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
    tcp.connect((HOST, PORT_TCP))
    while True:
        tcp.sendall(message.encode())
        data = tcp.recv(1024)
        print(data.decode('utf-8'))
        time.sleep(1)