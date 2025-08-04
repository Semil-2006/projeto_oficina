from PIL import Image, ImageTk
import customtkinter as ctk
import bcrypt
from tkinter import messagebox
from banco_de_dados_login import session, Usuario

class CadastroScreen(ctk.CTkFrame):
    def __init__(self, master, switch_to_login, cadastrar_usuario_callback):
        super().__init__(master, fg_color="darkblue")
        self.master = master
        self.switch_to_login = switch_to_login
        self.cadastrar_usuario_callback = cadastrar_usuario_callback
        
        self.criar_widgets()
        self.configurar_grid()

    def configurar_grid(self):

        for i in range(10): 
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def criar_widgets(self):

        self.texto_de_boas_vindas_cadastro = ctk.CTkLabel(
            self, 
            text="Cadastro", 
            font=('Century Gothic bold', 28),
            text_color="green"
        )
        self.texto_de_boas_vindas_cadastro.grid(row=0, column=0, pady=(20, 5))

        self.texto = ctk.CTkLabel(
            self, 
            text="--"*9,
            font=('Century Gothic bold', 24),
            text_color="green"
        )
        self.texto.grid(row=1, column=0, pady=5)


        campos_config = {
            'height': 35,
            'width': 250,
            'corner_radius': 30,
            'border_width': 2,
            'font': ('Century Gothic', 18)
        }

        self.criar_usuario = ctk.CTkEntry(
            self,
            placeholder_text="Criar Usuario",
            **campos_config
        )
        self.criar_usuario.grid(row=2, column=0, pady=10)

        self.criar_senha = ctk.CTkEntry(
            self,
            placeholder_text="Criar Senha",
            show="*",
            **campos_config
        )
        self.criar_senha.grid(row=3, column=0, pady=10)

        self.repetir_criar_senha = ctk.CTkEntry(
            self,
            placeholder_text="Repita a Senha",
            show="*",
            **campos_config
        )
        self.repetir_criar_senha.grid(row=4, column=0, pady=10)


        self.mostrar_senha = ctk.CTkCheckBox(
            self, 
            text="Mostrar senha",
            font=("Arial", 16),
            text_color="white",
            corner_radius=20,
            border_width=2,
            command=self.mostrar_senhas
        )
        self.mostrar_senha.grid(row=5, column=0, pady=10)


        self.opcoes = [
            "Qual estado você nasceu?",
            "Qual é o nome do seu melhor amigo?",
            "Qual o nome do seu primeiro animal?"
        ]
        self.pergunta_seguranca = ctk.CTkComboBox(
            self, 
            values=self.opcoes, 
            width=250, 
            height=35,
            font=("Arial", 16),
            state="readonly"
        )
        self.pergunta_seguranca.grid(row=6, column=0, pady=10)

        self.resposta_segurança = ctk.CTkEntry(
            self, 
            placeholder_text="Resposta",
            **campos_config
        )
        self.resposta_segurança.grid(row=7, column=0, pady=10)


        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=8, column=0, pady=20)
        

        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)
        self.frame_botoes.grid_rowconfigure(0, weight=1)


        botoes_config = {
            'font': ("Century Gothic bold", 18),
            'width': 120,
            'height': 40,
            'corner_radius': 30
        }

        self.botao_criar_conta = ctk.CTkButton(
            self.frame_botoes,
            text="Criar conta",
            **botoes_config,
            command=self.cadastrar_usuario
        )
        self.botao_criar_conta.grid(row=0, column=0, padx=10)

        self.botao_voltar = ctk.CTkButton(
            self.frame_botoes,
            text="Voltar",
            **botoes_config,
            command=self.switch_to_login
        )
        self.botao_voltar.grid(row=0, column=1, padx=10)

    def mostrar_senhas(self):
        show = "" if self.mostrar_senha.get() else "*"
        self.criar_senha.configure(show=show)
        self.repetir_criar_senha.configure(show=show)

    def cadastrar_usuario(self):
        self.cadastrar_usuario_callback(
            self.criar_usuario,
            self.criar_senha,
            self.repetir_criar_senha,
            self.pergunta_seguranca,
            self.resposta_segurança,
            self.switch_to_login
        )