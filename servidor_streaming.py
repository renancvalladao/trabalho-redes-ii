import socket
import threading
import time
import wave  # Manipular audio

import mensagens
from conectionThread import ConnectionThread


def getIP():
    return socket.gethostbyname(socket.gethostname())


def getHostName():
    return socket.gethostname()


# Inicializações
host_ip = getIP()  # Pegar host_ip e host_name dinamicamente
host_name = getHostName()
UDP_PORT = 6000
BUFFER_SIZE = 65536
print("Host IP: ", host_ip)
print("Host Name: ", host_name)

# Conexão UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket UDP do servidor
socket_address = (host_ip, UDP_PORT)
server_socket.bind(socket_address)  # Iniciando servidor no socket_address
print("(UDP) Ouvindo em: ", socket_address)
threads = {}


# Enviar audio
def audio_stream():
    audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    audio_socket.bind((host_ip, (UDP_PORT - 1)))
    CHUNK = 10 * 1024
    wf = wave.open("Audios/interstellar_720p.mp4.wav")
    print('server listening at', (host_ip, (UDP_PORT - 1)), wf.getframerate())
    sample_rate = wf.getframerate()
    while True:
        msg, client_addr = audio_socket.recvfrom(BUFFER_SIZE)
        print('GOT connection from ', client_addr, msg)

        while True:
            data = wf.readframes(CHUNK)
            audio_socket.sendto(data, client_addr)
            time.sleep(0.8 * CHUNK / sample_rate)


# Gerando multithreading
thread_audio = threading.Thread(target=audio_stream, args=())
thread_audio.start()

while True:
    print("Aguardando conexão...")
    mensagem, client = server_socket.recvfrom(BUFFER_SIZE)
    mensagem = mensagem.decode("utf-8")
    print(mensagem)
    if client not in threads:
        threads[client] = ConnectionThread(server_socket, client)
        threads[client].start()
    if mensagem.find(".mp4") != -1:
        threads[client].video = mensagem
    else:
        threads[client].mensagem = mensagem
    if mensagem == mensagens.PARAR_STREAMING:
        threads[client].stop = True
