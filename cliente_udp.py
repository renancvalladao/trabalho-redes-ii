import socket
import cv2, imutils
import numpy as np
import time
import base64 #Converte dados de imagem em formato texto

BUFFER_SIZE = 65536
UDP_PORT = 6000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Socket UDP do cliente
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFFER_SIZE)
host_name = socket.gethostname()
host_ip = '192.168.1.106'
print(host_ip)

message = b"Hello" #Mensagem enviada ao servidor
client_socket.sendto(message,(host_ip,UDP_PORT))

#Receber datagrama de dados do servidor, no lado do cliente
while True:
    packet,_ = client_socket.recvfrom(BUFFER_SIZE)
    data = base64.b64decode(packet,' /') #Fazendo decode do datagrama recebido
    npdata = np.fromstring(data,dtype=np.uint8)
    frame = cv2.imdecode(npdata,1)
    cv2.imshow("Transmissao",frame) #Display do video no cliente

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        client_socket.close()
        break


''' COMENTADO
HOST = '127.0.0.1'
PORT_UDP = 6000
BUFFER_SIZE = 1024

#Conexão com Servidor de Streaming por UDP na porta 6000
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
    udp.sendto(b'Hello from client', (HOST, PORT_UDP))
    data = udp.recv(BUFFER_SIZE)
print(data.decode('utf-8'))


'''
