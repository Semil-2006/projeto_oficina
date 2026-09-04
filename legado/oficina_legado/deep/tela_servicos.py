import customtkinter as ctk
from PIL import Image, ImageTk

class ServicosScreen(ctk.CTkFrame):
    def __init__(self, master, switch_to_cadastrar_servico, switch_to_listar_servicos, switch_to_menu_principal):
        super().__init__(master, fg_color="darkblue")
        self.master = master
        self.switch_to_cadastrar_servico = switch_to_cadastrar_servico
        self.switch_to_listar_servicos = switch_to_listar_servicos
        self.switch_to_menu_principal = switch_to_menu_principal
        
        self.criar_widgets()

    def criar_widgets(self):
        # Cabeçalho com ícone
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(20, 10), fill="x")
        
        try:
            self.logo_image = ctk.CTkImage(
                light_image=Image.open("img_do_carro.png"),
                size=(80, 40)
            )
            self.logo_label = ctk.CTkLabel(
                self.header_frame, 
                image=self.logo_image, 
                text=""
            )
            self.logo_label.pack(side="left", padx=20)
        except:
            pass
        
        self.label = ctk.CTkLabel(
            self.header_frame, 
            text="Gerenciamento de Serviços",
            font=("Century Gothic bold", 24),
            text_color="yellow"
        )
        self.label.pack(side="left", padx=10, pady=10)
        
        # Botões principais
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=30, padx=50, fill="both", expand=True)
        
        self.botao_cadastrar = ctk.CTkButton(
            self.button_frame,
            text="Cadastrar Novo Serviço",
            font=("Century Gothic bold", 20),
            height=50,
            corner_radius=10,
            fg_color="#2E8B57",
            hover_color="#3CB371",
            command=self.switch_to_cadastrar_servico
        )
        self.botao_cadastrar.pack(pady=15, fill="x")
        
        self.botao_lista_servicos = ctk.CTkButton(
            self.button_frame,
            text="Visualizar Serviços Cadastrados",
            font=("Century Gothic bold", 20),
            height=50,
            corner_radius=10,
            fg_color="#4169E1",
            hover_color="#6495ED",
            command=self.switch_to_listar_servicos
        )
        self.botao_lista_servicos.pack(pady=15, fill="x")
        
        # Botão de voltar
        self.botao_voltar = ctk.CTkButton(
            self.button_frame,
            text="Voltar ao Menu Principal",
            font=("Century Gothic bold", 18),
            height=40,
            corner_radius=8,
            fg_color="#B22222",
            hover_color="#CD5C5C",
            command=self.switch_to_menu_principal
        )
        self.botao_voltar.pack(pady=30, fill="x")