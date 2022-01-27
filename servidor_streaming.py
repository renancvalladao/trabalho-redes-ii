import socket
import threading

import mensagens
from audioThread import AudioThread
from conectionThread import ConnectionThread
from guardaSocketCliente import GuardaSocketCliente
import json


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

audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
audio_socket.bind((host_ip, (UDP_PORT - 1)))


def recebe_audio_cliente(msg,client_addr,audio_threads):
        print("Entrei recebe audio")
        print("Client audio:",client_addr)
        if msg == b'Stop':
            audio_threads[client_addr].stop = True
        else:
            audio_threads[client_addr] = AudioThread(audio_socket, client_addr, msg.decode("utf-8"))
            audio_threads[client_addr].start()


def recebe_video_cliente(mensagem,client):
    mensagem = mensagem.decode("utf-8")
    
    if mensagem == mensagens.GUARDA_SOCKET:
        mensagem, client = server_socket.recvfrom(BUFFER_SIZE)
        mensagem = mensagem.decode("utf-8")
        print("Client video:",mensagem)
        print("Client video:",client)
        GuardaSocketCliente.insere_socket(mensagem,client[1])

    if mensagem == mensagens.RETORNA_SOCKET:
        users_list = []
        users_list = GuardaSocketCliente.get_porta()
        print("Lista dos users")
        print(users_list)

        with open('./InternalUserInfo/informacao_porta.json', 'w') as f:
            json.dump(users_list, f)


    if client not in threads:
        threads[client] = ConnectionThread(server_socket, client)
        threads[client].start()
    if mensagem.find(".mp4") != -1:
        data = mensagem.split(",")
        threads[client].video = data[0]
        threads[client].usuario = data[1]
    else:
        threads[client].mensagem = mensagem
    if mensagem == mensagens.PARAR_STREAMING:
        threads[client].stop = True


# Enviar audio
def audio_stream():
    audio_threads = {}
    print('(UDP) Ouvindo conexões de audio em:', (host_ip, (UDP_PORT - 1)))
    while True:
        print("Esperando conexao de audio...")
        msg, client_addr = audio_socket.recvfrom(BUFFER_SIZE)
        print('Conexão de audio recebida de ', client_addr, msg)
        thread_audio_cliente = threading.Thread(target=recebe_audio_cliente(msg,client_addr,audio_threads), args=())
        thread_audio_cliente.start()



#Inicia server
def inicia_server():
    while True:
        print("Aguardando conexão...")
        mensagem, client = server_socket.recvfrom(BUFFER_SIZE)
        thread_video_cliente = threading.Thread(target=recebe_video_cliente(mensagem,client), args=())
        thread_video_cliente.start()


# Gerando multithreading
thread_audio = threading.Thread(target=audio_stream, args=())
thread_audio.start()

thread_server = threading.Thread(target=inicia_server, args=())
thread_server.start()


