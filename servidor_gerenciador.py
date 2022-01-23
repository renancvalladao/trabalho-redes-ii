import socket
import threading

import mensagens


def getIP():
    return socket.gethostbyname(socket.gethostname())


def getHostName():
    return socket.gethostname()


def entrarNaApp(mensagem):
    usuario = mensagem[1]
    tipo = mensagem[2]
    ip = mensagem[3]

    arqUsuario = open("Usuarios/usuarios.txt")

    linhas = arqUsuario.readlines()
    arqUsuario.close()

    userValido = False
    tamanhoArq = len(linhas)
    linhasPercorridas = 1

    id_usuario = -1
    print(linhas)

    for linha in linhas:
        linha_sem_barra_n = linha[0:len(linha)-1]

        print(linha_sem_barra_n.split(" ")[1], usuario)
        print(linha_sem_barra_n.split(" ")[1] == usuario)
        if linha_sem_barra_n.split(" ")[1] == usuario:
            id_usuario = linha_sem_barra_n.split(" ")[0]
            tipo = linha_sem_barra_n.split(" ")[2]
            userValido = True
            break
        linhasPercorridas += 1

    if not userValido:
        arqUsuario = open("Usuarios/usuarios.txt", "a")
        novoUsuario = str(tamanhoArq) + " " + usuario + " " + tipo + "\n"
        arqUsuario.write(novoUsuario)
        conn.sendall(mensagens.ENTRAR_NA_APP_ACK.encode("utf-8"))
    else:
        mensagem = mensagens.STATUS_DO_USUARIO + "," + str(id_usuario) + "," + tipo
        conn.sendall(mensagem.encode("utf-8"))



# Servidor Gerenciador na porta 5000
def conectado(conn, client):
    print('Conectado por ', client)
    data = conn.recv(1024)
    mensagem = (data.decode('utf-8').split(","))
    print(mensagem)
    if mensagem[0] == mensagens.ENTRAR_NA_APP:
        entrarNaApp(mensagem)


# Inicializações
host_ip = getIP()  # Pegar host_ip e host_name dinamicamente
host_name = getHostName()
TCP_PORT = 5000
print("Host IP: ", host_ip)
print("Host Name: ", host_name)

# Conexão TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket TCP do servidor
socket_address = (host_ip, TCP_PORT)
server_socket.bind(socket_address)
server_socket.listen()  # Iniciando servidor no socket_address
print("(TCP) Ouvindo em: ", socket_address)

while True:
    # Aceita entrada de cliente
    conn, addr = server_socket.accept()
    thread = threading.Thread(target=conectado, args=(conn, addr))
    thread.start()
