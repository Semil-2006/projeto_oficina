import customtkinter as ctk

class MenuPrincipalScreen(ctk.CTkFrame):
    def __init__(self, master, switch_to_clientes, switch_to_servicos, switch_to_estoque, switch_to_relatorios, switch_to_login):
        super().__init__(master, fg_color="darkblue")
        self.master = master
        self.switch_to_clientes = switch_to_clientes
        self.switch_to_servicos = switch_to_servicos
        self.switch_to_estoque = switch_to_estoque
        self.switch_to_relatorios = switch_to_relatorios
        self.switch_to_login = switch_to_login
        
        self.criar_widgets()
        self.configurar_grid()

    def configurar_grid(self):

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def criar_widgets(self):

        self.titulo = ctk.CTkLabel(
            self,
            text="Qual função deseja?",
            text_color="yellow",
            font=("Century Gothic bold", 32)
        )
        self.titulo.grid(row=0, column=0, padx=60, pady=(50, 75))


        self.btn_clientes = ctk.CTkButton(
            self,
            text="Clientes",
            font=("Century Gothic bold", 42),
            width=225,
            corner_radius=360,
            command=self.switch_to_clientes
        )
        self.btn_clientes.grid(row=1, column=0, pady=(0, 20))


        self.btn_servicos = ctk.CTkButton(
            self,
            text="Serviços",
            font=("Century Gothic bold", 42),
            width=225,
            corner_radius=360,
            command=self.switch_to_servicos
        )
        self.btn_servicos.grid(row=2, column=0, pady=(0, 20))


        self.btn_estoque = ctk.CTkButton(
            self,
            text="Estoque",
            font=("Century Gothic bold", 42),
            width=225,
            corner_radius=360,
            command=self.switch_to_estoque
        )
        self.btn_estoque.grid(row=3, column=0, pady=(0, 20))


        self.btn_relatorios = ctk.CTkButton(
            self,
            text="Relatorios",
            font=("Century Gothic bold", 42),
            width=225,
            corner_radius=360,
            command=self.switch_to_relatorios
        )
        self.btn_relatorios.grid(row=4, column=0, pady=(0, 20))


        self.btn_sair = ctk.CTkButton(
            self,
            text="SAIR",
            font=("Century Gothic bold", 42),
            fg_color="red",
            command=self.switch_to_login
        )
        self.btn_sair.grid(row=5, column=0, pady=35)