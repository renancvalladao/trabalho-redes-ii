import base64  # Converte dados de imagem em formato texto
import pickle
import queue
import socket
import threading
import time

import cv2
import numpy as np
import pyaudio

import mensagens
import json

from guardaSocketCliente import GuardaSocketCliente

pararAudio = False
reproduzindoVideo = False
users_grupo = []

def getIP():
    return socket.gethostbyname(socket.gethostname())


def getHostName():
    return socket.gethostname()


def reproduzirVideoGrupo(nomeVideo, usuario, flagGrupo):
    if flagGrupo == "Individual":
        message = mensagens.RETORNA_SOCKET.encode("utf-8")  # Mensagem enviada ao servidor
        client_socket_udp.sendto(message, (host_ip, UDP_PORT))
        reproduzirVideo(nomeVideo, usuario,client_socket_udp,audio_socket)
    elif flagGrupo == "Grupo":
        
        message = mensagens.RETORNA_SOCKET.encode("utf-8")  # Mensagem enviada ao servidor
        client_socket_udp.sendto(message, (host_ip, UDP_PORT))
    
        '''
        #Verificar membros do grupo
        arqGrupo = open("./Grupos/" + usuario + ".txt")
        linhas = arqGrupo.readlines()
        arqGrupo.close()

        membros = []

        for linha in linhas:
            linha_sem_barra_n = linha[0:len(linha) - 1]
            membros.append(linha_sem_barra_n)

        tamanhoGrupo = len(membros)
        '''
        reproduzirVideo(nomeVideo, usuario,client_socket_udp,audio_socket)

def reproduzirVideo(nomeVideo, usuario,client_socket_udp_parm,audio_socket_parm):

    global pararAudio
    pararAudio = False
    message = mensagens.REPRODUZIR_VIDEO.encode("utf-8")  # Mensagem enviada ao servidor
    client_socket_udp_parm.sendto(message, (host_ip, UDP_PORT))
    mensagem = nomeVideo + "," + usuario
    client_socket_udp_parm.sendto(mensagem.encode("utf-8"), (host_ip, UDP_PORT))
    queue_audio = queue.Queue(maxsize=2000)

    video_mensagem = client_socket_udp_parm.recv(BUFFER_SIZE)
    video_mensagem = video_mensagem.decode("utf-8")
    print(video_mensagem)

    def receive_video():
        global reproduzindoVideo
        reproduzindoVideo = True
        cv2.namedWindow("Video no Cliente")
        cv2.moveWindow("Video no Cliente", 10, 360)

        # Receber datagrama de dados do servidor, no lado do cliente
        while True:
            packet, _ = client_socket_udp_parm.recvfrom(BUFFER_SIZE)
            data = base64.b64decode(packet, ' /')  # Fazendo decode do datagrama recebido
            npdata = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)
            cv2.imshow("Video no Cliente", frame)  # Display do video no cliente

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or not reproduzindoVideo:
                reproduzindoVideo = False
                message = mensagens.PARAR_STREAMING.encode("utf-8")  # Mensagem enviada ao servidor
                client_socket_udp_parm.sendto(message, (host_ip, UDP_PORT))
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
        audio_socket_parm.sendto(nomeVideo.encode("utf-8"), (host_ip, UDP_PORT - 1))

        def getAudioData():
            global pararAudio
            while True:
                frame, _ = audio_socket_parm.recvfrom(BUFFER_SIZE)
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
        audio_socket_parm.sendto(b'Stop', (host_ip, UDP_PORT - 1))
        print("Encerrando transmissão de audio")

    t1 = threading.Thread(target=receive_audio, args=())
    t1.start()
    t2 = threading.Thread(target=receive_video, args=())
    t2.start()


def listarVideos():
    message = mensagens.LISTAR_VIDEOS.encode("utf-8")  # Mensagem enviada ao servidor
    client_socket_udp.sendto(message, (host_ip, UDP_PORT))
    mensagem = client_socket_udp.recv(BUFFER_SIZE)
    mensagem = mensagem.decode("utf-8")
    print(mensagem)
    lista_de_videos = client_socket_udp.recv(BUFFER_SIZE)
    lista_de_videos = pickle.loads(lista_de_videos)
    print(lista_de_videos)
    return lista_de_videos


def entrarApp(usuario, tipo, ip):

    message = mensagens.GUARDA_SOCKET.encode("utf-8")  # Mensagem enviada ao servidor
    client_socket_udp.sendto(message, (host_ip, UDP_PORT))
    message = usuario.encode("utf-8")
    client_socket_udp.sendto(message, (host_ip, UDP_PORT))

    #EntrarApp
    mensagem = mensagens.ENTRAR_NA_APP + "," + usuario + "," + tipo + "," + ip
    client_socket_tcp.sendall(mensagem.encode("utf-8"))
    data = client_socket_tcp.recv(1024)
    resp = data.decode('utf-8').split(",")
    print(resp)
    return resp


def sairApp(usuario):
    mensagem = mensagens.SAIR_DA_APP + "," + usuario
    client_socket_tcp.sendall(mensagem.encode("utf-8"))
    data = client_socket_tcp.recv(1024)
    resp = data.decode('utf-8')
    print(resp)
    global reproduzindoVideo
    reproduzindoVideo = False
    return resp


def criarGrupo(usuario):
    mensagem = mensagens.CRIAR_GRUPO + "," + usuario
    client_socket_tcp.sendall(mensagem.encode("utf-8"))
    data = client_socket_tcp.recv(1024)
    resp = data.decode('utf-8').split(",")
    print(resp)
    return resp


def verGrupo(usuario):
    mensagem = mensagens.VER_GRUPO + "," + usuario
    client_socket_tcp.sendall(mensagem.encode("utf-8"))
    data = client_socket_tcp.recv(1024)
    resp = data.decode('utf-8').split(",")
    print(resp)
    return resp


def addUsuario(grupo, usuario):
    mensagem = mensagens.ADD_USUARIO_GRUPO + "," + grupo + "," + usuario
    client_socket_tcp.sendall(mensagem.encode("utf-8"))
    data = client_socket_tcp.recv(1024)
    resp = data.decode('utf-8')
    print(resp)
    return resp


def removerUsuario(grupo, novosMembros):
    mensagem = mensagens.REMOVER_USUARIO_GRUPO + "," + grupo + "," + " ".join(novosMembros)
    client_socket_tcp.sendall(mensagem.encode("utf-8"))
    data = client_socket_tcp.recv(1024)
    resp = data.decode('utf-8')
    print(resp)
    return resp



# Inicializações
host_ip = getIP()  # Pegar host_ip e host_name dinamicamente
host_name = getHostName()
BUFFER_SIZE = 65536
UDP_PORT = 6000
TCP_PORT = 5000

print("Host IP: ", host_ip)
print("Host Name: ", host_name)

# Socket para a conexão UDP
client_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket UDP do cliente
client_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)

# Conexão TCP
client_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket TCP do cliente
client_socket_tcp.connect((host_ip, TCP_PORT))

#Conexão UDP áudio
audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
audio_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)

# listarVideos()
# reproduzirVideo("interstellar_720p.mp4")
