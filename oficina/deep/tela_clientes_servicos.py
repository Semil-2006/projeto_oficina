import customtkinter as ctk
from tkinter import ttk

class TelaClientesServicos(ctk.CTkFrame):
    def __init__(self, master, carregar_clientes_servicos_callback, editar_cliente_callback, switch_to_servicos):
        super().__init__(master, fg_color="darkblue")
        self.master = master
        self.carregar_clientes_servicos_callback = carregar_clientes_servicos_callback
        self.editar_cliente_callback = editar_cliente_callback
        self.switch_to_servicos = switch_to_servicos
        
        self.criar_widgets()
        self.carregar_clientes_servicos()

    def criar_widgets(self):
        self.label = ctk.CTkLabel(
            self,
            text="Clientes e Serviços",
            font=("Century Gothic bold", 20),
            text_color="yellow"
        )
        self.label.pack(pady=10)

        self.frame_lista = ctk.CTkFrame(self)
        self.frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.frame_lista, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        colunas = ("Nome", "Marca", "Placa", "Serviços", "Peças", "Valor")
        self.treeview = ttk.Treeview(
            self.frame_lista,
            columns=colunas,
            show="headings",
            height=10,
            yscrollcommand=self.scrollbar.set
        )
        
        for col in colunas:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, anchor="center")
        
        self.treeview.bind("<Double-1>", self.editar_cliente)
        self.treeview.pack(side="left", fill="both", expand=True)
        
        self.scrollbar.config(command=self.treeview.yview)

        self.botao_voltar = ctk.CTkButton(
            self,
            text="Voltar",
            font=("Century Gothic", 14),
            command=self.switch_to_servicos
        )
        self.botao_voltar.pack(pady=10)

    def carregar_clientes_servicos(self):
        clientes_servicos = self.carregar_clientes_servicos_callback()
        for cliente in clientes_servicos:
            self.treeview.insert("", "end", values=(
                cliente.nome,
                cliente.marca_carro,
                cliente.placa_carro,
                "Serviço Placeholder",  # Ajustar para os serviços reais
                cliente.pecas_utilizadas,
                cliente.valor
            ))

    def editar_cliente(self, event):
        item_selecionado = self.treeview.selection()
        if item_selecionado:
            cliente_nome = self.treeview.item(item_selecionado, "values")[0]
            self.editar_cliente_callback(cliente_nome)