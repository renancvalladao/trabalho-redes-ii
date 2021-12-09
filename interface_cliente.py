from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Definição das constantes
LB_FONT = ('arial', 12, 'bold')
ENT_FONT = ('verdana', 10)
WINDOW_COLOR = '#1e3743'
BACKGROUND_COLOR = '#dfe3ee'
FOREGROUND_COLOR = 'black'
BT_BACKGROUND_COLOR = '#103d72'
BT_FOREGROUND_COLOR = 'white'
BT_BORDER = 3


class JanelaLogin:
    def __init__(self):
        # Criação da janela de login
        self.root = Tk()

        # Configurações básicas da janela
        self.root.title("Login")
        self.root.configure(background=WINDOW_COLOR)
        self.root.geometry("700x550+280+50")
        self.root.maxsize(width=800, height=600)
        self.root.minsize(width=600, height=500)

        # Criação dos componentes da janela
        self.criar_menubar()
        self.criar_frames()
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
    def criar_frames(self):
        self.frame = Frame(self.root, bg=BACKGROUND_COLOR)
        self.frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    # Criação dos widgets
    def criar_widgets(self):
        # Criação e posicionamento do label e entry do nome de usuário
        self.lb_usuario = Label(self.root, text="Usuário", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
        self.lb_usuario.place(relx=0.35, rely=0.2)
        self.ent_usuario = Entry(self.root, font=ENT_FONT)
        self.ent_usuario.place(relx=0.45, rely=0.205)

        # Criação e posicionamento do label e radio buttons de tipo de usuário
        self.lb_tipo = Label(self.root, text="Tipo", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
        self.lb_tipo.place(relx=0.38, rely=0.35)
        self.tipo = StringVar()
        self.tipo.set("Premium")
        bt_tipo_1 = Radiobutton(self.root, text="Premium", variable=self.tipo, value="Premium",
                                bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
        bt_tipo_1.place(relx=0.45, rely=0.35)
        bt_tipo_2 = Radiobutton(self.root, text="Convidado", variable=self.tipo, value="Convidado",
                                bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
        bt_tipo_2.place(relx=0.45, rely=0.42)

        # Criação e posicionamento do label e entry do endereço IP
        self.lb_end_ip = Label(self.root, text="Endereço IP", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
        self.lb_end_ip.place(relx=0.33, rely=0.55)
        self.ent_end_ip = Entry(self.root, font=ENT_FONT)
        self.ent_end_ip.place(relx=0.48, rely=0.555)

        # Criação e posicionamento do botão que faz o login
        bt_entrar = Button(self.root, text="Entrar", font=LB_FONT, bd=BT_BORDER, command=self.bt_entrar_click,
                           bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
        bt_entrar.place(relx=0.44, rely=0.7, relwidth=0.15, relheight=0.08)

    # Função executada ao clicar no botão bt_entrar
    def bt_entrar_click(self):
        # Recupera os valores de entrada
        usuario = self.ent_usuario.get()
        tipo = self.tipo.get()
        end_ip = self.ent_end_ip.get()
        # Verifica se todos as entradas estão preenchidas
        if usuario and tipo and end_ip:
            # Reseta os valores das entrys e radio buttons
            self.ent_usuario.delete(0, END)
            self.tipo.set("Premium")
            self.ent_end_ip.delete(0, END)
            # Chama a janela de menu (passa a janela atual)
            JanelaMenu(self)
        else:
            # Mensagem de erro
            messagebox.showerror("ERRO", "Todas as entradas devem \nser preenchidas")

    # Fecha o programa
    def sair(self):
        # Fecha a janela atual
        self.root.destroy()


class JanelaMenu:
    def __init__(self, parent):
        # Cria a janela de menu
        self.root = Toplevel()
        # Define a janela pai
        self.parent = parent

        # Configurações básicas da janela
        self.root.title("Menu")
        self.root.configure(background=WINDOW_COLOR)
        self.root.geometry("700x550+280+50")
        self.root.maxsize(width=800, height=600)
        self.root.minsize(width=600, height=500)
        # Garante que a janela pai não possa ser
        # alcançada enquanto esta estiver aberta
        self.root.focus_force()
        self.root.grab_set()

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

        # Opção que volta para a janela de login
        opcoes.add_command(label="Logout", command=self.logout)
        # Opção que fecha o programa
        opcoes.add_command(label="Sair", command=self.sair)

    # Criação do frame
    def criar_frame(self):
        self.frame = Frame(self.root, bg=BACKGROUND_COLOR)
        self.frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    # Criação dos widgets
    def criar_widgets(self):
        # Criação e posicionamento do botão que cria um grupo (parte 2 do trabalho)
        self.bt_grupo = Button(self.root, text="Criar grupo", font=LB_FONT, bd=BT_BORDER, command=self.bt_grupo_click,
                               bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
        self.bt_grupo.place(relx=0.35, rely=0.25, relwidth=0.3, relheight=0.15)

        # Criação e posicionamento do botão que acessa o catálogo de vídeos
        self.bt_videos = Button(self.root, text="Catálogo de vídeos", font=LB_FONT, bd=BT_BORDER,
                                command=self.bt_videos_click,
                                bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
        self.bt_videos.place(relx=0.35, rely=0.6, relwidth=0.3, relheight=0.15)

    # Função executada ao clicar no botão bt_grupo
    def bt_grupo_click(self):
        # Somente para a parte 2 do trabalho
        pass

    # Função executada ao clicar no botão bt_videos
    def bt_videos_click(self):
        # Chama a janela de catálogo de vídeos (passa a janela atual e seu pai)
        JanelaVideos([self, self.parent])

    # Volta para a janela de login
    def logout(self):
        # Fecha a janela atual
        self.root.destroy()

    # Fecha o programa
    def sair(self):
        # Fecha a janela atual
        self.root.destroy()
        # Fecha a janela pai
        self.parent.root.destroy()


class JanelaVideos:
    def __init__(self, parents):
        # Cria a janela de catálogo de vídeos
        self.root = Toplevel()
        # Define uma lista das janela antecessoras
        self.parents = parents

        # Configurações básicas da janela
        self.root.title("Catálogo de vídeos")
        self.root.configure(background=WINDOW_COLOR)
        self.root.geometry("700x550+280+50")
        self.root.maxsize(width=800, height=600)
        self.root.minsize(width=600, height=500)
        # Garante que a janela pai não possa ser
        # alcançada enquanto esta estiver aberta
        self.root.focus_force()
        self.root.grab_set()

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

        # Opção que volta para a janela de menu
        opcoes.add_command(label="Voltar", command=self.voltar)
        # Opção que volta para a janela de login
        opcoes.add_command(label="Logout", command=self.logout)
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
        videos = ["video1.mp4", "video2.mp4", "video3.mp4", "video4.mp4", "video5.mp4",
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
        for video in videos:
            self.lista_videos.insert("", END, values=video)

        # Criação e posicionamento do botão para assistir o vídeo selecionado
        self.bt_assistir = Button(self.root, text="Assistir vídeo", font=LB_FONT, bd=BT_BORDER,
                                  command=self.bt_assistir_click,
                                  bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
        self.bt_assistir.place(relx=0.35, rely=0.85, relwidth=0.3, relheight=0.05)

    # Função executada ao clicar no botão bt_assistir
    def bt_assistir_click(self):
        # Recupera o vídeo selecionado
        selecionado = self.lista_videos.selection()
        # Verifica se algum vídeo foi selecionado
        if selecionado:
            # Recupera o nome do arquivo do vídeo selecionado
            self.video = self.lista_videos.item(selecionado, 'values')[0]

            # Cria uma janela para a escolha da resolução
            self.janela_resolucao = Toplevel()

            # Configurações básicas da janela
            self.janela_resolucao.title("Resolução")
            self.janela_resolucao.configure(background='#151515')
            self.janela_resolucao.geometry("350x275+520+175")
            # Impede que a janela seja redimensionada
            self.janela_resolucao.resizable(False, False)
            # Garante que a janela pai não possa ser
            # alcançada enquanto esta estiver aberta
            self.janela_resolucao.focus_force()
            self.janela_resolucao.grab_set()

            # Criação e posicionamento do botão que define resolução como 240p
            self.bt_res_240 = Button(self.janela_resolucao, text="240p", font=LB_FONT, bd=BT_BORDER,
                                     command=self.bt_res_240_click,
                                     bg='gray35', fg=BT_FOREGROUND_COLOR)
            self.bt_res_240.place(relx=0.35, rely=0.18, relwidth=0.3, relheight=0.15)

            # Criação e posicionamento do botão que define resolução como 480p
            self.bt_res_480 = Button(self.janela_resolucao, text="480p", font=LB_FONT, bd=BT_BORDER,
                                     command=self.bt_res_480_click,
                                     bg='gray35', fg=BT_FOREGROUND_COLOR)
            self.bt_res_480.place(relx=0.35, rely=0.43, relwidth=0.3, relheight=0.15)

            # Criação e posicionamento do botão que define resolução como 720p
            self.bt_res_720 = Button(self.janela_resolucao, text="720p", font=LB_FONT, bd=BT_BORDER,
                                     command=self.bt_res_720_click,
                                     bg='gray35', fg=BT_FOREGROUND_COLOR)
            self.bt_res_720.place(relx=0.35, rely=0.68, relwidth=0.3, relheight=0.15)

            # Criação do loop da janela
            self.janela_resolucao.mainloop()

    # Função executada ao clicar no botão bt_res_240
    def bt_res_240_click(self):
        # Define resolução do vídeo
        self.resolucao = "240"
        # Fecha a janela de resolução
        self.janela_resolucao.destroy()
        # Chama a função que pede o vídeo ao servidor
        self.assistir_video()

    # Função executada ao clicar no botão bt_res_480
    def bt_res_480_click(self):
        # Define resolução do vídeo
        self.resolucao = "480"
        # Fecha a janela de resolução
        self.janela_resolucao.destroy()
        # Chama a função que pede o vídeo ao servidor
        self.assistir_video()

    # Função executada ao clicar no botão bt_res_720
    def bt_res_720_click(self):
        # Define resolução do vídeo
        self.resolucao = "720"
        # Fecha a janela de resolução
        self.janela_resolucao.destroy()
        # Chama a função que pede o vídeo ao servidor
        self.assistir_video()

    # Função que pede o vídeo ao servidor
    def assistir_video(self):
        pass
        # self.video = nome do arquivo do vídeo, self.resolucao = resolução do vídeo

        # 
        # Código para pedir o vídeo ao servidor
        # 

    # Volta para a janela de menu
    def voltar(self):
        # Fecha a janela atual
        self.root.destroy()

    # Volta para a janela de login
    def logout(self):
        # Fecha a janela atual
        self.root.destroy()
        # Fecha a janela pai (janela de menu)
        self.parents[0].root.destroy()

    # Fecha o programa
    def sair(self):
        # Fecha a janela atual
        self.root.destroy()
        # Fecha as janelas antecessoras
        for parent in self.parents:
            parent.root.destroy()


if __name__ == "__main__":
    # Chama a janela de login
    JanelaLogin()
