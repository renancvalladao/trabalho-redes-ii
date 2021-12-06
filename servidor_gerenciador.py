import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

#Servidor Gerenciador na porta 5000
def conectado(conn, client):
    print('Conectado por ', client)

    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(data.decode('utf-8'))
            conn.sendall(b'Prazer, eu sou o servidor!')

if __name__ == '__main__':

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
        tcp.bind((HOST, PORT))
        tcp.listen()
        print('Server ready!')

        while True:
            #Aceita entrada de cliente
            conn, addr = tcp.accept()
            thread = threading.Thread(target=conectado, args=(conn, addr))
            thread.start()