import socket
import cv2, imutils
import time
import numpy as np
import base64 #Converte dados de imagem em formato texto

HOST = ''
UDP_PORT = 6000
BUFFER_SIZE = 65536

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Socket UDP do servidor
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFFER_SIZE)
host_name = socket.gethostname()
host_ip = '192.168.1.106' #Host local
print("host_ip: ",host_ip)

socket_address = (host_ip,UDP_PORT)
server_socket.bind(socket_address) #Iniciando servidor no socket_address
print("Ouvindo em: ",socket_address)

video = cv2.VideoCapture("./Videos/Sony_Demo_720p.mp4") #Captura do video
#fps,st,frames_to_count,cnt = (0,0,20,0) #Variáveis para obter framerate

while True: #Loop para o servidor receber dados de cada cliente no endereço socket
    msg,client_addr = server_socket.recvfrom(BUFFER_SIZE) #Recebendo mensagem msg do cliente
    print("Conexão recebida de: ",client_addr)
    print("Mensagem recebida: ",msg)

    #Enviar imagens ao cliente
    WIDTH = 400 #Caber em um único datagrama
    while(video.isOpened()):
        _,frame = video.read()
        frame = imutils.resize(frame,width=WIDTH)
        encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80]) #Colocar/Encode a imagem em JPEG com qualidade de 80% após o resize
        message = base64.b64encode(buffer) #Converter dado binario em texto e vice versa com base64
        server_socket.sendto(message,client_addr) #Envio da mensagem ao cliente

        cv2.imshow("Transmitindo video",frame) #Display da janela de transmissão no servidor
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            server_socket.close()
            break



''' COMENTADO
#Servidor de Streaming na porta 6000
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
    udp.bind((HOST, UDP_PORT))

    while True:
        data, client = udp.recvfrom(BUFFER_SIZE)
        udp.sendto(b'Hello world', client)
        print(data.decode('utf-8'))

'''