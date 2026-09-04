import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tela_detalhes_servico import TelaDetalhesServico

class TelaListarServicos(ctk.CTkFrame):
    def __init__(self, master, carregar_servicos_callback, switch_to_servicos, deletar_servico_callback):
        super().__init__(master, fg_color="darkblue")
        self.master = master
        self.carregar_servicos_callback = carregar_servicos_callback
        self.switch_to_servicos = switch_to_servicos
        self.deletar_servico_callback = deletar_servico_callback
        
        self.criar_widgets()
        self.carregar_servicos()

    def criar_widgets(self):
        # Cabeçalho
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(10, 20), padx=20)
        
        self.titulo = ctk.CTkLabel(
            self.header_frame,
            text="Serviços Cadastrados",
            font=("Century Gothic bold", 24),
            text_color="yellow"
        )
        self.titulo.pack(side="left")
        
        self.botao_voltar = ctk.CTkButton(
            self.header_frame,
            text="Voltar",
            font=("Century Gothic", 14),
            width=100,
            command=self.switch_to_servicos
        )
        self.botao_voltar.pack(side="right")
        
        # Frame para a lista
        self.lista_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.lista_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Adicionando scrollbar
        self.scrollbar = ttk.Scrollbar(self.lista_frame)
        self.scrollbar.pack(side="right", fill="y")
        
        # Treeview para listar os serviços
        self.treeview = ttk.Treeview(
            self.lista_frame,
            columns=("Nome",),
            show="headings",
            height=15,
            yscrollcommand=self.scrollbar.set,
            selectmode="browse"
        )
        # Configurar estilo
        style = ttk.Style()
        style.configure("Treeview", 
                        background="#2b2b2b", 
                        foreground="white", 
                        fieldbackground="#2b2b2b",
                        font=("Century Gothic", 12))
        style.configure("Treeview.Heading", 
                        background="#4169E1", 
                        foreground="white",
                        font=("Century Gothic bold", 14))
        style.map("Treeview", background=[('selected', '#3498db')])
        
        self.treeview.heading("Nome", text="Nome do Serviço")
        self.treeview.column("Nome", width=280, anchor="w")
        self.treeview.pack(side="left", fill="both", expand=True)
        self.treeview.bind("<Double-1>", self.abrir_detalhes_servico)
        
        self.scrollbar.configure(command=self.treeview.yview)

    def carregar_servicos(self):
        self.treeview.delete(*self.treeview.get_children())
        servicos = self.carregar_servicos_callback()
        for servico in servicos:
            self.treeview.insert("", "end", iid=servico.id, values=(servico.nome,))
    
    def abrir_detalhes_servico(self, event):
        selected = self.treeview.selection()
        if selected:
            servico_id = selected[0]
            servico = next((s for s in self.carregar_servicos_callback() if s.id == int(servico_id)), None)
            if servico:
                # Abre a janela de detalhes
                TelaDetalhesServico(
                    self,
                    servico=servico,
                    deletar_servico_callback=self.deletar_servico_callback,
                    atualizar_lista_callback=self.carregar_servicos
                )

    # Não é mais necessário o método deletar_servico aqui