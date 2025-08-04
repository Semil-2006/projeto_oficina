from PIL import Image, ImageTk
import customtkinter as ctk
import bcrypt
from tkinter import messagebox
from banco_de_dados_login import session, Usuario

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, switch_to_register, switch_to_forgot_password, switch_to_main):
        super().__init__(master, fg_color="#1A237E")  # Dark blue mais suave
        self.master = master
        self.switch_to_register = switch_to_register
        self.switch_to_forgot_password = switch_to_forgot_password
        self.switch_to_main = switch_to_main
        
        self.configurar_grid()
        self.criar_widgets()

    def configurar_grid(self):
        # Grid mais organizado com pesos adequados
        for i in range(7): 
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def criar_widgets(self):
        # Imagem com borda sutil
        imagem = Image.open("img_do_carro.png").resize((200, 120))  # Tamanho ligeiramente maior
        self.imagem_de_inicio = ImageTk.PhotoImage(imagem)
        self.lb_imagem = ctk.CTkLabel(
            self, 
            image=self.imagem_de_inicio, 
            text=None,
            fg_color="transparent"
        )
        self.lb_imagem.grid(row=0, column=0, pady=(40, 20))

        # Texto de boas-vindas com gradiente
        self.texto_de_boas_vindas = ctk.CTkLabel(
            self,
            text="Bem-vindo ao Sistema",
            font=('Century Gothic', 26, 'bold'),
            text_color="#FFFFFF"  # Branco para contraste
        )
        self.texto_de_boas_vindas.grid(row=1, column=0, pady=(0, 20))

        # Frame para campos de login com sombra sutil
        self.login_frame = ctk.CTkFrame(
            self,
            fg_color="#283593",  # Tom mais claro de blue
            corner_radius=12,
            border_width=1,
            border_color="#3949AB"
        )
        self.login_frame.grid(row=2, column=0, padx=50, pady=10, sticky="nsew")
        self.login_frame.grid_columnconfigure(0, weight=1)

        # Configurações modernas para os campos
        campo_config = {
            'height': 45,
            'corner_radius': 8,
            'border_width': 1,
            'font': ('Century Gothic', 14),
            'justify': 'left',
            'border_color': '#5C6BC0',
            'fg_color': "#3949AB",  # Fundo dos campos
            'text_color': '#FFFFFF',
            'placeholder_text_color': '#C5CAE9'  # Placeholder mais claro
        }

        # Campo de usuário
        self.ver_usuario = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Nome de usuário",
            **campo_config
        )
        self.ver_usuario.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # Campo de senha
        self.ver_senha = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Senha",
            show="*",
            **campo_config
        )
        self.ver_senha.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Container para opções
        self.options_frame = ctk.CTkFrame(
            self.login_frame,
            fg_color="transparent"
        )
        self.options_frame.grid(row=2, column=0, padx=20, sticky="ew")
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)

        # Checkbox estilizado
        self.mostrar_senha = ctk.CTkCheckBox(
            self.options_frame,
            text="Mostrar senha",
            font=("Century Gothic", 12),
            text_color="#E8EAF6",
            corner_radius=4,
            border_width=1,
            border_color="#5C6BC0",
            hover_color="#7986CB",
            fg_color="#3949AB",
            command=self.toggle_password_visibility
        )
        self.mostrar_senha.grid(row=0, column=0, sticky="w")

        # Link "esqueci senha" estilizado
        self.esqueci_senha_button = ctk.CTkButton(
            self.options_frame,
            text="Esqueci minha senha",
            command=self.switch_to_forgot_password,
            fg_color="transparent",
            hover_color="#283593",
            font=("Century Gothic", 12),
            text_color="#8C9EFF",  # Azul claro
            height=25,
            width=1,
            anchor="e"
        )
        self.esqueci_senha_button.grid(row=0, column=1, sticky="e")

        # Frame para botões
        self.frame_botoes = ctk.CTkFrame(
            self.login_frame, 
            fg_color="transparent"
        )
        self.frame_botoes.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="nsew")
        
        self.frame_botoes.grid_rowconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)

        # Estilo dos botões
        botao_config = {
            'height': 45,
            'corner_radius': 8,
            'font': ('Century Gothic', 14, 'bold'),
            'border_width': 0
        }

        # Botão de entrar com gradiente
        self.botao_entrar = ctk.CTkButton(
            self.frame_botoes,
            text="Entrar",
            fg_color="#2962FF",  # Azul vibrante
            text_color="white",
            hover_color="#0039CB",
            command=self.verificar_login,
            **botao_config
        )
        self.botao_entrar.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        # Botão de cadastrar
        self.botao_cadastrar = ctk.CTkButton(
            self.frame_botoes,
            text="Cadastrar",
            fg_color="#00B0FF",  # Azul claro
            text_color="#1A237E",  # Texto escuro
            hover_color="#0091EA",
            command=self.switch_to_register,
            **botao_config
        )
        self.botao_cadastrar.grid(row=0, column=1, padx=(10, 0), sticky="ew")

    def toggle_password_visibility(self):
        show = "" if self.mostrar_senha.get() else "*"
        self.ver_senha.configure(show=show)

    def verificar_login(self):
        usuario = self.ver_usuario.get().strip().upper()
        senha = self.ver_senha.get().strip()

        if not usuario and not senha:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        if not usuario:
            messagebox.showerror("Erro", "O campo 'Usuário' deve ser preenchido.")
            return

        if not senha:
            messagebox.showerror("Erro", "O campo 'Senha' deve ser preenchido.")
            return

        usuario_encontrado = session.query(Usuario).filter_by(nome_usuario=usuario).first()

        if usuario_encontrado:
            senha_armazenada = usuario_encontrado.senha

            if isinstance(senha_armazenada, str):
                senha_armazenada = senha_armazenada.encode('utf-8')

            if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada):
                self.switch_to_main()
            else:
                messagebox.showerror("Erro", "Senha incorreta. Tente novamente.")
        else:
            messagebox.showerror("Erro", "Usuário não existe.")