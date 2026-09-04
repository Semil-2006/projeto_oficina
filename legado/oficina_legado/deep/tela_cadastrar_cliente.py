import customtkinter as ctk
import re
from datetime import datetime
from tkcalendar import Calendar
from tkinter import messagebox
from banco_de_dados_clientes import Cliente, secao
import tkinter as tk

class TelaCadastrarCliente(ctk.CTkFrame):
    def __init__(self, master, switch_to_clientes):
        super().__init__(master, fg_color="darkblue")
        self.master = master
        self.switch_to_clientes = switch_to_clientes
        
        self.criar_widgets()
        self.configurar_grid()

    def configurar_grid(self):
        # Configuração responsiva do grid
        for i in range(14):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def criar_widgets(self):
        # Título
        self.titulo = ctk.CTkLabel(
            self,
            text="Cadastrar Clientes",
            font=('Century Gothic bold', 32),
            text_color="green"
        )
        self.titulo.grid(row=0, column=0, pady=(30, 2), padx=70)

        self.divisor = ctk.CTkLabel(
            self,
            text="--" * 14,
            font=('Century Gothic bold', 32),
            text_color="green"
        )
        self.divisor.grid(row=1, column=0, pady=(0, 20))

        # Campo Nome do Cliente
        self.nome_cliente = ctk.CTkEntry(
            self,
            placeholder_text="Nome do Cliente",
            font=('Century Gothic bold', 20),
            width=250,
            height=40,
            justify="center",
            corner_radius=45,
            border_width=3,
            border_color="black"
        )
        self.nome_cliente.grid(row=2, column=0, pady=(0, 5))

        # Pergunta sobre CPF na nota
        self.label_cpf_nota = ctk.CTkLabel(
            self,
            text="CPF na nota",
            font=("Arial", 16),
            text_color="white"
        )
        self.label_cpf_nota.grid(row=3, column=0, pady=(0, 5))

        # Frame para opções SIM/NÃO
        self.frame_opcoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_opcoes.grid(row=4, column=0, pady=5)

        self.opcao_selecionada = ctk.StringVar(value="")
        
        self.radio_sim = ctk.CTkRadioButton(
            self.frame_opcoes,
            text="SIM",
            variable=self.opcao_selecionada,
            value="SIM",
            font=("Arial", 20),
            text_color="white",
            command=self.atualizar_interface
        )
        self.radio_sim.grid(row=0, column=0, padx=(60, 15))
        
        self.radio_nao = ctk.CTkRadioButton(
            self.frame_opcoes,
            text="NÃO",
            variable=self.opcao_selecionada,
            value="NÃO",
            font=("Arial", 20),
            text_color="white",
            command=self.atualizar_interface
        )
        self.radio_nao.grid(row=0, column=1, padx=20)

        # Label para resposta (será usada para mostrar o campo CPF)
        self.label_resposta = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 16),
            text_color="white"
        )
        self.label_resposta.grid(row=5, column=0, pady=5)

        # Campo CPF (inicialmente oculto)
        self.entry_cpf = ctk.CTkEntry(
            self,
            placeholder_text="Digite seu CPF",
            font=('Century Gothic bold', 20),
            width=250,
            height=40,
            justify="center",
            corner_radius=45,
            border_width=3,
            border_color="black"
        )
        self.entry_cpf.bind("<KeyRelease>", self.formatar_cpf)
        self.entry_cpf.grid_remove()

        # Campo Email
        self.email_cliente = ctk.CTkEntry(
            self,
            placeholder_text="Email do Cliente",
            font=('Century Gothic bold', 20),
            width=250,
            height=40,
            justify="center",
            corner_radius=45,
            border_width=3,
            border_color="black"
        )
        self.email_cliente.grid(row=6, column=0, pady=5)

        # Campo Telefone
        self.telefone = ctk.CTkEntry(
            self,
            placeholder_text="Telefone de Contato",
            font=('Century Gothic bold', 20),
            width=250,
            height=40,
            justify="center",
            corner_radius=45,
            border_width=3,
            border_color="black"
        )
        self.telefone.grid(row=7, column=0, pady=5)
        self.telefone.bind("<KeyRelease>", self.formatar_telefone)

        # Campo Data de Entrada
        self.data_entrada = ctk.CTkEntry(
            self,
            placeholder_text="Data de Entrada",
            font=('Century Gothic bold', 20),
            width=250,
            height=40,
            justify="center",
            corner_radius=45,
            border_width=3,
            border_color="black"
        )
        self.data_entrada.grid(row=8, column=0, pady=5)
        self.data_entrada.bind("<Button-1>", self.abrir_calendario)

        # Campo Valor
        self.valor = ctk.CTkEntry(
            self,
            placeholder_text="Valor",
            font=('Century Gothic bold', 20),
            width=250,
            height=40,
            justify="center",
            corner_radius=45,
            border_width=3,
            border_color="black"
        )
        self.valor.grid(row=9, column=0, pady=5)
        self.valor.bind("<KeyRelease>", self.formatar_valor)

        # Campo Marca do Carro
        self.marca_carro = ctk.CTkEntry(
            self,
            placeholder_text="Marca do carro",
            font=('Century Gothic bold', 20),
            width=250,
            height=40,
            justify="center",
            corner_radius=45,
            border_width=3,
            border_color="black"
        )
        self.marca_carro.grid(row=10, column=0, pady=5)

        # Campo Placa do Carro
        self.placa_carro = ctk.CTkEntry(
            self,
            placeholder_text="Placa do carro",
            font=('Century Gothic bold', 20),
            width=250,
            height=40,
            justify="center",
            corner_radius=45,
            border_width=3,
            border_color="black"
        )
        self.placa_carro.grid(row=11, column=0, pady=5)
        self.placa_carro.bind('<KeyRelease>', self.formatar_placa)

        # Frame para botões
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=12, column=0, pady=5)

        # Botão Voltar
        self.btn_voltar = ctk.CTkButton(
            self.frame_botoes,
            text="VOLTAR",
            corner_radius=70,
            font=('Century Gothic bold', 22),
            command=self.switch_to_clientes
        )
        self.btn_voltar.grid(row=0, column=0, padx=10)

        # Botão Cadastrar
        self.btn_cadastrar = ctk.CTkButton(
            self.frame_botoes,
            text="CADASTRAR",
            corner_radius=70,
            font=('Century Gothic bold', 22),
            command=self.cadastrar_cliente
        )
        self.btn_cadastrar.grid(row=0, column=1)

    def atualizar_interface(self):
        opcao = self.opcao_selecionada.get()
        if opcao == "SIM":
            self.label_resposta.configure(text="Insira o CPF:")
            self.entry_cpf.grid(row=5, column=0, pady=5)
        elif opcao == "NÃO":
            self.label_resposta.configure(text="")
            self.entry_cpf.grid_remove()

    def formatar_telefone(self, event=None):
        texto = self.telefone.get()
        texto = ''.join(filter(str.isdigit, texto))
        
        if texto.startswith("55"):
            texto = texto[2:]
        texto = "55" + texto

        if len(texto) <= 2:
            texto_formatado = f"+{texto}"
        elif len(texto) <= 4:
            texto_formatado = f"+{texto[:2]} ({texto[2:]})"
        elif len(texto) <= 9:
            texto_formatado = f"+{texto[:2]} ({texto[2:4]}) {texto[4:9]}"
        else:
            texto_formatado = f"+{texto[:2]} ({texto[2:4]}) {texto[4:9]}-{texto[9:13]}"

        self.telefone.delete(0, ctk.END)
        self.telefone.insert(0, texto_formatado)

    def formatar_cpf(self, event):
        cpf = self.entry_cpf.get().replace(".", "").replace("-", "")
        if not cpf.isdigit():
            cpf = "".join(filter(str.isdigit, cpf))

        if len(cpf) > 11:
            cpf = cpf[:11]

        cpf_formatado = ""
        if len(cpf) > 3:
            cpf_formatado = f"{cpf[:3]}."
        if len(cpf) > 6:
            cpf_formatado += f"{cpf[3:6]}."
        if len(cpf) > 9:
            cpf_formatado += f"{cpf[6:9]}-{cpf[9:]}"
        elif len(cpf) > 6:
            cpf_formatado += cpf[6:]
        elif len(cpf) > 3:
            cpf_formatado += cpf[3:]
        else:
            cpf_formatado = cpf

        self.entry_cpf.delete(0, "end")
        self.entry_cpf.insert(0, cpf_formatado)

    def formatar_placa(self, event):
        texto = self.placa_carro.get()
        texto = ''.join([char for char in texto if char.isalnum()])

        if len(texto) > 3:
            texto = texto[:3] + '-' + texto[3:7]
        elif len(texto) > 7:
            texto = texto[:7]

        self.placa_carro.delete(0, ctk.END)
        self.placa_carro.insert(0, texto)

    def formatar_valor(self, event):
        valor = self.valor.get()
        valor = re.sub(r'\D', '', valor)

        if valor == '':
            self.valor.delete(0, ctk.END)
            self.valor.insert(0, "R$ 0,00")
        else:
            valor = int(valor)
            valor_formatado = f"R$ {valor // 100},{valor % 100:02d}"
            self.valor.delete(0, ctk.END)
            self.valor.insert(0, valor_formatado)

    def abrir_calendario(self, event):
        calendario_popup = ctk.CTkToplevel(self)
        calendario_popup.title("Selecione a Data")
        calendario_popup.geometry("300x300")
        calendario_popup.grab_set()  # Modal

        calendario = Calendar(calendario_popup, selectmode='day', date_pattern='yyyy-mm-dd')
        calendario.pack(padx=10, pady=10)

        def selecionar_data():
            data_selecionada = calendario.get_date()
            self.data_entrada.delete(0, tk.END)
            self.data_entrada.insert(0, data_selecionada)
            calendario_popup.destroy()

        btn_confirmar = ctk.CTkButton(calendario_popup, text="Confirmar", command=selecionar_data)
        btn_confirmar.pack(pady=10)

    def cadastrar_cliente(self):
        # Obter valores dos campos
        nome = self.nome_cliente.get().strip().upper()
        cpf = self.entry_cpf.get().strip() if self.opcao_selecionada.get() == "SIM" else None
        email = self.email_cliente.get().strip()
        telefone = self.telefone.get().strip()
        data_entrada = self.data_entrada.get().strip()
        valor_str = self.valor.get().strip()
        marca_carro = self.marca_carro.get().strip()
        placa_carro = self.placa_carro.get().strip()

        # Validações básicas
        if not nome:
            messagebox.showerror("Erro", "O campo Nome do Cliente é obrigatório!")
            return
        if not data_entrada:
            messagebox.showerror("Erro", "O campo Data de Entrada é obrigatório!")
            return
        if not marca_carro:
            messagebox.showerror("Erro", "O campo Marca do Carro é obrigatório!")
            return
        if not placa_carro:
            messagebox.showerror("Erro", "O campo Placa do Carro é obrigatório!")
            return

        # Converter valor para float
        valor = None
        if valor_str:
            try:
                valor = float(valor_str.replace("R$", "").replace(".", "").replace(",", ".").strip())
            except ValueError:
                messagebox.showerror("Erro", "O campo Valor está em um formato inválido!")
                return

        # Converter data
        try:
            data_entrada = datetime.strptime(data_entrada, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Erro", "A Data de Entrada está em um formato inválido! Use o formato YYYY-MM-DD.")
            return

        # Criar objeto cliente
        novo_cliente = Cliente(
            nome=nome,
            cpf=cpf,
            email=email if email else None,
            telefone=telefone if telefone else None,
            data_entrada=data_entrada,
            valor=valor,
            marca_carro=marca_carro,
            placa_carro=placa_carro,
            forma_pagamento=None,
            data_saida=None,
            pecas_utilizadas=None
        )

        try:
            # Salvar no banco de dados
            secao.add(novo_cliente)
            secao.commit()
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.switch_to_clientes()
        except Exception as e:
            secao.rollback()
            messagebox.showerror("Erro", f"Erro ao cadastrar cliente: {e}")