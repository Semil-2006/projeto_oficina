import customtkinter as ctk

class TelaClientes(ctk.CTkFrame):
    def __init__(self, master, switch_to_cadastrar_cliente, switch_to_ver_cliente, switch_to_menu_principal):
        super().__init__(master, fg_color="darkblue")
        self.master = master
        self.switch_to_cadastrar_cliente = switch_to_cadastrar_cliente
        self.switch_to_ver_cliente = switch_to_ver_cliente
        self.switch_to_menu_principal = switch_to_menu_principal
        
        self.criar_widgets()
        self.configurar_grid()

    def configurar_grid(self):
        # Configuração responsiva do grid
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def criar_widgets(self):
        # Título
        self.titulo = ctk.CTkLabel(
            self,
            text="Clientes",
            font=("Century Gothic bold", 42),
            text_color="yellow"
        )
        self.titulo.grid(row=0, column=0, pady=(50, 20))

        # Botão Cadastrar Cliente
        self.btn_cadastrar = ctk.CTkButton(
            self,
            text="Cadastrar cliente",
            font=("Century Gothic bold", 42),
            width=225,
            corner_radius=360,
            command=self.switch_to_cadastrar_cliente
        )
        self.btn_cadastrar.grid(row=1, column=0, pady=20)

        # Botão Ver Clientes
        self.btn_ver = ctk.CTkButton(
            self,
            text="Ver Clientes",
            font=("Century Gothic bold", 42),
            width=400,
            corner_radius=360,
            command=self.switch_to_ver_cliente
        )
        self.btn_ver.grid(row=2, column=0, pady=20)

        # Botão Voltar
        self.btn_voltar = ctk.CTkButton(
            self,
            text="Voltar",
            font=("Century Gothic bold", 32),
            corner_radius=360,
            command=self.switch_to_menu_principal
        )
        self.btn_voltar.grid(row=3, column=0, pady=(50, 20))