#global end_socket
'''
end_socket = []

class GuardaSocketCliente():

    def insere_socket(usuario,socket_video,socket_audio):
        #global end_socket
        end_socket.append([usuario,socket_video,socket_audio])
        print("Vendo lista")
        print(end_socket)

'''

porta = []

class GuardaSocketCliente():

    def insere_socket(usuario,porta_udp_video):
        porta.append([usuario,porta_udp_video])
        print("Vendo lista")
        print(porta)

    def get_porta():
        return porta



