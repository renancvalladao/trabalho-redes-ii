import os
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

    for linha in linhas:
        linha_sem_barra_n = linha[0:len(linha) - 1]

        if linha_sem_barra_n.split(" ")[0] == usuario:
            tipo = linha_sem_barra_n.split(" ")[1]
            userValido = True
            break

    if not userValido:
        arqUsuario = open("Usuarios/usuarios.txt", "a")
        novoUsuario = usuario + " " + tipo + "\n"
        arqUsuario.write(novoUsuario)
        conn.sendall(mensagens.ENTRAR_NA_APP_ACK.encode("utf-8"))
    else:
        mensagem = mensagens.STATUS_DO_USUARIO + "," + usuario + "," + tipo
        conn.sendall(mensagem.encode("utf-8"))


def verGrupo(usuario):
    arqGrupo = open("./Grupos/" + usuario + ".txt")
    linhas = arqGrupo.readlines()
    arqGrupo.close()

    membros = ""

    for linha in linhas:
        linha_sem_barra_n = linha[0:len(linha) - 1]

        membros += linha_sem_barra_n + " "

    mensagem = mensagens.GRUPO_DE_STREAMING + "," + membros[0:-1]
    conn.sendall(mensagem.encode("utf-8"))


def criarGrupo(usuario):
    arqGrupo = open("./Grupos/" + usuario + ".txt", "w")
    arqGrupo.write(usuario)
    arqGrupo.write("\n")
    arqGrupo.close()
    mensagem = mensagens.CRIAR_GRUPO_ACK
    conn.sendall(mensagem.encode("utf-8"))


def addUsuario(mensagem):
    # Leitura do arquivo usuarios.txt
    arqUsuario = open("Usuarios/usuarios.txt", "r")
    linhas = arqUsuario.readlines()
    arqUsuario.close()

    userValido = False
    for linha in linhas:
        linha_sem_barra_n = linha[0:len(linha) - 1]
        if linha_sem_barra_n.split(" ")[0] == mensagem[2]:
            userValido = True
            break
        
    # Verifica se o usuário existe
    if userValido:
        arqGrupo = open("./Grupos/" + mensagem[1] + ".txt", "a")
        arqGrupo.write(mensagem[2])
        arqGrupo.write("\n")
        arqGrupo.close()
        mensagem = mensagens.ADD_USUARIO_GRUPO_ACK
    else:
        mensagem = mensagens.ADD_USUARIO_GRUPO_NACK
    conn.sendall(mensagem.encode("utf-8"))


def removerUsuario(mensagem):
    membros = mensagem[2].split(" ")
    arqGrupo = open("./Grupos/" + mensagem[1] + ".txt","w")
    for membro in membros:
        arqGrupo.write(membro)
        arqGrupo.write("\n")
    arqGrupo.close()
    mensagem = mensagens.REMOVER_USUARIO_GRUPO_ACK
    conn.sendall(mensagem.encode("utf-8"))


def sairDaApp(usuario):
    if os.path.exists("./Grupos/" + usuario + ".txt"):
        os.remove("./Grupos/" + usuario + ".txt")

    arqUsuario = open("Usuarios/usuarios.txt")
    usuarios = []

    linhas = arqUsuario.readlines()
    arqUsuario.close()

    for linha in linhas:
        linha_sem_barra_n = linha[0:len(linha) - 1]

        if not linha_sem_barra_n.split(" ")[0] == usuario:
            usuarios.append(linha_sem_barra_n)

    arqUsuario = open("Usuarios/usuarios.txt", "w")
    for usuario in usuarios:
        arqUsuario.write(usuario + "\n")
    arqUsuario.close()
    mensagem = mensagens.SAIR_DA_APP_ACK
    conn.sendall(mensagem.encode("utf-8"))


def getUserInformation(usuario):
    arqUsuario = open("Usuarios/usuarios.txt")

    linhas = arqUsuario.readlines()
    arqUsuario.close()
    usuario_info = ""

    for linha in linhas:
        linha_sem_barra_n = linha[0:len(linha) - 1]

        if linha_sem_barra_n.split(" ")[0] == usuario:
            usuario_info = linha_sem_barra_n
            break
    mensagem = mensagens.USER_INFORMATION + "," + usuario_info
    conn.sendall(mensagem.encode("utf-8"))


# Servidor Gerenciador na porta 5000
def conectado(conn, client):
    print('Conectado por ', client)
    while True:
        data = conn.recv(1024)
        if not data:
            break
        mensagem = (data.decode('utf-8').split(","))
        print(mensagem)
        if mensagem[0] == mensagens.ENTRAR_NA_APP:
            entrarNaApp(mensagem)
        elif mensagem[0] == mensagens.VER_GRUPO:
            verGrupo(mensagem[1])
        elif mensagem[0] == mensagens.CRIAR_GRUPO:
            criarGrupo(mensagem[1])
        elif mensagem[0] == mensagens.ADD_USUARIO_GRUPO:
            addUsuario(mensagem)
        elif mensagem[0] == mensagens.REMOVER_USUARIO_GRUPO:
            removerUsuario(mensagem)
        elif mensagem[0] == mensagens.SAIR_DA_APP:
            sairDaApp(mensagem[1])
        elif mensagem[0] == mensagens.GET_USER_INFORMATION:
            getUserInformation(mensagem[1])


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
    print("Aguardando conexao...")
    conn, addr = server_socket.accept()
    thread = threading.Thread(target=conectado, args=(conn, addr))
    thread.start()
