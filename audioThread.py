import os
import threading
import time
import wave

CHUNK = 10 * 1024


class AudioThread(threading.Thread):

    def __init__(self, audio_socket, client, video, *args, **kwargs):
        super(AudioThread, self).__init__(*args, **kwargs)
        self.video = video
        self.stop = False
        self.client = client
        self.audio_socket = audio_socket

    def run(self):
        # Gerar arquivo de áudio .wav
        command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {} -y".format("./Videos/" + self.video,
                                                                           "./Audios/" + self.video + ".wav")
        os.system(command)  # Executa comando ffmpeg
        wf = wave.open("Audios/" + self.video + ".wav")
        sample_rate = wf.getframerate()
        while not self.stop:
            data = wf.readframes(CHUNK)
            self.audio_socket.sendto(data, self.client)
            time.sleep(0.8 * CHUNK / sample_rate)
        self.audio_socket.sendto(b'Stopped', self.client)
