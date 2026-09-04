import customtkinter as ctk
from tkinter import Canvas, Scrollbar
from banco_de_dados_de_servicos import seccao, Peca

class TelaVerEstoque(ctk.CTkFrame):
    def __init__(self, master, switch_to_estoque):
        super().__init__(master, fg_color="darkblue")
        self.switch_to_estoque = switch_to_estoque
        
        self.criar_widgets()

    def criar_widgets(self):
        # Título
        self.titulo = ctk.CTkLabel(
            self,
            text="Visualização de Estoque",
            text_color="yellow",
            font=("Century Gothic bold", 24)
        )
        self.titulo.pack(pady=20)

        # Frame para canvas e scrollbar
        frame_container = ctk.CTkFrame(self, fg_color="transparent")
        frame_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Canvas e Scrollbar
        self.canvas = Canvas(frame_container, bg="#2b2b2b", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(frame_container, orientation="vertical", command=self.canvas.yview)
        
        # Frame rolável
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="#2b2b2b")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Carregar peças
        self.carregar_pecas()
        
        # Botão Voltar
        self.btn_voltar = ctk.CTkButton(
            self,
            text="Voltar",
            font=("Century Gothic bold", 24),
            command=self.switch_to_estoque
        )
        self.btn_voltar.pack(pady=20)

    def carregar_pecas(self):
        pecas = seccao.query(Peca).all()
        
        # Cabeçalho
        cabecalho_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#A9A9A9")
        cabecalho_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(cabecalho_frame, text="Nome", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(cabecalho_frame, text="Quantidade", font=("Arial", 16, "bold")).grid(row=0, column=1, padx=10, pady=5)
        
        # Lista de peças
        for i, peca in enumerate(pecas, start=1):
            frame_peca = ctk.CTkFrame(self.scrollable_frame)
            frame_peca.grid(row=i, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
            
            ctk.CTkLabel(frame_peca, text=peca.nome, font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
            ctk.CTkLabel(frame_peca, text=str(peca.quantidade), font=("Arial", 14)).grid(row=0, column=1, padx=10, pady=5)