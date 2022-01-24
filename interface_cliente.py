import socket
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mensagens
import cliente_udp

# Definição das constantes
LB_FONT = ('arial', 12, 'bold')
ENT_FONT = ('verdana', 10)
WINDOW_COLOR = '#1e3743'
BACKGROUND_COLOR = '#dfe3ee'
FOREGROUND_COLOR = 'black'
BT_BACKGROUND_COLOR = '#103d72'
BT_FOREGROUND_COLOR = 'white'
BT_BORDER = 3

# Variaveis globais
global usuario_logado
global tipo_usuario_logado

class JanelaLogin:
    def __init__(self, parent=None):
        # Fecha a janela anterior, se ela existir
        if parent:
            parent.root.destroy()
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
        self.lb_usuario.place(relx=0.345, rely=0.29)
        self.ent_usuario = Entry(self.root, font=ENT_FONT)
        self.ent_usuario.place(relx=0.455, rely=0.295)

        # Criação e posicionamento do label e radio buttons de tipo de usuário
        self.lb_tipo = Label(self.root, text="Tipo", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
        self.lb_tipo.place(relx=0.38, rely=0.42)
        self.tipo = StringVar()
        self.tipo.set("Premium")
        bt_tipo_1 = Radiobutton(self.root, text="Premium", variable=self.tipo, value="Premium",
                                bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
        bt_tipo_1.place(relx=0.45, rely=0.42)
        bt_tipo_2 = Radiobutton(self.root, text="Convidado", variable=self.tipo, value="Convidado",
                                bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
        bt_tipo_2.place(relx=0.45, rely=0.49)

        # Criação e posicionamento do label e entry do endereço IP (somente para a parte 2)
        # self.lb_end_ip = Label(self.root, text="Endereço IP", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
        # self.lb_end_ip.place(relx=0.33, rely=0.55)
        # self.ent_end_ip = Entry(self.root, font=ENT_FONT)
        # self.ent_end_ip.place(relx=0.48, rely=0.555)

        # Criação e posicionamento do botão que faz o login
        bt_entrar = Button(self.root, text="Entrar", font=LB_FONT, bd=BT_BORDER, command=self.bt_entrar_click,
                           bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
        bt_entrar.place(relx=0.425, rely=0.62, relwidth=0.15, relheight=0.08)

    # Função executada ao clicar no botão bt_entrar
    def bt_entrar_click(self):
        # Recupera os valores de entrada
        usuario = self.ent_usuario.get()
        tipo = self.tipo.get()

        #Setando usuario logado e tipo globalmente
        global usuario_logado 
        global tipo_usuario_logado

        usuario_logado = usuario
        tipo_usuario_logado = tipo

        end_ip = socket.gethostbyname(socket.gethostname())

        if not(usuario and tipo):
            # Mensagem de erro
            messagebox.showerror("ERRO", "Todas as entradas devem \nser preenchidas")
        else:
            resp = cliente_udp.entrarApp(usuario_logado, tipo_usuario_logado, end_ip)
            if resp[0] == mensagens.ENTRAR_NA_APP_ACK:
                messagebox.showinfo("Status", "Usuário criado com sucesso!")
            elif resp[0] == mensagens.STATUS_DO_USUARIO:
                messagebox.showinfo("Status", "ID: " + resp[1] + "\n" + "Tipo: " + resp[2])
                tipo_usuario_logado = resp[2]
            # Reseta os valores das entrys e radio buttons
            self.ent_usuario.delete(0, END)
            self.tipo.set("Premium")
            # self.ent_end_ip.delete(0, END)
            # Chama a janela de menu (passa a janela atual)
            JanelaMenu(self)

    # Fecha o programa
    def sair(self):
        # Fecha a janela atual
        self.root.destroy()


class JanelaMenu:
    def __init__(self, parent, grupo=False):
        # Fecha a janela anterior
        parent.root.destroy()
        # Cria a janela de menu
        self.root = Tk()

        self.grupo = grupo

        # Configurações básicas da janela
        self.root.title("Menu")
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
        if tipo_usuario_logado == "Premium":
            #Verifica se grupo ja existe (Verifica se o arquivo no nome do usuario premium logado existe)
            try:
                with open("./Grupos/" + usuario_logado + ".txt","r") as f:
                    self.grupo = True
                    f.close()
            except IOError:
                self.grupo = False

            # Criação e posicionamento do botão que cria um grupo (parte 2 do trabalho)
            if self.grupo:
                self.bt_grupo = Button(self.root, text="Ver grupo", font=LB_FONT, bd=BT_BORDER, 
                                    command=self.bt_grupo_click, bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
            else:
                self.bt_grupo = Button(self.root, text="Criar grupo", font=LB_FONT, bd=BT_BORDER, 
                                    command=self.bt_grupo_click, bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
            self.bt_grupo.place(relx=0.35, rely=0.25, relwidth=0.3, relheight=0.15)

        # Criação e posicionamento do botão que acessa o catálogo de vídeos
        self.bt_videos = Button(self.root, text="Catálogo de vídeos", font=LB_FONT, bd=BT_BORDER,
                                command=self.bt_videos_click,
                                bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)

        if tipo_usuario_logado == "Premium":                        
            self.bt_videos.place(relx=0.35, rely=0.6, relwidth=0.3, relheight=0.15)
        else:
            self.bt_videos.place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.15)

    # Função executada ao clicar no botão bt_grupo
    def bt_grupo_click(self):
        if not self.grupo:
            self.grupo = True
            self.bt_grupo.destroy()
            self.bt_grupo = Button(self.root, text="Ver grupo", font=LB_FONT, bd=BT_BORDER, 
                                   command=self.bt_grupo_click, bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
            self.bt_grupo.place(relx=0.35, rely=0.25, relwidth=0.3, relheight=0.15)
            arqGrupo = open("./Grupos/" + usuario_logado + ".txt","w")
            arqGrupo.write(usuario_logado)
            arqGrupo.write("\n")
            arqGrupo.close()
            print("GRUPO_CRIADO")
            #Para adicionar novos membros    
            #arqGrupo = open("./Grupos/" + usuario_logado + ".txt","a")
            #arqGrupo.write("abc")
            #arqGrupo.close()

        else:
            # Chama a janela de catálogo de vídeos (passa a janela atual)
            JanelaGrupo(self)

    # Função executada ao clicar no botão bt_videos
    def bt_videos_click(self):
        # Recupera a lista de vídeos
        lista_de_videos = cliente_udp.listarVideos()
        # Chama a janela de catálogo de vídeos (passa a janela atual e a lista de vídeos)
        JanelaVideos(self, lista_de_videos, self.grupo)

    # Volta para a janela de login
    def logout(self):
        # Chama a janela de login (passa a janela atual)
        JanelaLogin(self)

    # Fecha o programa
    def sair(self):
        # Fecha a janela atual
        self.root.destroy()


class JanelaGrupo:
    def __init__(self, parent):
        # Fecha a janela anterior
        parent.root.destroy()
        # Cria a janela de catálogo de vídeos
        self.root = Tk()

        # Configurações básicas da janela
        self.root.title("Grupo")
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
        # Código para recuperar o ID dos membros do grupo no servidor
        # 
        global usuario_logado
        arqGrupo = open("./Grupos/" + usuario_logado + ".txt")
        linhas = arqGrupo.readlines()
        arqGrupo.close()

        tamanhoArq = len(linhas)
        linhasPercorridas = 1
        self.membros = []

        for linha in linhas:
            linha_sem_barra_n = linha[0:len(linha)-1]

            self.membros.append(linha_sem_barra_n)
            linhasPercorridas += 1

        # lista exemplo de membros
        #self.membros = ["nome1", "nome2", "nome3", "nome4", "nome5",
        #                "nome6", "nome7", "nome8", "nome9", "nome10",
        #                "nome11", "nome12", "nome13", "nome14", "nome15"]

        # Criação e posicionamento da entry para adicionar um membro
        self.ent_adiciona = Entry(self.root, font=ENT_FONT)
        self.ent_adiciona.place(relx=0.25, rely=0.105, relwidth=0.22)
        # Criação e posicionamento do botão para adicionar um membro
        self.bt_adiciona = Button(self.root, text="Adicionar membro", font=LB_FONT, bd=BT_BORDER,
                                  command=self.bt_adiciona_click,
                                  bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
        self.bt_adiciona.place(relx=0.472, rely=0.1, relwidth=0.28, relheight=0.05)

        # Criação e posicionamento da lista de membros do grupo
        self.lista_membros = ttk.Treeview(self.root, column=("col0", "col1"))
        self.lista_membros.heading("#0", text="")
        self.lista_membros.heading("#1", text="Membros do grupo")
        self.lista_membros.column("#0", width=1)
        self.lista_membros.column("#1", width=500)
        self.lista_membros.place(relx=0.1, rely=0.23, relwidth=0.77, relheight=0.54)

        # Criação e posicionamento da barra de rolamento
        self.scroll_lista = Scrollbar(self.root, orient='vertical')
        self.scroll_lista.place(relx=0.87, rely=0.23, relheight=0.54)

        # Conecta a barra de rolamento com a lista de membros
        self.scroll_lista['command'] = self.lista_membros.yview
        self.lista_membros.configure(yscroll=self.scroll_lista.set)

        # Insere os membros do grupo na lista
        for membro in self.membros:
            self.lista_membros.insert("", END, values=membro)

        # Criação e posicionamento do botão para remover o membro selecionado
        self.bt_remove = Button(self.root, text="Remover membro", font=LB_FONT, bd=BT_BORDER,
                                command=self.bt_remove_click,
                                bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
        self.bt_remove.place(relx=0.35, rely=0.85, relwidth=0.3, relheight=0.05)

    # Função executada ao clicar no botão bt_adiciona
    def bt_adiciona_click(self):
        # Recupera o valor da entry para adicionar um membro
        nome = self.ent_adiciona.get()
        # Verifica se algo foi digitado na entry
        if nome:

            # Verifica se o usuário existe
            arqUsuario = open("Usuarios/usuarios.txt")
            linhas = arqUsuario.readlines()
            arqUsuario.close()

            userValido = False
            for linha in linhas:
                linha_sem_barra_n = linha[0:len(linha)-1]
                if linha_sem_barra_n.split(" ")[0] == nome:
                    userValido = True
                    break

            if userValido:
                # Verifica se o usuário já é um membro do grupo
                if nome not in self.membros:
                    # Reseta o conteúdo da entry
                    self.ent_adiciona.delete(0, END)

                    # 
                    # Código para adicionar o usuário no grupo no 
                    # servidor gerenciador de serviços
                    # 
                    arqGrupo = open("./Grupos/" + usuario_logado + ".txt","a")
                    arqGrupo.write(nome)
                    arqGrupo.write("\n")
                    arqGrupo.close()                
                    # Adiciona o nome do vídeo na lista de vídeos da interface
                    self.membros.append(nome)
                    # Chama a função que atualiza a lista de vídeos da interface
                    self.atualiza_lista()
                    print("MEMBRO_ADICIONADO")
                else:
                    # Mensagem de erro
                    messagebox.showinfo("MEMBRO NÃO ADICIONADO", "Já existe um membro com\neste nome no grupo")
            else:
                # Mensagem de erro
                messagebox.showerror("ERRO", "Não existe um usuário\ncom este nome")
        else:
            # Mensagem de erro
            messagebox.showerror("ERRO", "Digite o nome de usuário\nque você deseja adicionar")

    # Função executada ao clicar no botão bt_remove
    def bt_remove_click(self):
        # Recupera o membro selecionado
        selecionado = self.lista_membros.selection()
        # Verifica se somente um membro foi selecionado
        if len(selecionado) == 1:
            # Recupera o nome do membro selecionado
            membro = self.lista_membros.item(selecionado, 'values')[0]

            if membro != usuario_logado:
                # Remove o membro selecionado da lista de membros
                self.membros.remove(membro)
                # Chama a função que atualiza a lista de membros na interface
                self.atualiza_lista()

                #
                # Código que remove o membro do grupo no servidor
                #
                arqGrupo = open("./Grupos/" + usuario_logado + ".txt","w")

                for membro in self.membros:
                    arqGrupo.write(membro)
                    arqGrupo.write("\n")

                arqGrupo.close()
                print("MEMBRO_REMOVIDO")
            else:
                messagebox.showerror("ERRO", "Você não pode se remover")
        # Verifica se mais de um membro foi selecionado
        elif selecionado:
            # Mensagem de erro
            messagebox.showerror("ERRO", "Selecione somente um membro")
        # Verifica se nenhum membro foi selecionado
        else:
            # Mensagem de erro
            messagebox.showerror("ERRO", "Selecione o membro que\nvocê deseja remover")

    # Função que atualiza a lista de membros na interface
    def atualiza_lista(self):
        # Deleta as informações antigas
        self.lista_membros.delete(*self.lista_membros.get_children())
        # Insere as informações atualizadas
        for membro in self.membros:
            self.lista_membros.insert("", END, values=membro)

    # Volta para a janela de menu
    def voltar(self):
        # Chama a janela de menu (passa a janela atual)
        JanelaMenu(self, True)

    # Volta para a janela de login
    def logout(self):
        # Chama a janela de login (passa a janela atual)
        JanelaLogin(self)

    # Fecha o programa
    def sair(self):
        # Fecha a janela atual
        self.root.destroy()


class JanelaVideos:
    def __init__(self, parent, lista_de_videos, grupo):
        # Fecha a janela anterior
        parent.root.destroy()
        # Cria a janela de catálogo de vídeos
        self.root = Tk()

        self.lista_de_videos = lista_de_videos
        self.grupo = grupo

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
        # Criação e posicionamento da lista de vídeos disponíveis
        self.lista_videos = ttk.Treeview(self.root, column=("col0", "col1"))
        self.lista_videos.heading("#0", text="")
        self.lista_videos.heading("#1", text="Catálogo de vídeos")
        self.lista_videos.column("#0", width=1)
        self.lista_videos.column("#1", width=500)
        self.lista_videos.place(relx=0.06, rely=0.065, relwidth=0.85, relheight=0.435)

        # Criação e posicionamento da barra de rolamento
        self.scroll_lista = Scrollbar(self.root, orient='vertical')
        self.scroll_lista.place(relx=0.91, rely=0.065, relheight=0.385)

        # Conecta a barra de rolamento com a lista de vídeos
        self.scroll_lista['command'] = self.lista_videos.yview
        self.lista_videos.configure(yscroll=self.scroll_lista.set)

        # Insere os vídeos disponíveis no servidor na lista
        for video in self.lista_de_videos:
            self.lista_videos.insert("", END, values=video)

        # Criação e posicionamento do label e radio buttons de resolução so vídeo
        self.lb_resolucao = Label(self.root, text="Resolução:", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
        self.lb_resolucao.place(relx=0.26, rely=0.58)
        self.resolucao = StringVar()
        self.resolucao.set("240p")
        bt_resolucao_1 = Radiobutton(self.root, text="240p", variable=self.resolucao, value="240p",
                                bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
        bt_resolucao_1.place(relx=0.41, rely=0.58)
        if tipo_usuario_logado == "Premium":
            bt_resolucao_2 = Radiobutton(self.root, text="480p", variable=self.resolucao, value="480p",
                                    bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
            bt_resolucao_2.place(relx=0.53, rely=0.58)
            bt_resolucao_3 = Radiobutton(self.root, text="720p", variable=self.resolucao, value="720p",
                                    bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
            bt_resolucao_3.place(relx=0.65, rely=0.58)

        # Criação e posicionamento do label e radio buttons de tipo de streaming
        self.lb_streaming = Label(self.root, text="Streaming:", bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
        self.lb_streaming.place(relx=0.28, rely=0.7)
        self.streaming = StringVar()
        self.streaming.set("Individual")
        bt_streaming_1 = Radiobutton(self.root, text="Individual", variable=self.streaming, value="Individual",
                                bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
        bt_streaming_1.place(relx=0.43, rely=0.7)
        if tipo_usuario_logado == "Premium":
            bt_streaming_2 = Radiobutton(self.root, text="Grupo", variable=self.streaming, value="Grupo",
                                    bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, font=LB_FONT)
            bt_streaming_2.place(relx=0.6, rely=0.7)

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
        if len(selecionado) == 1:
            # Recupera o nome do arquivo do vídeo selecionado
            self.video = self.lista_videos.item(selecionado, 'values')[0]
            # Chama a função que pede o vídeo ao servidor
            self.assistir_video()
        # Verifica se mais de um vídeo foi selecionado
        elif selecionado:
            # Mensagem de erro
            messagebox.showerror("ERRO", "Selecione somente um vídeo")
        # Verifica se nenhum vídeo foi selecionado
        else:
            # Mensagem de erro
            messagebox.showerror("ERRO", "Selecione o vídeo que\nvocê deseja assistir")
    
    # Função que pede o vídeo ao servidor
    def assistir_video(self):
        # self.video = nome do arquivo do vídeo, self.resolucao.get() = resolução do vídeo, 
        # self.streaming.get() = tipo de streaming
        nome_arquivo_video = self.video + "_" + self.resolucao.get() + ".mp4"
        # Código para pedir o vídeo ao servidor
        cliente_udp.reproduzirVideo(nome_arquivo_video)

    # Volta para a janela de menu
    def voltar(self):
        # Chama a janela de menu (passa a janela atual)
        JanelaMenu(self, self.grupo)

    # Volta para a janela de login
    def logout(self):
        # Chama a janela de login (passa a janela atual)
        JanelaLogin(self)

    # Fecha o programa
    def sair(self):
        # Fecha a janela atual
        self.root.destroy()


if __name__ == "__main__":
    # Chama a janela de login
    JanelaLogin()
