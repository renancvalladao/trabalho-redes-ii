from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import servidor_streaming

# Definição das constantes
BT_FONT = ('arial', 12, 'bold')
WINDOW_COLOR = '#1e3743'
BACKGROUND_COLOR = '#dfe3ee'
BT_BACKGROUND_COLOR = '#103d72'
BT_FOREGROUND_COLOR = 'white'
BT_BORDER = 3


class InterfaceServidor:
    def __init__(self):
        # Cria a janela de catálogo de vídeos
        self.root = Tk()

        # Configurações básicas da janela
        self.root.title("Catálogo de vídeos")
        self.root.configure(background=WINDOW_COLOR)
        self.root.geometry("700x550+280+50")
        self.root.maxsize(width=800, height=600)
        self.root.minsize(width=600, height=500)

        # Criação dos componentes da janela
        self.criar_menubar()
        self.criar_frame()
        self.criar_widgets()

        # Define uma função a ser executada ao fechar a janela
        self.root.protocol("WM_DELETE_WINDOW", self.sair)
        # Criação do loop da janela
        self.root.mainloop()

    # Criação da barra de menu
    def criar_menubar(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        opcoes = Menu(menubar)

        menubar.add_cascade(label="Opções", menu=opcoes)

        # Opção que fecha o programa
        opcoes.add_command(label="Sair", command=self.sair)

    # Criação do frame
    def criar_frame(self):
        self.frame = Frame(self.root, bg=BACKGROUND_COLOR)
        self.frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    # Criação dos widgets
    def criar_widgets(self):
        # 
        # Código para recuperar a lista de vídeos disponíveis no servidor
        # 

        # lista exemplo de vídeos
        self.videos = ["video1.mp4", "video2.mp4", "video3.mp4", "video4.mp4", "video5.mp4",
                       "video6.mp4", "video7.mp4", "video8.mp4", "video9.mp4", "video10.mp4",
                       "video11.mp4", "video12.mp4", "video13.mp4", "video14.mp4", "video15.mp4",
                       "video16.mp4", "video17.mp4", "video18.mp4", "video19.mp4", "video20.mp4",
                       "video21.mp4", "video22.mp4", "video23.mp4", "video24.mp4", "video25.mp4", ]

        # Criação e posicionamento da lista de vídeos disponíveis
        self.lista_videos = ttk.Treeview(self.root, column=("col0", "col1"))
        self.lista_videos.heading("#0", text="")
        self.lista_videos.heading("#1", text="Catálogo de vídeos")
        self.lista_videos.column("#0", width=1)
        self.lista_videos.column("#1", width=500)
        self.lista_videos.place(relx=0.06, rely=0.065, relwidth=0.85, relheight=0.75)

        # Criação e posicionamento da barra de rolamento
        self.scroll_lista = Scrollbar(self.root, orient='vertical')
        self.scroll_lista.place(relx=0.91, rely=0.065, relheight=0.75)

        # Conecta a barra de rolamento com a lista de vídeos
        self.scroll_lista['command'] = self.lista_videos.yview
        self.lista_videos.configure(yscroll=self.scroll_lista.set)

        # Insere os vídeos disponíveis no servidor na lista
        for video in self.videos:
            self.lista_videos.insert("", END, values=video)

        # Criação e posicionamento do botão para assistir o vídeo selecionado
        self.bt_adiciona = Button(self.root, text="Adiciona vídeo", font=BT_FONT, bd=BT_BORDER,
                                  command=self.bt_adiciona_click,
                                  bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
        self.bt_adiciona.place(relx=0.15, rely=0.85, relwidth=0.3, relheight=0.05)

        self.bt_remove = Button(self.root, text="Remove vídeo", font=BT_FONT, bd=BT_BORDER,
                                command=self.bt_remove_click,
                                bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
        self.bt_remove.place(relx=0.55, rely=0.85, relwidth=0.3, relheight=0.05)

    # Função executada ao clicar no botão bt_adiciona
    def bt_adiciona_click(self):
        # Abre a pasta (Videos) onde estão os arquivos mp4 e
        # recupera o caminho absoluto do arquivo escolhido
        self.arq_nome = filedialog.askopenfilename(initialdir="./Videos", title="Selecione um arquivo",
                                                   filetypes=(("mp4 files", "*.mp4"), ("all files", "*.*")))

        # Verifica se algum arquivo foi escolhido
        if self.arq_nome:
            # Recupera o nome do arquivo de vídeo escolhido
            self.video = self.arq_nome.split('/')[-1]

            # Verifica se o vídeo não está na lista
            if self.video not in self.videos:
                # Adiciona o nome do vídeo na lista de vídeos da interface
                self.videos.append(self.video)
                # Chama a função que atualiza a lista de vídeos da interface
                self.atualiza_lista()

                # 
                # Código que adiciona o nome do vídeo escolhido
                # na lista de vídeos do servidor
                # 

            else:
                # Mensagem de erro
                messagebox.showinfo("VIDEO NÃO ADICIONADO", "Já existe um vídeo com \neste nome no servidor")

    # Função executada ao clicar no botão bt_remove
    def bt_remove_click(self):
        # Recupera o vídeo selecionado
        selecionado = self.lista_videos.selection()
        # Verifica se somente um vídeo foi selecionado
        if len(selecionado) == 1:
            # Recupera o nome do arquivo do vídeo selecionado
            self.video = self.lista_videos.item(selecionado, 'values')[0]

            # Remove o vídeo selecionado da lista de vídeos da interface
            self.videos.remove(self.video)
            # Chama a função que atualiza a lista de vídeos da interface
            self.atualiza_lista()

            # 
            # Código que remove o vídeo selecionado
            # da lista de vídeos do servidor
            # 

        # Verifica se mais de um vídeo foi selecionado
        elif selecionado:
            # Mensagem de erro
            messagebox.showerror("ERRO", "Selecione somente um vídeo")

    # Função que atualiza a lista de vídeos da interface
    def atualiza_lista(self):
        # Deleta as informações antigas
        self.lista_videos.delete(*self.lista_videos.get_children())
        # Insere as informações atualizadas
        for video in self.videos:
            self.lista_videos.insert("", END, values=video)

    # Fecha o programa
    def sair(self):
        # Fecha a janela atual
        self.root.destroy()


if __name__ == "__main__":
    # Chama a janela de login
    InterfaceServidor()
