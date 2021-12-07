import socket
import cv2, imutils
import time
import numpy as np
import base64 #Converte dados de imagem em formato texto
import os #funcões DE INTERFACE COM O SISTEMA OPERACIONAL teste
import queue
import wave #manipular audio
import pyaudio
import pickle, struct

#Fila 'q' dos frames
q = queue.Queue(maxsize=10)

#==============================#
#= Gerar arquivo de Audio wav =#
#==============================#

name_Video = "./Videos/Sony_Demo_720p.mp4"
command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(name_Video,"audio.wav")
os.system(command) #executa comando ffmpeg

#==============================#
#=           GET_IP           =#
#==============================#

def getIP():
    return socket.gethostbyname(socket.gethostname())

def getHostName():
    return socket.gethostname()

#==============================#
#=       Inicializações       =#
#==============================#
HOST = ''
UDP_PORT = 6000
BUFFER_SIZE = 65536


host_ip = getIP() #Pegar host_ip e host_name dinamicamente
host_name = getHostName()
print("host_ip: ",host_ip)
print("host_name: ",host_name)

#Conexão de Video
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Socket UDP do servidor
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFFER_SIZE)
socket_address = (host_ip,UDP_PORT)
server_socket.bind(socket_address) #Iniciando servidor no socket_address
print("(Video) Ouvindo em: ",socket_address)

#Conexão para Audio
server_socket_audio = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Socket UDP do servidor
server_socket_audio.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFFER_SIZE)
socket_address_audio = (host_ip,UDP_PORT-1) #Porta -1 para o Audio
server_socket_audio.bind(socket_address_audio) #Iniciando servidor no socket_address_audio
print("(Audio) Ouvindo em: ",socket_address_audio)


#==============================#
#=       Tratando Video       =#
#==============================#
video = cv2.VideoCapture("./Videos/Sony_Demo_720p.mp4") #Captura do video
FPS = video.get(cv2.CAP_PROP_FPS) #Pegando FPS do video original
global TS
TS = (0.5/FPS)
BREAK = False
print("FPS:",FPS," TS:",TS)
totalNoFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
durationInSeconds = float(totalNoFrames) / float(FPS)
d = video.get(cv2.CAP_PROP_POS_MSEC)
print(durationInSeconds,d)


def video_stream_generator():
    WIDTH = 400 #Caber em um único datagrama
    while(video.isOpened()):
        try:
            _,frame = video.read()
            frame = imutils.resize(frame,width=WIDTH)
            q.put(frame)
        except:
            os._exit(1) #fecha transmissao
    print("Transmissão Fechada")
    BREAK = True
    video.release()


def video_stream():
    global TS
    fps,st,frames_to_count,cnt = (0,0,1,0)

    while True: #Loop para o servidor receber dados de cada cliente no endereço socket
        msg,client_addr = server_socket.recvfrom(BUFFER_SIZE) #Recebendo mensagem msg do cliente
        print("Conexão recebida de: ",client_addr)
        print("Mensagem recebida: ",msg)

        #Enviar imagens ao cliente
        while(True):
            frame = q.get() #pega frame da fila
            encoded,buffer = cv2.imencode('.jpeg',frame,[cv2.IMWRITE_JPEG_QUALITY,80]) #Colocar/Encode a imagem em JPEG com qualidade de 80% após o resize
            message = base64.b64encode(buffer) #Converter dado binario em texto e vice versa com base64
            server_socket.sendto(message,client_addr) #Envio da mensagem ao cliente (do frame)
            
            #Controle de frames ao enviar a 'message'    
            if cnt == frames_to_count:
                try:
                    fps = (frames_to_count/(time.time()-st))
                    st = time.time()
                    cnt = 0
                    if fps > FPS:
                        TS += 0.001
                    elif fps < FPS:
                        TS -=0.001
                    else:
                        pass
                except:
                    pass
            cnt +=1
            cv2.imshow('Video Servidor', frame)
            key = cv2.waitKey(int(1000*TS)) & 0xFF	
            if key == ord('q'):
                os._exit(1)
            
#enviar audio
def audio_stream():
    s = socket.socket()
    s.bind((host_ip, (UDP_PORT-1)))

    s.listen(5)
    CHUNK = 1024
    wf = wave.open("audio.wav", 'rb')
    p = pyaudio.PyAudio()
    print('(Audio) Servidor ouvindo em:)',(host_ip, (UDP_PORT-1)))
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

    client_socket,addr = s.accept()

    while True:
        if client_socket:
            while True:
                data = wf.readframes(CHUNK)
                a = pickle.dumps(data)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)


#Executa paralelamente as 3 funções com Thread
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as executor:
    executor.submit(audio_stream)
    executor.submit(video_stream_generator)
    executor.submit(video_stream)