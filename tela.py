import customtkinter as ctk
from PIL import Image, ImageTk

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
        for widget in self.winfo_children():
            widget.grid_forget()
        """Cria e posiciona a imagem na tela de login"""
        imagem = Image.open("img_do_carro.png").resize((250, 150))
        self.imagem_de_inicio = ImageTk.PhotoImage(imagem)

        self.lb_imagem = ctk.CTkLabel(self, image=self.imagem_de_inicio, text=None)
        self.lb_imagem.grid(row=1, column=0, padx=105, pady=(40, 10))

        self.texto_de_boas_vindas = ctk.CTkLabel(self,text="Seja Bem Vindo",font=('Century Gothic bold',32),
                                                 text_color="#FF0000",)
        self.texto_de_boas_vindas.grid()


        self.ver_usuario = ctk.CTkEntry(self, placeholder_text="Usuario", justify="center",border_width=3,
                                        border_color="black",font=('Century Gothic bold',32), width=250,height=40,
                                        corner_radius=45)
        self.ver_usuario.grid(row=3, column=0, pady=(10, 10))

        self.ver_senha = ctk.CTkEntry(self, placeholder_text="Senha", justify="center", width=250, height=40,
                                      font=('Century Gothic bold',32), corner_radius=45,border_width=3,
                                      border_color="black",show="*")
        self.ver_senha.grid(row=4, column=0, pady=(10, 10))

        self.mostrar_senha = ctk.CTkCheckBox(
            self, text="Mostrar senha", width=250, font=("Arial", 20), text_color="white", corner_radius=30,
            border_color="black",border_width=3,
            command=lambda: self.ver_senha.configure(show="" if self.mostrar_senha.get() else "*"))
        self.mostrar_senha.grid( pady=(10, 40), padx=90, )

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=6, column=0, pady=10)

        self.botao_entrar = ctk.CTkButton(self.frame_botoes, text="Entrar", width=50, height=50,corner_radius=70,
                                          font=('Century Gothic bold',32), fg_color="white", text_color="gray", command=self.criar_tela_entrar)
        self.botao_entrar.grid(row=0, column=0, padx=8)  # Espaçamento horizontal entre os botões

        self.botao_cadastrar = ctk.CTkButton(self.frame_botoes, text="Cadastrar", width=50, height=50,corner_radius=70,
                                             font=('Century Gothic bold',32),command=self.criar_tela_cadastro)
        self.botao_cadastrar.grid(row=0, column=1, padx=8)

        # Ajustar as colunas do frame para garantir o mesmo peso
        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)

    def criar_tela_cadastro(self):

        self.limpar_tela()

        self.texto_de_boas_vindas_cadastro = ctk.CTkLabel(self, text="Cadastro", font=('Century Gothic bold',42),
                                                          text_color="green")
        self.texto_de_boas_vindas_cadastro.grid(padx=120, pady=(40,0))
        self.texto = ctk.CTkLabel(self, text="--"*9,font=('Century Gothic bold',32),text_color="green")
        self.texto.grid()

        self.criar_usuario = ctk.CTkEntry(self, placeholder_text="Criar Usuario",font=('Century Gothic bold',26),
                                          width=250,height=40,justify="center",corner_radius=45,border_width=3,
                                          border_color="black")
        self.criar_usuario.grid(pady=(30,10))

        self.criar_senha = ctk.CTkEntry(self, placeholder_text="Criar Senha", font=('Century Gothic bold', 26),
                                          width=250, height=40, justify="center", corner_radius=45, border_width=3,
                                          border_color="black",show="*")
        self.criar_senha.grid()

        self.repetir_criar_senha = ctk.CTkEntry(self, placeholder_text="Repita a Senha", font=('Century Gothic bold', 26),
                                          width=250, height=40, justify="center", corner_radius=45, border_width=3,
                                          border_color="black",show="*")
        self.repetir_criar_senha.grid(pady=(10,15))

        self.mostrar_senha = ctk.CTkCheckBox(
            self, text="Mostrar senha", width=250, font=("Arial", 25), text_color="white", corner_radius=30,
            border_color="black", border_width=3,
            command=self.mostrar_senhas)
        self.mostrar_senha.grid(row=5, column=0, pady=(1,0), )

        self.opcoes = ["Qual estado você nasceu?", "Qual é o nome do seu melhor amigo?",
                  "Qual o nome do seu primeiro animal?"]
        combo_box = ctk.CTkComboBox(self, values=self.opcoes, width=275, height=38,
                                              font=("Arial", 25), state="readonly")
        combo_box.grid(padx=15, pady=15)

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=7, column=0, pady=10)

        self.botao_criar_conta = ctk.CTkButton(self.frame_botoes, text="Criar conta", font=("Century Gothic bold", 30),corner_radius=460)
        self.botao_criar_conta.grid(row=0,column=0,padx=8)

        self.botao_voltar = ctk.CTkButton(self.frame_botoes,command=self.criar_tela_login, text="Voltar",font=("Century Gothic bold", 30),corner_radius=460)
        self.botao_voltar.grid(row=0, column=1,padx=8)

        # Ajustar as colunas do frame para garantir o mesmo peso
        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)

    def criar_tela_entrar(self):
        self.limpar_tela()

        self.texto_de_boas_vindas = ctk.CTkLabel(self, text="Qual função deseja?", text_color="yellow", font=("Century Gothic bold", 32))
        self.texto_de_boas_vindas.grid(padx=60, pady=(25,0))









        self.botao_voltar = ctk.CTkButton(self, command=self.criar_tela_login, text="Voltar")
        self.botao_voltar.grid()


if __name__ == "__main__":
    tela = Tela()
    tela.mainloop()
