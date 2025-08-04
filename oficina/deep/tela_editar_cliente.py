import customtkinter as ctk
import re
from datetime import datetime
from tkcalendar import Calendar
from tkinter import messagebox
from banco_de_dados_clientes import Cliente, secao

class TelaEditarCliente(ctk.CTkFrame):
    def __init__(self, master, cliente, switch_to_detalhes_cliente):
        super().__init__(master, fg_color="darkblue")
        self.master = master
        self.cliente = cliente  # Dicionário com os dados do cliente
        self.switch_to_detalhes_cliente = switch_to_detalhes_cliente
        
        self.criar_widgets()
        self.configurar_grid()
        self.preencher_campos()

    def configurar_grid(self):
        # Configuração responsiva do grid
        for i in range(14):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def criar_widgets(self):
        # Título
        self.titulo = ctk.CTkLabel(
            self,
            text="Editar Cliente",
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

        self.data_saida = ctk.CTkEntry(
            self,
            placeholder_text="Data de Saída (opcional)",
            font=('Century Gothic bold', 20),
            width=250,
            height=40,
            justify="center",
            corner_radius=45,
            border_width=3,
            border_color="black"
        )
        self.data_saida.grid(row=12, column=0, pady=5)  # Ajustado para nova posição
        self.data_saida.bind("<Button-1>", lambda e: self.abrir_calendario_saida(e))
        
        # Frame para botões (ajustado para nova posição)
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=13, column=0, pady=5)  # Ajustado para nova posição

        # Botão Voltar
        self.btn_voltar = ctk.CTkButton(
            self.frame_botoes,
            text="VOLTAR",
            corner_radius=70,
            font=('Century Gothic bold', 22),
            command=self.voltar
        )
        self.btn_voltar.grid(row=0, column=0, padx=10)

        # Botão Salvar
        self.btn_salvar = ctk.CTkButton(
            self.frame_botoes,
            text="SALVAR",
            corner_radius=70,
            font=('Century Gothic bold', 22),
            command=self.salvar_alteracoes
        )
        self.btn_salvar.grid(row=0, column=1)

    def preencher_campos(self):
        """Preenche os campos com os dados do cliente existente"""
        # Nome
        self.nome_cliente.insert(0, self.cliente['nome'])
        
        # CPF
        if self.cliente['cpf']:
            self.opcao_selecionada.set("SIM")
            self.entry_cpf.insert(0, self.cliente['cpf'])
            self.atualizar_interface()
        else:
            self.opcao_selecionada.set("NÃO")
            self.atualizar_interface()
        
        # Email
        if self.cliente['email']:
            self.email_cliente.insert(0, self.cliente['email'])
        
        # Telefone
        if self.cliente['telefone']:
            self.telefone.insert(0, self.cliente['telefone'])
        
        # Data de Entrada
        if self.cliente['data_entrada']:
            self.data_entrada.insert(0, self.cliente['data_entrada'].strftime("%Y-%m-%d"))
        
        # Valor
        if self.cliente['valor']:
            valor_formatado = f"R$ {self.cliente['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.valor.insert(0, valor_formatado)
        
        # Marca do Carro
        if self.cliente['marca_carro']:
            self.marca_carro.insert(0, self.cliente['marca_carro'])
        
        # Placa do Carro
        if self.cliente['placa_carro']:
            self.placa_carro.insert(0, self.cliente['placa_carro'])

        if self.cliente['data_saida']:
            self.data_saida.insert(0, self.cliente['data_saida'].strftime("%Y-%m-%d"))

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

    def abrir_calendario_saida(self, event):
        calendario_popup = ctk.CTkToplevel(self)
        calendario_popup.title("Selecione a Data de Saída")
        calendario_popup.geometry("300x300")
        calendario_popup.grab_set()  # Modal

        calendario = Calendar(calendario_popup, selectmode='day', date_pattern='yyyy-mm-dd')
        calendario.pack(padx=10, pady=10)

        def selecionar_data():
            data_selecionada = calendario.get_date()
            self.data_saida.delete(0, ctk.END)
            self.data_saida.insert(0, data_selecionada)
            calendario_popup.destroy()

        btn_confirmar = ctk.CTkButton(calendario_popup, text="Confirmar", command=selecionar_data)
        btn_confirmar.pack(pady=10)

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
            self.data_entrada.delete(0, ctk.END)
            self.data_entrada.insert(0, data_selecionada)
            calendario_popup.destroy()

        btn_confirmar = ctk.CTkButton(calendario_popup, text="Confirmar", command=selecionar_data)
        btn_confirmar.pack(pady=10)

    def salvar_alteracoes(self):
        """Salva as alterações feitas nos dados do cliente"""
        # Obter valores dos campos
        nome = self.nome_cliente.get().strip().upper()
        cpf = self.entry_cpf.get().strip() if self.opcao_selecionada.get() == "SIM" else None
        email = self.email_cliente.get().strip()
        telefone = self.telefone.get().strip()
        data_entrada = self.data_entrada.get().strip()
        valor_str = self.valor.get().strip()
        marca_carro = self.marca_carro.get().strip()
        placa_carro = self.placa_carro.get().strip()
        data_saida = self.data_saida.get().strip()

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
        
        
        if data_saida:
            try:
                data_saida = datetime.strptime(data_saida, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Erro", "A Data de Saída está em um formato inválido! Use o formato YYYY-MM-DD.")
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

        # Atualizar cliente no banco de dados
        try:
            cliente_atualizado = secao.query(Cliente).filter_by(id=self.cliente['id']).first()
            if cliente_atualizado:
                cliente_atualizado.nome = nome
                cliente_atualizado.cpf = cpf
                cliente_atualizado.email = email if email else None
                cliente_atualizado.telefone = telefone if telefone else None
                cliente_atualizado.data_entrada = data_entrada
                cliente_atualizado.valor = valor
                cliente_atualizado.marca_carro = marca_carro
                cliente_atualizado.placa_carro = placa_carro
                cliente_atualizado.data_saida = data_saida if data_saida else None
                # Não alteramos: forma_pagamento, data_saida, pecas_utilizadas nesta tela

                secao.commit()
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
                # Atualizar os dados do cliente para mostrar na tela de detalhes
                self.cliente = {
                    "id": cliente_atualizado.id,
                    "nome": cliente_atualizado.nome,
                    "cpf": cliente_atualizado.cpf,
                    "email": cliente_atualizado.email,
                    "telefone": cliente_atualizado.telefone,
                    "data_entrada": cliente_atualizado.data_entrada,
                    "valor": cliente_atualizado.valor,
                    "marca_carro": cliente_atualizado.marca_carro,
                    "placa_carro": cliente_atualizado.placa_carro,
                    "forma_pagamento": cliente_atualizado.forma_pagamento,
                    "data_saida": cliente_atualizado.data_saida,
                    "pecas_utilizadas": cliente_atualizado.pecas_utilizadas,
                }
                self.cliente['data_saida'] = cliente_atualizado.data_saida
                self.switch_to_detalhes_cliente(self.cliente)
            else:
                messagebox.showerror("Erro", "Cliente não encontrado no banco de dados!")
        except Exception as e:
            secao.rollback()
            messagebox.showerror("Erro", f"Erro ao atualizar cliente: {e}")

        

    def voltar(self):
        """Volta para a tela de detalhes do cliente sem salvar"""
        self.switch_to_detalhes_cliente(self.cliente)