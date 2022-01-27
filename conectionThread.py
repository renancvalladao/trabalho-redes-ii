import base64
import os
import pickle
import queue
import socket
import threading
import time
import json
import time

import cv2
import imutils

import mensagens


class ConnectionThread(threading.Thread):

    def __init__(self, server_socket, client, *args, **kwargs):
        super(ConnectionThread, self).__init__(*args, **kwargs)
        self.video = ''
        self.mensagem = ''
        self.usuario = ''
        self.stop = False
        self.finish = False
        self.client = client
        self.server_socket = server_socket
        # Conexão TCP
        socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket TCP do cliente
        socket_tcp.connect((socket.gethostbyname(socket.gethostname()), 5000))
        self.socket_tcp = socket_tcp

    def run(self):
        while not self.finish:
            if self.mensagem == mensagens.LISTAR_VIDEOS:
                self.listarVideos()
                self.mensagem = ''
            elif self.mensagem == mensagens.REPRODUZIR_VIDEO and self.video != '':
                self.getUserInformation()
                self.reproduzirVideoThread()
                self.mensagem = ''
                self.video = ''
                self.stop = False

    def getUserInformation(self):
        mensagem = mensagens.GET_USER_INFORMATION + "," + self.usuario
        self.socket_tcp.sendall(mensagem.encode("utf-8"))
        data = self.socket_tcp.recv(1024)
        resp = data.decode('utf-8').split(",")
        print(resp)

    def listarVideos(self):
        self.server_socket.sendto(mensagens.LISTA_DE_VIDEOS.encode("utf-8"), self.client)
        lista_de_videos_total = next(os.walk("Videos"), (None, None, []))[2]
        lista_de_videos_total = list(map(lambda video: video[0:(len(video) - 9)], lista_de_videos_total))
        lista_de_videos = set()
        lista_de_videos.update(lista_de_videos_total)
        self.server_socket.sendto(pickle.dumps(lista_de_videos), self.client)

    def reproduzirVideoThread(self):
        with open('./InternalUserInfo/informacao_porta.json', 'r') as openfile: 
            json_object = json.load(openfile) 

        tam = len(json_object)
        i = 0
        porta = []
        print("tam=",tam)
        while(i < tam):
            porta.append(json_object[i][1])
            i += 1
        print(porta)
        
        if tam == 1:
            self.reproduzirVideo(0)
        else:
            i = 0
            while(i < tam):
                print("Passando no while")
                print("i=",i)
                print("tam=",tam)
                print(porta[i])
                t1 = threading.Thread(target=self.reproduzirVideo(porta[i]), args=())
                t1.start()
                print("depois threading")
                i += 2

    def reproduzirVideo(self,porta):
        nomeVideo = self.video[0:(len(self.video) - 9)]
        resolucao = self.video[(len(self.video) - 8):(len(self.video) - 4)]
        mensagem_video = "REPRODUZINDO O VÍDEO " + nomeVideo + ", COM RESOLUÇÃO " + resolucao
        if porta != 0:
            #self.server_socket.sendto(mensagem_video.encode("utf-8"), (str(self.client[0]), int(porta)))
            self.server_socket.sendto(mensagem_video.encode("utf-8"), self.client)
        else:
            self.server_socket.sendto(mensagem_video.encode("utf-8"), self.client)
        print("VEEEER AQUI ")
        print(mensagem_video)
        print(self.client[0])
        print(self.client[1])
        print(porta)
        #if porta != 0:
        #    self.client[1] = porta
            
        # Fila 'q' dos frames
        q = queue.Queue(maxsize=10)

        # Tratando Vídeo
        video = cv2.VideoCapture("./Videos/" + self.video)  # Captura do vídeo
        FPS = video.get(cv2.CAP_PROP_FPS)  # Pegando FPS do video original

        WIDTH = 400  # Caber em um único datagrama

        TS = (0.5 / FPS)
        fps, st, frames_to_count, cnt = (0, 0, 1, 0)
        time.sleep(0.8)  # Sleep para equiparar ao sleep do Audio
        while not self.stop:
            try:
                _, frame = video.read()
                frame = imutils.resize(frame, width=WIDTH)
                q.put(frame)  # Frames na queue
            except:
                os._exit(1)  # fecha transmissao
            frame = q.get()  # pega frame da fila
            encoded, buffer = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY,
                                                            80])  # Colocar/Encode a imagem em JPEG com qualidade de 80% após o resize
            message = base64.b64encode(buffer)  # Converter dado binário em texto e vice versa com base64
            if porta != 0:
                #self.server_socket.sendto(message, (str(self.client[0]), int(porta)))  # Envio da mensagem ao cliente (do frame)
                self.server_socket.sendto(message, self.client)  # Envio da mensagem ao cliente (do frame)
            else:
                self.server_socket.sendto(message, self.client)  # Envio da mensagem ao cliente (do frame)

            # Controle de frames ao enviar a 'message'
            if cnt == frames_to_count:
                try:
                    fps = (frames_to_count / (time.time() - st))
                    st = time.time()
                    cnt = 0
                    if fps > FPS:
                        TS += 0.001
                    elif fps < FPS:
                        TS -= 0.001
                    else:
                        pass
                except:
                    pass
            cnt += 1
            # cv2.imshow('Video Servidor', frame) mostra o vídeo no servidor (não necessário)
            key = cv2.waitKey(int(1000 * TS)) & 0xFF
            if key == ord('q'):
                break
        cv2.destroyAllWindows()
        video.release()
