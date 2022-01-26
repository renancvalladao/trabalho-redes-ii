import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Definição das constantes
LB_FONT = ('arial', 12, 'bold')
ENT_FONT = ('verdana', 10)
WINDOW_COLOR = '#1e3743'
BACKGROUND_COLOR = '#dfe3ee'
FOREGROUND_COLOR = 'black'
BT_BACKGROUND_COLOR = '#103d72'
BT_FOREGROUND_COLOR = 'white'
BT_BORDER = 3


class JanelaMenu:
    def __init__(self, parent=None):
        # Fecha a janela anterior, se ela existir
        if parent:
            parent.root.destroy()
        # Criação da janela de menu
        self.root = Tk()

        # Configurações básicas da janela
        self.root.title("Menu")
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
        # Criação e posicionamento do botão que cria um grupo (parte 2 do trabalho)
        self.bt_usuarios = Button(self.root, text="Ver usuários", font=LB_FONT, bd=BT_BORDER,
                               command=self.bt_usuarios_click,
                               bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
        self.bt_usuarios.place(relx=0.35, rely=0.25, relwidth=0.3, relheight=0.15)

        # Criação e posicionamento do botão que acessa o catálogo de vídeos
        self.bt_grupos = Button(self.root, text="Ver grupos", font=LB_FONT, bd=BT_BORDER,
                                command=self.bt_grupos_click,
                                bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
        self.bt_grupos.place(relx=0.35, rely=0.6, relwidth=0.3, relheight=0.15)

    # Função executada ao clicar no botão bt_usuarios
    def bt_usuarios_click(self):
        # Chama a janela de usuários (passa a janela atual)
        JanelaUsuarios(self)

    # Função executada ao clicar no botão bt_grupos
    def bt_grupos_click(self):
        # Chama a janela de grupos (passa a janela atual)
        JanelaGrupos(self)

    # Fecha o programa
    def sair(self):
        # Fecha a janela atual
        self.root.destroy()


class JanelaUsuarios:
    def __init__(self, parent):
        # Fecha a janela anterior
        parent.root.destroy()
        # Cria a janela de usuários
        self.root = Tk()

        # Configurações básicas da janela
        self.root.title("Usuários")
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
        opcoes.add_command(label="Voltar", command=self.voltar)
        # Opção que fecha o programa
        opcoes.add_command(label="Sair", command=self.sair)

    # Criação do frame
    def criar_frame(self):
        self.frame = Frame(self.root, bg=BACKGROUND_COLOR)
        self.frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    # Criação dos widgets
    def criar_widgets(self):
        # Leitura do arquivo usuarios.txt
        arqUsuario = open("Usuarios/usuarios.txt")
        linhas = arqUsuario.readlines()
        arqUsuario.close()

        # Pega lista de usuários
        self.usuarios = []
        for linha in linhas:
            linha_sem_barra_n = linha[0:len(linha) - 1]
            usuario = linha_sem_barra_n.split(" ")[0:2]
            self.usuarios.append(usuario)

        # Criação e posicionamento da lista de usuários
        self.lista_usuarios = ttk.Treeview(self.root, column=("col0", "col1", "col2"))
        self.lista_usuarios.heading("#0", text="")
        self.lista_usuarios.heading("#1", text="Nome")
        self.lista_usuarios.heading("#2", text="Tipo")
        self.lista_usuarios.column("#0", width=1)
        self.lista_usuarios.column("#1", width=250)
        self.lista_usuarios.column("#2", width=250)
        self.lista_usuarios.place(relx=0.1, rely=0.1, relwidth=0.77, relheight=0.8)

        # Criação e posicionamento da barra de rolamento
        self.scroll_lista = Scrollbar(self.root, orient='vertical')
        self.scroll_lista.place(relx=0.87, rely=0.1, relheight=0.8)

        # Conecta a barra de rolamento com a lista de usuários
        self.scroll_lista['command'] = self.lista_usuarios.yview
        self.lista_usuarios.configure(yscroll=self.scroll_lista.set)

        # Insere os usuários na lista
        for usuario in self.usuarios:
            self.lista_usuarios.insert("", END, values=usuario)

    # Volta para a janela de login
    def voltar(self):
        # Chama a janela de menu (passa a janela atual)
        JanelaMenu(self)

    # Fecha o programa
    def sair(self):
        # Fecha a janela atual
        self.root.destroy()


class JanelaGrupos:
    def __init__(self, parent):
        # Fecha a janela anterior
        parent.root.destroy()
        # Cria a janela de grupos
        self.root = Tk()

        # Configurações básicas da janela
        self.root.title("Grupos")
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
        # Opção que fecha o programa
        opcoes.add_command(label="Sair", command=self.sair)

    # Criação do frame
    def criar_frame(self):
        self.frame = Frame(self.root, bg=BACKGROUND_COLOR)
        self.frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    # Criação dos widgets
    def criar_widgets(self):
        # Pega lista de grupos
        self.grupos = next(os.walk("Grupos"), (None, None, []))[2]
        self.grupos = list(map(lambda grupo: grupo[:-4], self.grupos))

        # Criação e posicionamento da lista de grupos
        self.lista_grupos = ttk.Treeview(self.root, column=("col0", "col1"))
        self.lista_grupos.heading("#0", text="")
        self.lista_grupos.heading("#1", text="Grupos")
        self.lista_grupos.column("#0", width=1)
        self.lista_grupos.column("#1", width=500)
        self.lista_grupos.place(relx=0.1, rely=0.1, relwidth=0.77, relheight=0.7)

        # Criação e posicionamento da barra de rolamento
        self.scroll_lista = Scrollbar(self.root, orient='vertical')
        self.scroll_lista.place(relx=0.87, rely=0.1, relheight=0.7)

        # Conecta a barra de rolamento com a lista de grupos
        self.scroll_lista['command'] = self.lista_grupos.yview
        self.lista_grupos.configure(yscroll=self.scroll_lista.set)

        # Insere os grupos na lista
        for grupo in self.grupos:
            self.lista_grupos.insert("", END, values=grupo)

        # Criação e posicionamento do botão para ver os membros do grupo selecionado
        self.bt_membros = Button(self.root, text="Ver membros", font=LB_FONT, bd=BT_BORDER,
                                 command=self.bt_membros_click,
                                 bg=BT_BACKGROUND_COLOR, fg=BT_FOREGROUND_COLOR)
        self.bt_membros.place(relx=0.35, rely=0.85, relwidth=0.3, relheight=0.05)

    # Função executada ao clicar no botão bt_membros
    def bt_membros_click(self):
        # Recupera o grupo selecionado
        selecionado = self.lista_grupos.selection()
        # Verifica se somente um grupo foi selecionado
        if len(selecionado) == 1:
            # Recupera o nome do grupo selecionado
            grupo = self.lista_grupos.item(selecionado, 'values')[0]

            # Chama a janela de membros (passa a janela atual e o grupo selecionado)
            JanelaMembros(self, grupo)

        # Verifica se mais de um grupo foi selecionado
        elif selecionado:
            # Mensagem de erro
            messagebox.showerror("ERRO", "Selecione somente um grupo")
        # Verifica se nenhum grupo foi selecionado
        else:
            # Mensagem de erro
            messagebox.showerror("ERRO", "Selecione o grupo cujos\nmembros você deseja ver")

    # Volta para a janela de menu
    def voltar(self):
        # Chama a janela de menu (passa a janela atual)
        JanelaMenu(self)

    # Fecha o programa
    def sair(self):
        # Fecha a janela atual
        self.root.destroy()


class JanelaMembros:
    def __init__(self, parent, grupo):
        # Fecha a janela anterior
        parent.root.destroy()
        # Cria a janela de membros
        self.root = Tk()

        # Define o nome do arquivo do grupo
        self.arq_grupo_nome = grupo + '.txt'

        # Configurações básicas da janela
        self.root.title("Membros")
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

        # Opção que volta para a janela de grupos
        opcoes.add_command(label="Voltar", command=self.voltar)
        # Opção que volta para a janela de menu
        opcoes.add_command(label="Menu", command=self.menu)
        # Opção que fecha o programa
        opcoes.add_command(label="Sair", command=self.sair)

    # Criação do frame
    def criar_frame(self):
        self.frame = Frame(self.root, bg=BACKGROUND_COLOR)
        self.frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    # Criação dos widgets
    def criar_widgets(self):
        # Leitura do arquivo dos membros do grupo
        try:    
            arqGrupo = open("Grupos/" + self.arq_grupo_nome)
        except:
            messagebox.showerror("EERO", "Grupo inválido")
            JanelaGrupos(self)
        else:
            linhas = arqGrupo.readlines()
            arqGrupo.close()

            # Pega lista de membros
            self.membros = []
            for linha in linhas:
                linha_sem_barra_n = linha[0:len(linha) - 1]
                membro = linha_sem_barra_n.split(" ")[0]
                self.membros.append(membro)

            # Criação e posicionamento da lista de usuários
            self.lista_membros = ttk.Treeview(self.root, column=("col0", "col1"))
            self.lista_membros.heading("#0", text="")
            self.lista_membros.heading("#1", text="Membros")
            self.lista_membros.column("#0", width=1)
            self.lista_membros.column("#1", width=500)
            self.lista_membros.place(relx=0.1, rely=0.1, relwidth=0.77, relheight=0.8)

            # Criação e posicionamento da barra de rolamento
            self.scroll_lista = Scrollbar(self.root, orient='vertical')
            self.scroll_lista.place(relx=0.87, rely=0.1, relheight=0.8)

            # Conecta a barra de rolamento com a lista de usuários
            self.scroll_lista['command'] = self.lista_membros.yview
            self.lista_membros.configure(yscroll=self.scroll_lista.set)

            # Insere os membros na lista
            for membro in self.membros:
                self.lista_membros.insert("", END, values=membro)

    # Volta para a janela de grupos
    def voltar(self):
        # Chama a janela de grupos (passa a janela atual)
        JanelaGrupos(self)

    # Volta para a janela de menu
    def menu(self):
        # Chama a janela de menu (passa a janela atual)
        JanelaMenu(self)

    # Fecha o programa
    def sair(self):
        # Fecha a janela atual
        self.root.destroy()


if __name__ == "__main__":
    # Chama a janela de menu
    JanelaMenu()
