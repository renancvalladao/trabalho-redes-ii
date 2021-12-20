import base64  # Converte dados de imagem em formato texto
import os
import pickle
import queue
import socket
import threading
import time

import cv2
import mensagens
import numpy as np
import pyaudio

pararAudio = False


def getIP():
    return socket.gethostbyname(socket.gethostname())


def getHostName():
    return socket.gethostname()


def reproduzirVideo(nomeVideo):
    global pararAudio
    pararAudio = False
    message = mensagens.REPRODUZIR_VIDEO.encode("utf-8")  # Mensagem enviada ao servidor
    client_socket.sendto(message, (host_ip, UDP_PORT))
    client_socket.sendto(nomeVideo.encode("utf-8"), (host_ip, UDP_PORT))
    queue_audio = queue.Queue(maxsize=2000)

    video_mensagem = client_socket.recv(BUFFER_SIZE)
    video_mensagem = video_mensagem.decode("utf-8")
    print(video_mensagem)
    if video_mensagem == 'VideoNotFound':
        return False

    def receive_video():
        cv2.namedWindow("Video no Cliente")
        cv2.moveWindow("Video no Cliente", 10, 360)

        # Receber datagrama de dados do servidor, no lado do cliente
        while True:
            packet, _ = client_socket.recvfrom(BUFFER_SIZE)
            data = base64.b64decode(packet, ' /')  # Fazendo decode do datagrama recebido
            npdata = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)
            cv2.imshow("Video no Cliente", frame)  # Display do video no cliente

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                message = mensagens.PARAR_STREAMING.encode("utf-8")  # Mensagem enviada ao servidor
                client_socket.sendto(message, (host_ip, UDP_PORT))
                global pararAudio
                pararAudio = True
                cv2.destroyAllWindows()
                break
        print("Encerrando transmissão de video")

    def receive_audio():
        print("Começando a receber audio")
        p = pyaudio.PyAudio()
        CHUNK = 10 * 1024
        stream = p.open(format=p.get_format_from_width(2),
                        channels=2,
                        rate=44100,
                        output=True,
                        frames_per_buffer=CHUNK)

        # create socket
        audio_socket.sendto(nomeVideo.encode("utf-8"), (host_ip, UDP_PORT - 1))

        def getAudioData():
            global pararAudio
            while True:
                frame, _ = audio_socket.recvfrom(BUFFER_SIZE)
                if frame == b'Stopped':
                    break
                queue_audio.put(frame)
            print("Encerrando aquisição de dados de audio")

        t3 = threading.Thread(target=getAudioData, args=())
        t3.start()
        time.sleep(0.1)
        print('Now Playing...')
        global pararAudio
        while not pararAudio:
            frame = queue_audio.get()
            stream.write(frame)
        audio_socket.sendto(b'Stop', (host_ip, UDP_PORT - 1))
        print("Encerrando transmissão de audio")

    t1 = threading.Thread(target=receive_audio, args=())
    t1.start()
    t2 = threading.Thread(target=receive_video, args=())
    t2.start()
    return True


def listarVideos():
    message = mensagens.LISTAR_VIDEOS.encode("utf-8")  # Mensagem enviada ao servidor
    client_socket.sendto(message, (host_ip, UDP_PORT))
    mensagem = client_socket.recv(BUFFER_SIZE)
    mensagem = mensagem.decode("utf-8")
    print(mensagem)
    lista_de_videos = client_socket.recv(BUFFER_SIZE)
    lista_de_videos = pickle.loads(lista_de_videos)
    print(lista_de_videos)
    return lista_de_videos


# Inicializações
host_ip = getIP()  # Pegar host_ip e host_name dinamicamente
host_name = getHostName()
BUFFER_SIZE = 65536
UDP_PORT = 6000

print("Host IP: ", host_ip)
print("Host Name: ", host_name)

# Socket para a conexão UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket UDP do cliente
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)

audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
audio_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)

# listarVideos()
# reproduzirVideo("interstellar_720p.mp4")
