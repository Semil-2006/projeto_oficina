import customtkinter as ctk
from PIL import Image, ImageTk
from sqlalchemy.exc import IntegrityError
from banco_de_dados_login import session, Usuario


class Tela(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._configurar_tela()
        self.criar_tela_login()

    def mostrar_senhas(self):
        show = "" if self.mostrar_senha.get() else "*"
        self.criar_senha.configure(show=show)
        self.repetir_criar_senha.configure(show=show)

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.grid_forget()

    def _configurar_tela(self):
        """Configura as propriedades iniciais da janela"""
        self.geometry("400x700")
        self.resizable(False, False)
        self.configure(fg_color="darkblue")

    def criar_tela_login(self):
        self.limpar_tela()

        # Configuração dos widgets
        self.texto_de_boas_vindas = ctk.CTkLabel(self, text="Seja Bem-Vindo", font=('Century Gothic bold', 32),
                                                 text_color="#FF0000")
        self.texto_de_boas_vindas.grid()

        self.ver_usuario = ctk.CTkEntry(self, placeholder_text="Usuário", justify="center",
                                        font=('Century Gothic bold', 32), width=250, height=40)
        self.ver_usuario.grid(pady=(10, 10))

        self.ver_senha = ctk.CTkEntry(self, placeholder_text="Senha", justify="center", show="*",
                                      font=('Century Gothic bold', 32), width=250, height=40)
        self.ver_senha.grid(pady=(10, 10))

        self.botao_entrar = ctk.CTkButton(self, text="Entrar", command=self.verificar_login,
                                          font=('Century Gothic bold', 32))
        self.botao_entrar.grid(pady=(10, 10))

        self.botao_cadastrar = ctk.CTkButton(self, text="Cadastrar", command=self.criar_tela_cadastro,
                                             font=('Century Gothic bold', 32))
        self.botao_cadastrar.grid(pady=(10, 10))

    def criar_tela_cadastro(self):
        self.limpar_tela()

        # Campos de cadastro
        self.criar_usuario = ctk.CTkEntry(self, placeholder_text="Criar Usuário", font=('Century Gothic bold', 26),
                                          width=250, height=40)
        self.criar_usuario.grid(pady=(30, 10))

        self.criar_senha = ctk.CTkEntry(self, placeholder_text="Criar Senha", font=('Century Gothic bold', 26),
                                        width=250, height=40, show="*")
        self.criar_senha.grid()

        self.repetir_criar_senha = ctk.CTkEntry(self, placeholder_text="Repita a Senha",
                                                font=('Century Gothic bold', 26),
                                                width=250, height=40, show="*")
        self.repetir_criar_senha.grid(pady=(10, 15))

        self.pergunta_seguranca = ctk.CTkEntry(self, placeholder_text="Pergunta de Segurança",
                                               font=('Century Gothic bold', 26), width=250, height=40)
        self.pergunta_seguranca.grid(pady=(10, 10))

        self.resposta_seguranca = ctk.CTkEntry(self, placeholder_text="Resposta",
                                               font=('Century Gothic bold', 26), width=250, height=40)
        self.resposta_seguranca.grid(pady=(10, 10))

        self.botao_criar_conta = ctk.CTkButton(self, text="Criar Conta", command=self.registrar_usuario,
                                               font=("Century Gothic bold", 30))
        self.botao_criar_conta.grid(pady=(10, 10))

        self.botao_voltar = ctk.CTkButton(self, text="Voltar", command=self.criar_tela_login,
                                          font=("Century Gothic bold", 30))
        self.botao_voltar.grid()

    def verificar_login(self):
        """Verifica o login do usuário"""
        nome_usuario = self.ver_usuario.get()
        senha = self.ver_senha.get()

        usuario = session.query(Usuario).filter_by(nome_usuario=nome_usuario, senha=senha).first()
        if usuario:
            ctk.CTkLabel(self, text="Login bem-sucedido!", text_color="green", font=("Century Gothic bold", 20)).grid()
        else:
            ctk.CTkLabel(self, text="Usuário ou senha incorretos.", text_color="red",
                         font=("Century Gothic bold", 20)).grid()

    def registrar_usuario(self):
        """Registra um novo usuário no banco de dados"""
        nome_usuario = self.criar_usuario.get()
        senha = self.criar_senha.get()
        repetir_senha = self.repetir_criar_senha.get()
        pergunta = self.pergunta_seguranca.get()
        resposta = self.resposta_seguranca.get()

        if senha != repetir_senha:
            ctk.CTkLabel(self, text="Senhas não correspondem.", text_color="red",
                         font=("Century Gothic bold", 20)).grid()
            return

        novo_usuario = Usuario(nome_usuario=nome_usuario, senha=senha, pergunta_seguranca=pergunta,
                               resposta_seguranca=resposta)
        try:
            session.add(novo_usuario)
            session.commit()
            ctk.CTkLabel(self, text="Usuário registrado com sucesso!", text_color="green",
                         font=("Century Gothic bold", 20)).grid()
        except IntegrityError:
            session.rollback()
            ctk.CTkLabel(self, text="Usuário já existe.", text_color="red",
                         font=("Century Gothic bold", 20)).grid()


if __name__ == "__main__":
    tela = Tela()
    tela.mainloop()
