import customtkinter as ctk
from tkinter import ttk
from banco_de_dados_clientes import Cliente, secao
from fpdf import FPDF
from tkinter import filedialog, Tk

class TelaVerCliente(ctk.CTkFrame):
    def __init__(self, master, switch_to_clientes, switch_to_detalhes_cliente):
        super().__init__(master, fg_color="darkblue")
        self.master = master
        self.switch_to_clientes = switch_to_clientes
        self.switch_to_detalhes_cliente = switch_to_detalhes_cliente
        
        self.criar_widgets()
        self.configurar_grid()
        
        # Variáveis para paginação
        self.clientes = []
        self.pagina_atual = 0
        self.resultados_por_pagina = 10
        
        # Carregar dados iniciais
        self.atualizar_lista_clientes()

    def configurar_grid(self):
        # Configuração responsiva do grid
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

    def criar_widgets(self):
        # Barra de busca
        self.search_var = ctk.StringVar()
        self.entry_search = ctk.CTkEntry(
            self,
            textvariable=self.search_var,
            placeholder_text="Buscar por nome...",
            width=500,
            font=('Century Gothic', 15)
        )
        self.entry_search.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.entry_search.bind("<KeyRelease>", lambda event: self.atualizar_lista_clientes())
        
        self.btn_search = ctk.CTkButton(
            self,
            text="Buscar",
            font=('Century Gothic bold', 15),
            command=self.atualizar_lista_clientes
        )
        self.btn_search.grid(row=0, column=1, padx=10, pady=10)

        # Frame rolável para lista de clientes
        self.frame_scrollable = ctk.CTkScrollableFrame(
            self,
            width=720,
            height=489
        )
        self.frame_scrollable.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.frame_scrollable.grid_columnconfigure(0, weight=1)

        # Botões de navegação
        self.btn_anterior = ctk.CTkButton(
            self,
            text="Anterior",
            font=('Century Gothic bold', 15),
            command=self.carregar_pagina_anterior
        )
        self.btn_anterior.grid(row=2, column=0, pady=10, sticky="w", padx=10)

        self.btn_proximo = ctk.CTkButton(
            self,
            text="Próximo",
            font=('Century Gothic bold', 15),
            command=self.carregar_proxima_pagina
        )
        self.btn_proximo.grid(row=2, column=1, pady=10, sticky="e", padx=10)

        # Botão Voltar
        self.btn_voltar = ctk.CTkButton(
            self,
            text="Voltar",
            corner_radius=70,
            font=('Century Gothic bold', 22),
            command=self.switch_to_clientes
        )
        self.btn_voltar.grid(row=3, column=0, columnspan=2, pady=10)

    def atualizar_lista_clientes(self):
        busca = self.search_var.get().strip()
        self.clientes = self.obter_clientes(busca=busca)
        self.pagina_atual = 0
        self.mostrar_clientes_na_tela()

    def mostrar_clientes_na_tela(self):
        # Limpar frame existente
        for widget in self.frame_scrollable.winfo_children():
            widget.destroy()

        # Cabeçalhos
        headers = ["Nome", "Data Entrada", "Marca do Carro", "Placa do Carro", "Está Pago"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(
                self.frame_scrollable,
                text=header,
                width=120,
                fg_color="#A9A9A9",
                text_color="white",
                font=('Century Gothic bold', 15)
            )
            label.grid(row=0, column=col, padx=5, pady=5, sticky="ew")

        # Calcular índices da página atual
        inicio = self.pagina_atual * self.resultados_por_pagina
        fim = inicio + self.resultados_por_pagina
        clientes_pagina = self.clientes[inicio:fim]

        # Exibir clientes
        for row, cliente in enumerate(clientes_pagina, start=1):
            btn_nome = ctk.CTkButton(
                self.frame_scrollable,
                text=cliente["nome"],
                width=120,
                font=('Century Gothic bold', 14),
                command=lambda c=cliente: self.switch_to_detalhes_cliente(c)
            )
            btn_nome.grid(row=row, column=0, padx=5, pady=5, sticky="ew")

            ctk.CTkLabel(
                self.frame_scrollable,
                text=str(cliente["data_entrada"] or "Não informado"),
                font=('Century Gothic bold', 14)
            ).grid(row=row, column=1, padx=5, pady=5, sticky="ew")
            
            ctk.CTkLabel(
                self.frame_scrollable,
                text=cliente["marca_carro"] or "Não informado",
                font=('Century Gothic bold', 14)
            ).grid(row=row, column=2, padx=5, pady=5, sticky="ew")
            
            ctk.CTkLabel(
                self.frame_scrollable,
                text=cliente["placa_carro"] or "Não informado",
                font=('Century Gothic bold', 14)
            ).grid(row=row, column=3, padx=5, pady=5, sticky="ew")
            
            ctk.CTkLabel(
                self.frame_scrollable,
                text="Sim" if cliente["valor"] else "Não",
                font=('Century Gothic bold', 14)
            ).grid(row=row, column=4, padx=5, pady=5, sticky="ew")

        # Atualizar estado dos botões de navegação
        self.btn_anterior.configure(state="normal" if self.pagina_atual > 0 else "disabled")
        self.btn_proximo.configure(state="normal" if fim < len(self.clientes) else "disabled")

    def carregar_pagina_anterior(self):
        if self.pagina_atual > 0:
            self.pagina_atual -= 1
            self.mostrar_clientes_na_tela()

    def carregar_proxima_pagina(self):
        if (self.pagina_atual + 1) * self.resultados_por_pagina < len(self.clientes):
            self.pagina_atual += 1
            self.mostrar_clientes_na_tela()

    def obter_clientes(self, busca=""):
        query = secao.query(Cliente)
        if busca:
            query = query.filter(Cliente.nome.ilike(f"%{busca}%"))
        
        query = query.order_by(Cliente.data_entrada.desc())
        
        clientes_query = query.all()
        clientes = [
            {
                "id": cliente.id,
                "nome": cliente.nome,
                "cpf": cliente.cpf,
                "email": cliente.email,
                "telefone": cliente.telefone,
                "data_entrada": cliente.data_entrada,
                "valor": cliente.valor,
                "marca_carro": cliente.marca_carro,
                "placa_carro": cliente.placa_carro,
                "forma_pagamento": cliente.forma_pagamento,
                "data_saida": cliente.data_saida,
                "pecas_utilizadas": cliente.pecas_utilizadas,
            }
            for cliente in clientes_query
        ]
        
        return clientes