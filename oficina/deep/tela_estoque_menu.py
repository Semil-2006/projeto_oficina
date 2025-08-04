import customtkinter as ctk

class EstoqueScreen(ctk.CTkFrame):
    def __init__(self, master, switch_to_adicionar_pecas, switch_to_ver_estoque, switch_to_menu_principal):
        super().__init__(master, fg_color="darkblue")
        self.master = master
        self.switch_to_adicionar_pecas = switch_to_adicionar_pecas
        self.switch_to_ver_estoque = switch_to_ver_estoque
        self.switch_to_menu_principal = switch_to_menu_principal
        
        self.criar_widgets()
        self.configurar_grid()

    def configurar_grid(self):
        # Configurar o grid: 5 linhas e 1 coluna
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def criar_widgets(self):
        # Título
        self.titulo = ctk.CTkLabel(
            self,
            text="Estoque",
            text_color="yellow",
            font=("Century Gothic bold", 52)
        )
        self.titulo.grid(row=0, column=0, padx=120, pady=(60,20))

        # Botão "Adicionar Peças"
        self.btn_adicionar_pecas = ctk.CTkButton(
            self,
            text="Adicionar Peças",
            font=("Century Gothic bold", 42),
            width=225,
            corner_radius=360,
            command=self.switch_to_adicionar_pecas
        )
        self.btn_adicionar_pecas.grid(row=1, column=0, pady=(0,20))

        # Botão "Ver Estoque"
        self.btn_ver_estoque = ctk.CTkButton(
            self,
            text="Ver Estoque",
            font=("Century Gothic bold", 42),
            width=365,
            corner_radius=360,
            command=self.switch_to_ver_estoque
        )
        self.btn_ver_estoque.grid(row=2, column=0)

        # Botão "Voltar"
        self.btn_voltar = ctk.CTkButton(
            self,
            text="Voltar",
            font=("Century Gothic bold", 42),
            width=225,
            corner_radius=360,
            command=self.switch_to_menu_principal
        )
        self.btn_voltar.grid(row=4, column=0, pady=60)