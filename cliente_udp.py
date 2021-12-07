import socket
import cv2, imutils
import numpy as np
import time
import base64 #Converte dados de imagem em formato texto
import os
import pyaudio, wave
import pickle, struct
import queue, threading

queue_audio = queue.Queue(maxsize=2000)

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

BUFFER_SIZE = 65536
UDP_PORT = 6000
BREAK = False


#Socket para o video
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Socket UDP do cliente
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFFER_SIZE)

host_ip = getIP() #Pegar host_ip e host_name dinamicamente
host_name = getHostName()
print("host_ip: ",host_ip)
print("host_name: ",host_name)

message = b"Hello, I'm client" #Mensagem enviada ao servidor
client_socket.sendto(message,(host_ip,UDP_PORT))

def receive_video():
    cv2.namedWindow("Video no Cliente")
    cv2.moveWindow("Video no Cliente",10,360)
    fps,st,frames_to_count,cnt = (0,0,200,0)
	
    #Receber datagrama de dados do servidor, no lado do cliente
    while True:
        packet,_ = client_socket.recvfrom(BUFFER_SIZE)
        data = base64.b64decode(packet,' /') #Fazendo decode do datagrama recebido
        npdata = np.frombuffer(data,dtype=np.uint8)
        frame = cv2.imdecode(npdata,1)
        cv2.imshow("Video no Cliente",frame) #Display do video no cliente

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            client_socket.close()
            os._exit(1)

        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count/(time.time()-st))
                st = time.time()
                cnt = 0
            except:
                cnt += 1


def receive_audio():
	
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFFER_SIZE)
	p = pyaudio.PyAudio()
	CHUNK = 10*1024
	stream = p.open(format=p.get_format_from_width(2),
					channels=2,
					rate=44100,
					output=True,
					frames_per_buffer=CHUNK)
					
	# create socket
	message = b'Hello from Client'
	client_socket.sendto(message,(host_ip,UDP_PORT-1))
	socket_address = (host_ip,UDP_PORT-1)
	
	def getAudioData():
		while True:
			frame,_= client_socket.recvfrom(BUFFER_SIZE)
			queue_audio.put(frame)
			print('Queue size...',queue_audio.qsize())
	t1 = threading.Thread(target=getAudioData, args=())
	t1.start()
	time.sleep(0.1)
	print('Now Playing...')
	while True:
		frame = queue_audio.get()
		stream.write(frame)


t1 = threading.Thread(target=receive_audio, args=())
t1.start()
#Executa paralelamente as 2 funções com Thread
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=2) as executor:
    #executor.submit(receive_audio)
    executor.submit(receive_video)