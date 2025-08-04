import customtkinter as ctk
import re
from tkinter import messagebox
from banco_de_dados_de_servicos import Peca, seccao

class TelaCadastrarPeca(ctk.CTkFrame):
    def __init__(self, master, switch_to_estoque):
        super().__init__(master, fg_color="darkblue")
        self.switch_to_estoque = switch_to_estoque
        
        self.criar_widgets()
        self.configurar_grid()

    def configurar_grid(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def criar_widgets(self):
        # Título
        self.titulo = ctk.CTkLabel(
            self,
            text="Cadastrar Peças",
            text_color="yellow",
            font=("Century Gothic bold", 42)
        )
        self.titulo.grid(row=0, column=0, padx=60, pady=(70, 50))

        # Campo Nome da Peça
        self.nome_da_peca = ctk.CTkEntry(
            self,
            placeholder_text="Nome Da Peça",
            justify="center",
            border_width=2,
            border_color="black",
            font=('Century Gothic bold', 24),
            width=400,
            height=60,
            corner_radius=45
        )
        self.nome_da_peca.grid(row=1, column=0, pady=(0,20))

        # Campo Quantidade
        self.qtdd_dessa_peca = ctk.CTkEntry(
            self,
            placeholder_text="Quantidade Dessa Peça",
            justify="center",
            border_width=2,
            border_color="black",
            font=('Century Gothic bold', 24),
            width=400,
            height=60,
            corner_radius=45
        )
        self.qtdd_dessa_peca.grid(row=2, column=0)
        self.qtdd_dessa_peca.bind("<KeyRelease>", self.validar_entrada)

        # Frame para botões
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=3, column=0, pady=50)

        # Botão Cadastrar
        self.btn_cadastrar_pecas = ctk.CTkButton(
            self.frame_botoes,
            text="Cadastrar",
            font=("Century Gothic bold", 25),
            width=200,
            corner_radius=360,
            command=self.cadastrar_peca
        )
        self.btn_cadastrar_pecas.grid(row=0, column=0)

        # Botão Voltar
        self.btn_voltar = ctk.CTkButton(
            self.frame_botoes,
            text="Voltar",
            font=("Century Gothic bold", 25),
            width=200,
            corner_radius=360,
            command=self.switch_to_estoque
        )
        self.btn_voltar.grid(row=0, column=1, padx=20)

    def validar_entrada(self, event):
        texto_atual = self.qtdd_dessa_peca.get()
        if not all(c.isdigit() for c in texto_atual):
            self.qtdd_dessa_peca.delete(0, "end")
            self.qtdd_dessa_peca.insert(0, texto_atual[:-1])

    def cadastrar_peca(self):
        nome = self.nome_da_peca.get()
        try:
            quantidade = int(self.qtdd_dessa_peca.get())
        except ValueError:
            messagebox.showerror("Erro", "O campo Quantidade deve ser um número inteiro!")
            return

        if not nome:
            messagebox.showerror("Erro", "O campo Nome Da Peça é obrigatório!")
            return

        try:
            nova_peca = Peca(nome=nome, quantidade=quantidade)
            seccao.add(nova_peca)
            seccao.commit()
            messagebox.showinfo("Sucesso", "Peça cadastrada com sucesso!")
            self.switch_to_estoque()
        except Exception as e:
            seccao.rollback()
            messagebox.showerror("Erro", f"Erro ao cadastrar peça: {e}")
            self.nome_da_peca.delete(0, 'end')
            self.qtdd_dessa_peca.delete(0, 'end')