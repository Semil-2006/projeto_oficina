from PIL import Image, ImageTk
from banco_de_dados_login import Usuario,session
import bcrypt
import re
from tkinter import messagebox, ttk
from definicoes import verificar_resposta,verificar_usuario_existe,cadastrar_usuario
from fpdf import FPDF
from tkinter import filedialog, Tk
import tkinter as tk
from banco_de_dados_de_servicos import Peca,seccao

from tkinter import Canvas, Scrollbar
from banco_de_dados_oficina_servicos import Servico, sessio
import customtkinter as ctk
from banco_de_dados_clientes import Cliente, secao
from tkcalendar import Calendar
from datetime import datetime
from collections import Counter


class Tela(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.imagem_de_inicio = None
        self.lb_imagem = None
        self.texto_de_boas_vindas = None
        self.ver_usuario = None
        self.ver_senha = None
        self.mostrar_senha = None
        self.frame_botoes = None
        self.botao_entrar = None
        self.botao_cadastrar = None
        self.texto_de_boas_vindas_cadastro = None
        self.texto = None
        self.criar_usuario = None
        self.criar_senha = None
        self.repetir_criar_senha = None
        self.pergunta_seguranca = None
        self.resposta_segurança = None
        self.botao_criar_conta = None
        self.botao_voltar = None
        self.opcoes = None
        self.tela_clientes()
        self.criar_tela_cadastro()
        self._configurar_tela()
        self.criar_tela_login()

    def _configurar_tela(self):
        largura = 450
        altura = 700
        self.geometry(f"{largura}x{altura}")
        self.minsize(largura, altura)
        self.resizable(True, True)
        self.configure(fg_color="darkblue")




    def criar_tela_login(self):
        self.limpar_tela()
        imagem = Image.open("img_do_carro.png").resize((250, 150))
        self.imagem_de_inicio = ImageTk.PhotoImage(imagem)

        self.lb_imagem = ctk.CTkLabel(self, image=self.imagem_de_inicio, text=None)
        self.lb_imagem.grid(row=1, column=0, padx=105, pady=(40, 10))

        self.texto_de_boas_vindas = ctk.CTkLabel(self,text="Seja Bem Vindo",font=('Century Gothic bold',32),
                                                 text_color="#FF0000")
        self.texto_de_boas_vindas.grid()


        self.ver_usuario = ctk.CTkEntry(self, placeholder_text="Usuario", justify="center",border_width=3,
                                        border_color="black",font=('Century Gothic bold',32), width=250,height=40,
                                        corner_radius=45)
        self.ver_usuario.grid(row=3, column=0, pady=(10, 10))

        self.ver_senha = ctk.CTkEntry(self, placeholder_text="Senha", justify="center", width=250, height=40,
                                      font=('Century Gothic bold',32), corner_radius=45,border_width=3,
                                      border_color="black",show="*")
        self.ver_senha.grid(row=4, column=0, pady=(10, 10))

        self.mostrar_senha = ctk.CTkCheckBox(
            self, text="Mostrar senha", width=250, font=("Arial", 20), text_color="white", corner_radius=30,
            border_color="black",border_width=3,
            command=lambda: self.ver_senha.configure(show="" if self.mostrar_senha.get() else "*"))
        self.mostrar_senha.grid( pady=(10, 40), padx=90, )



        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=6, column=0, pady=10)

        self.esqueci_senha_button = ctk.CTkButton(self, text="Esqueci minha senha", command=self.esqueceu_senha,
                                                       fg_color="transparent",
                                                       hover_color="#d1d1d1",
                                                       font=("Arial", 22),
                                                       text_color="blue",
                                                       anchor="center",
                                                       width=0
                                                       )
        self.esqueci_senha_button.grid(pady=15)

        self.botao_entrar = ctk.CTkButton(self.frame_botoes, text="Entrar", width=50, height=50,corner_radius=70,
                                          font=('Century Gothic bold',32), fg_color="white", text_color="gray", command=self.verificar_login)
        self.botao_entrar.grid(row=0, column=0, padx=8)

        self.botao_cadastrar = ctk.CTkButton(self.frame_botoes, text="Cadastrar", width=50, height=50,corner_radius=70,
                                             font=('Century Gothic bold',32),command=self.criar_tela_cadastro)
        self.botao_cadastrar.grid(row=0, column=1, padx=8)

        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)




    def criar_tela_cadastro(self):

        self.limpar_tela()

        self.texto_de_boas_vindas_cadastro = ctk.CTkLabel(self, text="Cadastro", font=('Century Gothic bold',42),
                                                          text_color="green")
        self.texto_de_boas_vindas_cadastro.grid(padx=120, pady=(40,0))

        self.texto = ctk.CTkLabel(self, text="--"*9,font=('Century Gothic bold',32),text_color="green")
        self.texto.grid()


        self.criar_usuario = ctk.CTkEntry(self, placeholder_text="Criar Usuario",font=('Century Gothic bold',26),
                                          width=250,height=40,justify="center",corner_radius=45,border_width=3,
                                          border_color="black")
        self.criar_usuario.grid(pady=(30,10))

        self.criar_senha = ctk.CTkEntry(self, placeholder_text="Criar Senha", font=('Century Gothic bold', 26),
                                          width=250, height=40, justify="center", corner_radius=45, border_width=3,
                                          border_color="black",show="*")
        self.criar_senha.grid()

        self.repetir_criar_senha = ctk.CTkEntry(self, placeholder_text="Repita a Senha", font=('Century Gothic bold', 26),
                                          width=250, height=40, justify="center", corner_radius=45, border_width=3,
                                          border_color="black",show="*")
        self.repetir_criar_senha.grid(pady=(10,15))

        self.mostrar_senha = ctk.CTkCheckBox(
            self, text="Mostrar senha", width=250, font=("Arial", 25), text_color="white", corner_radius=30,
            border_color="black", border_width=3,
            command=self.mostrar_senhas)
        self.mostrar_senha.grid( pady=(1,0) )

        self.opcoes = ["Qual estado você nasceu?", "Qual é o nome do seu melhor amigo?",
                  "Qual o nome do seu primeiro animal?"]
        self.pergunta_seguranca = ctk.CTkComboBox(self, values=self.opcoes, width=275, height=38,
                                              font=("Arial", 25), state="readonly")
        self.pergunta_seguranca.grid(padx=15, pady=15)

        self.resposta_segurança = ctk.CTkEntry(self, placeholder_text="Resposta", font=('Century Gothic bold', 26),
                                          width=250, height=40, justify="center", corner_radius=45, border_width=3,
                                          border_color="black")
        self.resposta_segurança.grid()



        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(pady=10)

        self.botao_criar_conta = ctk.CTkButton(
            self.frame_botoes,
            text="Criar conta",
            font=("Century Gothic bold", 30),
            corner_radius=460,
            command=lambda: cadastrar_usuario(
                self.criar_usuario,
                self.criar_senha,
                self.repetir_criar_senha,
                self.pergunta_seguranca,
                self.resposta_segurança,
                self.criar_tela_login
            )
        )
        self.botao_criar_conta.grid(row=0, column=0, padx=8)

        self.botao_voltar = ctk.CTkButton(self.frame_botoes,command=self.criar_tela_login, text="Voltar",font=("Century Gothic bold", 30),corner_radius=460)
        self.botao_voltar.grid(row=0, column=1,padx=8)

        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)




    def tela_clientes(self):
        self._configurar_tela()
        self.limpar_tela()
        self.cadastrar_clientes = ctk.CTkButton(self,text="Cadastrar cliente",font=("Century Gothic bold", 42),width=225,
                                                corner_radius=360,command=self.tela_cadastrar_clientes)
        self.cadastrar_clientes.grid(pady=(175,0),padx=30)
        self.ver_clientes = ctk.CTkButton(self,text="Ver Cliente",font=("Century Gothic bold", 42),width=400,corner_radius=360,command=self.criar_tela_ver_cliente)
        self.ver_clientes.grid(pady=(50,0))

    def criar_tela_entrar(self):
        self.limpar_tela()

        self.texto_de_boas_vindas = ctk.CTkLabel(self, text="Qual função deseja?", text_color="yellow",
                                                 font=("Century Gothic bold", 32))
        self.texto_de_boas_vindas.grid(padx=60, pady=(50,75))

        self.clientes = ctk.CTkButton(self, text="Clientes",font=("Century Gothic bold", 42),width=225,corner_radius=360, command=self.tela_clientes)
        self.clientes.grid(pady=(0,20))

        self.servicos = ctk.CTkButton(self, text="Serviços", font=("Century Gothic bold", 42), width=225,
                                     corner_radius=360, command=self.criar_tela_inicial)
        self.servicos.grid(pady=(0, 20))

        self.estoque = ctk.CTkButton(self, text="Estoque", font=("Century Gothic bold", 42),width=225,corner_radius=360,
                                     command=self.criar_tela_de_quando_entra_em_estoque)
        self.estoque.grid(pady=(0,20))

        self.relatorios = ctk.CTkButton(self, text="Relatorios", font=("Century Gothic bold", 42),width=225,corner_radius=360,command=self.criar_tela_de_escolha)
        self.relatorios.grid(pady=(0,20))

        self.botao_voltar = ctk.CTkButton(self, text="SAIR", font=("Century Gothic bold", 42), fg_color="red")
        self.botao_voltar.grid(pady=35)




    def abrir_calendario(self, event):
        calendario_popup = tk.Toplevel(self)
        calendario_popup.title("Selecione a Data")
        calendario_popup.geometry("300x300")

        calendario = Calendar(calendario_popup, selectmode='day', date_pattern='yyyy-mm-dd')
        calendario.pack(padx=10, pady=10)

        def selecionar_data():
            data_selecionada = calendario.get_date()
            self.data_de_entrada.delete(0, tk.END)
            self.data_de_entrada.insert(0, data_selecionada)
            calendario_popup.destroy()

        botao_confirmar = ctk.CTkButton(calendario_popup, text="Confirmar", command=selecionar_data)
        botao_confirmar.pack(pady=10)

    def abrir_calendariofim(self, event):
        calendario_popup = tk.Toplevel(self)
        calendario_popup.title("Selecione a Data")
        calendario_popup.geometry("300x300")

        calendario = Calendar(calendario_popup, selectmode='day', date_pattern='yyyy-mm-dd')
        calendario.pack(padx=10, pady=10)

        def selecionar_data():
            data_selecionada = calendario.get_date()
            self.data_de_saida.delete(0, tk.END)
            self.data_de_saida.insert(0, data_selecionada)
            calendario_popup.destroy()

        botao_confirmar = ctk.CTkButton(calendario_popup, text="Confirmar", command=selecionar_data)
        botao_confirmar.pack(pady=10)

    def atualizar_interface(self):
        opcao = self.opcao_selecionada.get()
        if opcao == "SIM":
            self.label_resposta.configure(text="Insira o CPF:")
            self.entry_cpf.grid(row=5)
        elif opcao == "NÃO":
            self.label_resposta.configure(text="")
            self.entry_cpf.grid_remove()

    def formatar_telefone(self, event=None):
        texto = self.telefone_para_contato.get()

        texto = ''.join(filter(str.isdigit, texto))
        if texto.startswith("55"):
            texto = texto[2:]
        texto = "55" + texto

        if len(texto) <= 2:
            texto_formatado = f"+{texto}"
        elif len(texto) <= 4:
            texto_formatado = f"+{texto[:2]} ({texto[2:]})"
        elif len(texto) <= 9:
            texto_formatado = f"+{texto[:2]} ({texto[2:4]}) {texto[4:]}"
        else:
            texto_formatado = f"+{texto[:2]} ({texto[2:4]}) {texto[4:9]}-{texto[9:13]}"

        self.telefone_para_contato.delete(0, ctk.END)
        self.telefone_para_contato.insert(0, texto_formatado)

    def formatar_placa(self, event):
        texto = self.placa_do_carro.get()

        texto = ''.join([char for char in texto if char.isalnum()])

        if len(texto) > 3:
            texto = texto[:3] + '-' + texto[3:7]
        elif len(texto) > 7:
            texto = texto[:7]

        self.placa_do_carro.delete(0, ctk.END)
        self.placa_do_carro.insert(0, texto)

    def cadastrar_clientee(self):
        nome = self.nome_do_clientes.get().strip().upper()
        cpf = self.entry_cpf.get().strip()
        email = self.email_do_cliente.get().strip()
        telefone = self.telefone_para_contato.get().strip()
        data_entrada = self.data_de_entrada.get().strip()
        valor = self.valor.get().strip()
        marca_carro = self.marca_do_carro.get().strip()
        placa_carro = self.placa_do_carro.get().strip()
        data_saida = None

        if valor:
            try:
                valor = float(valor.replace("R$", "").replace(".", "").replace(",", ".").strip())
            except ValueError:
                self.mostrar_erro("O campo Valor está em um formato inválido!")
                return
        else:
            valor = None

        try:
            data_entrada = datetime.strptime(data_entrada, "%Y-%m-%d").date()
        except ValueError:
            self.mostrar_erro("A Data de Entrada está em um formato inválido! Use o formato YYYY-MM-DD.")
            return

        if data_saida:
            try:
                data_saida = datetime.strptime(data_saida, "%Y-%m-%d").date()
            except ValueError:
                self.mostrar_erro("A Data de Saída está em um formato inválido! Use o formato YYYY-MM-DD.")
                return

        if not nome:
            self.mostrar_erro("O campo Nome do Cliente é obrigatório!")
            return
        if not data_entrada:
            self.mostrar_erro("O campo Data de Entrada é obrigatório!")
            return
        if not marca_carro:
            self.mostrar_erro("O campo Marca do Carro é obrigatório!")
            return
        if not placa_carro:
            self.mostrar_erro("O campo Placa do Carro é obrigatório!")
            return

        cliente_data = {
            "nome": nome,
            "cpf": cpf if cpf else None,
            "email": email if email else None,
            "telefone": telefone if telefone else None,
            "data_entrada": data_entrada,
            "valor": valor if valor else None,
            "marca_carro": marca_carro,
            "placa_carro": placa_carro,
            "forma_pagamento": None,
            "data_saida": None,
            "pecas_utilizadas": None
        }

        try:
            novo_cliente = Cliente(**cliente_data)
            secao.add(novo_cliente)
            secao.commit()
            self.mostrar_sucesso("Cliente cadastrado com sucesso!")
            self.criar_tela_entrar()
        except Exception as e:
            secao.rollback()
            self.mostrar_erro(f"Erro ao cadastrar cliente: {e}")

    def mostrar_erro(self, mensagem):
        messagebox.showerror("Erro", mensagem)

    def mostrar_sucesso(self, mensagem):
        messagebox.showinfo("Sucesso", mensagem)


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

    def tela_cadastrar_clientes(self):
        self.limpar_telaa()

        self.cadastrar_cliente = ctk.CTkLabel(self, text="Cadastrar Clientes", font=('Century Gothic bold', 32),
                                              text_color="green")
        self.cadastrar_cliente.grid(pady=(30, 2), padx=70)

        self.texto = ctk.CTkLabel(self, text="--" * 14
                                  , font=('Century Gothic bold', 32), text_color="green")
        self.texto.grid(pady=(0, 20))

        self.nome_do_clientes = ctk.CTkEntry(self, placeholder_text="Nome do Cliente", font=('Century Gothic bold', 20),
                                             width=250, height=40, justify="center", corner_radius=45, border_width=3,
                                             border_color="black")
        self.nome_do_clientes.grid(pady=(0, 5))

        self.incluir_na_nota = ctk.CTkLabel(self, text="CPF na nota", font=("Arial", 16), text_color="white")
        self.incluir_na_nota.grid(pady=(0, 5))

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(pady=5)

        self.opcao_selecionada = ctk.StringVar(value="")

        self.radio_sim = ctk.CTkRadioButton(
            self.frame_botoes, text="SIM", variable=self.opcao_selecionada,
            value="SIM", font=("Arial", 20), text_color="white",
            command=self.atualizar_interface
        )
        self.radio_sim.grid(row=0, column=0, padx=(60, 15))

        self.radio_nao = ctk.CTkRadioButton(
            self.frame_botoes, text="NÃO", variable=self.opcao_selecionada,
            value="NÃO", font=("Arial", 20), text_color="white",
            command=self.atualizar_interface
        )
        self.radio_nao.grid(row=0, column=1, padx=20)

        self.label_resposta = ctk.CTkLabel(self, text="", font=("Arial", 16), text_color="white", )
        self.label_resposta.grid(pady=5)

        self.entry_cpf = ctk.CTkEntry(self, placeholder_text="Digite seu CPF", font=('Century Gothic bold', 20),
                                      width=250, height=40, justify="center", corner_radius=45, border_width=3,
                                      border_color="black")
        self.entry_cpf.bind("<KeyRelease>", self.formatar_cpf)
        self.entry_cpf.grid_remove()

        self.email_do_cliente = ctk.CTkEntry(self, placeholder_text="Email do Cliente",
                                             font=('Century Gothic bold', 20),
                                             width=250, height=40, justify="center", corner_radius=45, border_width=3,
                                             border_color="black")
        self.email_do_cliente.grid(pady=5)

        self.telefone_para_contato = ctk.CTkEntry(self, placeholder_text="Telefone de Contato",
                                                  font=('Century Gothic bold', 20),
                                                  width=250, height=40, justify="center", corner_radius=45,
                                                  border_width=3,
                                                  border_color="black")
        self.telefone_para_contato.grid(pady=5)
        self.telefone_para_contato.bind("<KeyRelease>", self.formatar_telefone)

        self.data_de_entrada = ctk.CTkEntry(self, placeholder_text="Data de Entrada", font=('Century Gothic bold', 20),
                                            width=250, height=40, justify="center", corner_radius=45, border_width=3,
                                            border_color="black")
        self.data_de_entrada.grid(pady=5)
        self.data_de_entrada.bind("<Button-1>", self.abrir_calendario)

        self.calendario = None

        self.valor = ctk.CTkEntry(self, placeholder_text="Valor", font=('Century Gothic bold', 20),
                                  width=250, height=40, justify="center", corner_radius=45, border_width=3,
                                  border_color="black")
        self.valor.grid(pady=5)

        self.valor.bind("<KeyRelease>", self.formatar_valor)

        self.marca_do_carro = ctk.CTkEntry(self, placeholder_text="Marca do carro", font=('Century Gothic bold', 20),
                                           width=250, height=40, justify="center", corner_radius=45, border_width=3,
                                           border_color="black")
        self.marca_do_carro.grid(pady=5)

        self.placa_do_carro = ctk.CTkEntry(self, placeholder_text="Placa do carro", font=('Century Gothic bold', 20),
                                           width=250, height=40, justify="center", corner_radius=45, border_width=3,
                                           border_color="black")
        self.placa_do_carro.grid(pady=5)
        self.placa_do_carro.bind('<KeyRelease>', self.formatar_placa)

        # self.opcoes_de_pagamento = ["CRÉDITO", "DÉBITO", "PIX", "DINHEIRO EM ESPÉCIE", "AINDA NÃO PAGO"]
        # self.pagamento = ctk.CTkComboBox(self, values=self.opcoes_de_pagamento, width=275, height=38,
        #                                  font=("Century Gothic bold", 25), state="readonly")
        # self.pagamento.grid(pady=5)

        """Inicialmente não obrigatorio"""

        # self.data_de_saida = ctk.CTkEntry(self, placeholder_text="Data de Saida",font=('Century Gothic bold',20),
        #                                   width=250,height=40,justify="center",corner_radius=45,border_width=3,
        #                                   border_color="black")
        # self.data_de_saida.grid(pady=5)
        # self.data_de_saida.bind("<Button-1>", self.abrir_calendariofim)

        self.frame_botoess = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoess.grid(pady=5)

        self.botao_voltar = ctk.CTkButton(self.frame_botoess, text="VOLTAR", corner_radius=70,
                                          font=('Century Gothic bold', 22),command=self.tela_clientes)
        self.botao_voltar.grid(row=0, column=0, padx=10)

        self.botao_cadastrar = ctk.CTkButton(self.frame_botoess, text="CADASTRAR", corner_radius=70,
                                             font=('Century Gothic bold', 22), command=self.cadastrar_clientee)
        self.botao_cadastrar.grid(row=0, column=1)

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



    def tela_de_pergunta(self):
        self.limpar_tela()

        usuario = self.ver_usuario.get().strip().upper()

        usuario_encontrado = session.query(Usuario).filter_by(nome_usuario=usuario).first()

        if usuario_encontrado:
            pergunta = usuario_encontrado.pergunta_seguranca
            self.texto_pergunta = ctk.CTkLabel(self, text=f"Pergunta: {pergunta}",
                                               font=('Century Gothic bold', 18), text_color="blue")
            self.texto_pergunta.grid(row=0, column=0, padx=20, pady=(50, 20), columnspan=2)


            self.resposta = ctk.CTkEntry(self, placeholder_text="Resposta", justify="center", border_width=2,
                                         border_color="black", font=('Century Gothic bold', 24), width=250, height=40,
                                         corner_radius=45)
            self.resposta.grid(row=1, column=0, columnspan=2, padx=50, pady=15)

            self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
            self.frame_botoes.grid(row=2, column=0, columnspan=2, pady=30)

            self.botao_voltar = ctk.CTkButton(self.frame_botoes, command=self.criar_tela_login, text="Voltar", width=120)
            self.botao_voltar.grid(row=0, column=0, padx=8, pady=10)

            self.botao_continuar = ctk.CTkButton(
                self.frame_botoes,
                text="Confirmar",
                command=lambda: verificar_resposta(
                    self.ver_usuario,
                    self.resposta,
                    self.tela_de_sucesso
                ),
                width=120
            )
            self.botao_continuar.grid(row=0, column=1, padx=8, pady=10)

            self.frame_botoes.grid_columnconfigure(0, weight=1)
            self.frame_botoes.grid_columnconfigure(1, weight=1)

        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")


    def tela_de_sucesso(self):
        self.limpar_tela()
        self.texto_sucesso = ctk.CTkLabel(self, text="Senha recuperada com sucesso!", font=('Century Gothic bold', 22),
                                          text_color="green")
        self.texto_sucesso.grid(row=0, column=0, padx=20, pady=(100, 20), columnspan=2)

        self.botao_voltar = ctk.CTkButton(self, command=self.criar_tela_login, text="Voltar ao login", width=200)
        self.botao_voltar.grid(row=1, column=0, columnspan=2, pady=20)



    def esqueceu_senha(self):
        self.limpar_tela()
        self.texto_de_boas_vindas_esqueci = ctk.CTkLabel(self, text="Vamos recuperar sua senha!",
                                                         font=('Century Gothic bold',22), text_color="green")
        self.texto_de_boas_vindas_esqueci.grid(pady=(260,20))
        self.ver_usuario = ctk.CTkEntry(self, placeholder_text="Usuario", justify="center",border_width=3,
                                        border_color="black",font=('Century Gothic bold',32), width=250,height=40,
                                        corner_radius=45)
        self.ver_usuario.grid(padx=75)

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=6, column=0, pady=10)
        self.botao_voltar = ctk.CTkButton(self.frame_botoes, command=self.criar_tela_login, text="Voltar")
        self.botao_voltar.grid(padx=8,row=0, column=0)

        self.botao_continuar = ctk.CTkButton(
            self.frame_botoes,
            text="Continuar",
            command=lambda: verificar_usuario_existe(
                self.ver_usuario,
                self.tela_de_pergunta
            )
        )
        self.botao_continuar.grid(padx=8, row=0, column=1)

        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)

    def verificar_login(self):
        usuario = self.ver_usuario.get().strip().upper()
        senha = self.ver_senha.get().strip()

        if not usuario and not senha:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        if not usuario:
            messagebox.showerror("Erro", "O campo 'Usuário' deve ser preenchido.")
            return

        if not senha:
            messagebox.showerror("Erro", "O campo 'Senha' deve ser preenchido.")
            return

        usuario_encontrado = session.query(Usuario).filter_by(nome_usuario=usuario).first()

        if usuario_encontrado:
            senha_armazenada = usuario_encontrado.senha

            if isinstance(senha_armazenada, str):
                senha_armazenada = senha_armazenada.encode('utf-8')

            if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada):
                self.criar_tela_entrar()
            else:
                messagebox.showerror("Erro", "Senha incorreta. Tente novamente.")
        else:
            messagebox.showerror("Erro", "Usuário não existe.")

    def mostrar_senhas(self):
        show = "" if self.mostrar_senha.get() else "*"
        self.criar_senha.configure(show=show)
        self.repetir_criar_senha.configure(show=show)


    def limpar_telaa(self):
        for widget in self.winfo_children():
            widget.destroy()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.grid_forget()

    def atualizar_lista_clientes(self):
        busca = self.search_var.get().strip()
        self.clientes = self.obter_clientes(busca=busca)
        self.pagina_atual = 0
        self.mostrar_clientes_na_tela()

    def criar_tela_ver_cliente(self):
        self.geometry("741x700")
        self.limpar_tela()

        self.search_var = ctk.StringVar()
        entry_search = ctk.CTkEntry(self, textvariable=self.search_var,
                                    placeholder_text="Buscar por nome ou sobrenome...",
                                    width=500, font=('Century Gothic', 15))
        entry_search.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        btn_search = ctk.CTkButton(self, text="Buscar", command=self.atualizar_lista_clientes,
                                   font=('Century Gothic bold', 15))
        btn_search.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.frame_scrollable = ctk.CTkScrollableFrame(self, width=720, height=489)
        self.frame_scrollable.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.btn_anterior = ctk.CTkButton(self, text="Anterior", command=self.carregar_pagina_anterior,
                                          font=('Century Gothic bold', 15))
        self.btn_anterior.grid(row=2, column=0, pady=10, sticky="w")

        self.btn_proximo = ctk.CTkButton(self, text="Próximo", command=self.carregar_proxima_pagina,
                                         font=('Century Gothic bold', 15))
        self.btn_proximo.grid(row=2, column=1, pady=10, sticky="e")

        self.btn_voltar = ctk.CTkButton(self, text="Voltar",corner_radius=70,
                                             font=('Century Gothic bold',22), command=self.tela_clientes)
        self.btn_voltar.grid(padx=30)

        self.clientes = []
        self.pagina_atual = 0
        self.resultados_por_pagina = 10

        # Atualiza a lista inicial
        self.atualizar_lista_clientes()

    def atualizar_lista_clientes(self):
        busca = self.search_var.get().strip()
        self.clientes = self.obter_clientes(busca=busca)
        self.pagina_atual = 0
        self.mostrar_clientes_na_tela()

    def mostrar_clientes_na_tela(self):
        for widget in self.frame_scrollable.winfo_children():
            widget.destroy()


        headers = ["Nome", "Data Entrada", "Marca do Carro", "Placa do Carro", "Está Pago"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.frame_scrollable, text=header, width=120, fg_color="#A9A9A9",
                                 text_color="white",
                                 font=('Century Gothic bold', 15))
            label.grid(row=0, column=col, padx=5, pady=5)

        inicio = self.pagina_atual * self.resultados_por_pagina
        fim = inicio + self.resultados_por_pagina
        clientes_pagina = self.clientes[inicio:fim]

        for row, cliente in enumerate(clientes_pagina, start=1):
            btn_nome = ctk.CTkButton(self.frame_scrollable, text=cliente["nome"], width=120,
                                     command=lambda c=cliente: self.mostrar_detalhes_cliente(c),
                                     font=('Century Gothic bold', 20))
            btn_nome.grid(row=row, column=0, padx=5, pady=5)

            ctk.CTkLabel(self.frame_scrollable, text=str(cliente["data_entrada"] or "Não informado"),
                         font=('Century Gothic bold', 17)).grid(row=row, column=1, padx=5, pady=5)
            ctk.CTkLabel(self.frame_scrollable, text=cliente["marca_carro"] or "Não informado",
                         font=('Century Gothic bold', 17)).grid(row=row, column=2, padx=5, pady=5)
            ctk.CTkLabel(self.frame_scrollable, text=cliente["placa_carro"] or "Não informado",
                         font=('Century Gothic bold', 17)).grid(row=row, column=3, padx=5, pady=5)
            ctk.CTkLabel(self.frame_scrollable, text="Sim" if cliente["valor"] else "Não",
                         font=('Century Gothic bold', 17)).grid(row=row, column=4, padx=5, pady=5)

        self.btn_anterior.configure(state="normal" if self.pagina_atual > 0 else "disabled")
        if fim >= len(self.clientes):
            self.btn_proximo.configure(state="disabled")
        else:
            self.btn_proximo.configure(state="normal")

    def carregar_pagina_anterior(self):
        if self.pagina_atual > 0:
            self.pagina_atual -= 1
            self.mostrar_clientes_na_tela()

    def carregar_proxima_pagina(self):
        if (self.pagina_atual + 1) * self.resultados_por_pagina < len(self.clientes):
            self.pagina_atual += 1
            self.mostrar_clientes_na_tela()

    def mostrar_detalhes_cliente(self, cliente):
        self.limpar_tela()
        self._configurar_tela()

        detalhes = [
            f"Nome: {cliente['nome']}",
            f"CPF: {cliente['cpf'] or 'Não informado'}",
            f"E-mail: {cliente['email'] or 'Não informado'}",
            f"Telefone: {cliente['telefone'] or 'Não informado'}",
            f"Data Entrada: {cliente['data_entrada'] or 'Não informado'}",
            f"Valor: R${cliente['valor'] or 'Não informado'}",
            f"Marca do Carro: {cliente['marca_carro'] or 'Não informado'}",
            f"Placa do Carro: {cliente['placa_carro'] or 'Não informado'}",
            f"Forma de Pagamento: {cliente['forma_pagamento'] or 'Não informado'}",
            f"Data Saída: {cliente['data_saida'] or 'Não informado'}",
            f"Peças Utilizadas: {cliente['pecas_utilizadas'] or 'Não informado'}",
        ]

        for i, texto in enumerate(detalhes):
            label = ctk.CTkLabel(self, text=texto, anchor="w", width=700)
            label.grid(row=i, column=0, columnspan=2, padx=10, pady=2, sticky="w")

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=12, column=0, pady=10)

        btn_imprimir = ctk.CTkButton(
            self.frame_botoes,
            text="Imprimir",
            command=lambda: self.imprimir_orcamento(cliente)
        )
        btn_imprimir.grid(row=0, column=0)

        btn_voltar = ctk.CTkButton(self.frame_botoes, text="Editar")
        btn_voltar.grid(row=0, column=1)

        self.btn_voltar = ctk.CTkButton(self, text="Voltar", command=self.criar_tela_ver_cliente)
        self.btn_voltar.grid(padx=30)

    def imprimir_orcamento(self, cliente):
        gerar_pdf(cliente)

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def obter_clientes(self, busca=""):
        query = secao.query(Cliente)
        if busca:
            query = query.filter(Cliente.nome.ilike(f"%{busca}%"))

        query = query.order_by(Cliente.data_entrada.desc())

        clientes_query = query.all()
        clientes = [
            {
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

        secao.close()
        return clientes

    def criar_tela_de_quando_entra_em_estoque(self):
        self.limpar_tela()
        self.texto_de_estoque = ctk.CTkLabel(self,text="Estoque",text_color="yellow",
                                                 font=("Century Gothic bold", 52))
        self.texto_de_estoque.grid(padx=120,pady=(60,20))

        self.btn_cadastrar_pecas = ctk.CTkButton(self, text="Adicionar Peças",font=("Century Gothic bold", 42),width=225,
                                                 corner_radius=360,command=self.criar_tela_de_cadastrar_pecas)
        self.btn_cadastrar_pecas.grid(pady=(0,20))

        self.btn_ver_estoque = ctk.CTkButton(self,text="Ver Estoque",font=("Century Gothic bold", 42),width=365,
                                             corner_radius=360,command=self.criar_tela_de_estoque)
        self.btn_ver_estoque.grid()

        self.btn_voltar = ctk.CTkButton(self,text="Voltar",font=("Century Gothic bold", 42),width=225,
                                        corner_radius=360,command=self.criar_tela_entrar)
        self.btn_voltar.grid(pady=60)

    def validar_entrada(self, event):
        texto_atual = self.qtdd_dessa_peca.get()

        if not all(c.isdigit() for c in texto_atual):
            self.qtdd_dessa_peca.delete(0, "end")
            self.qtdd_dessa_peca.insert(0, texto_atual[:-1])

    def criar_tela_de_cadastrar_pecas(self):
        self.limpar_tela()
        self.texto_de_cadastro = ctk.CTkLabel(self, text="Cadastrar Peças", text_color="yellow",
                                              font=("Century Gothic bold", 42))
        self.texto_de_cadastro.grid(padx=60, pady=(70, 50))

        self.nome_da_peca = ctk.CTkEntry(self, placeholder_text="Nome Da Peça", justify="center", border_width=2,
                                         border_color="black", font=('Century Gothic bold', 24), width=400, height=60,
                                         corner_radius=45)
        self.nome_da_peca.grid(pady=(0,20))

        self.qtdd_dessa_peca = ctk.CTkEntry(self, placeholder_text="Quantidade Dessa Peça", justify="center",
                                            border_width=2,border_color="black", font=('Century Gothic bold', 24),
                                            width=400, height=60,corner_radius=45)
        self.qtdd_dessa_peca.grid()
        self.qtdd_dessa_peca.bind("<KeyRelease>", self.validar_entrada)

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=4, column=0, columnspan=2, pady=50)

        self.btn_voltar = ctk.CTkButton(self.frame_botoes, text="Voltar",font=("Century Gothic bold", 25),width=200,
                                        corner_radius=360,command=self.criar_tela_de_quando_entra_em_estoque)
        self.btn_voltar.grid(row=0, column=1, padx=20)

        self.btn_cadastrar_pecas = ctk.CTkButton(self.frame_botoes, text="Cadastrar", font=("Century Gothic bold", 25), width=200,
                                        corner_radius=360,command=self.cadastrar_peca)
        self.btn_cadastrar_pecas.grid(row=0, column=0)

    def cadastrar_peca(self):
        nome = self.nome_da_peca.get()
        try:
            quantidade = int(self.qtdd_dessa_peca.get())
        except ValueError:
            self.mostrar_erro("O campo Quantidade deve ser um número inteiro!")
            return

        if not nome:
            self.mostrar_erro("O campo Nome Da Peça é obrigatório!")
            return

        pecas = {"nome": nome, "quantidade": quantidade}

        try:
            nova_pecas = Peca(**pecas)
            session.add(nova_pecas)
            session.commit()
            self.mostrar_sucesso("Peça cadastrada com sucesso!")
            self.criar_tela_de_quando_entra_em_estoque()
        except Exception as e:
            session.rollback()
            self.mostrar_erro(f"Erro ao cadastrar peça: {e}")
            self.nome_da_peca.delete(0, 'end')
            self.qtdd_dessa_peca.delete(0, 'end')
    def mostrar_erro(self, mensagem):
        messagebox.showerror("Erro", mensagem)

    def mostrar_sucesso(self, mensagem):
        messagebox.showinfo("Sucesso", mensagem)

    def criar_tela_de_estoque(self):
        self.limpar_telaa()
        texto_de_estoque = ctk.CTkLabel(self, text="Vamos ver seu estoque", text_color="yellow",
                                        font=("Century Gothic bold", 22))
        texto_de_estoque.grid(padx=10, pady=(60, 20))

        pecas = seccao.query(Peca).all()

        def editar_quantidade(peca):
            def salvar_quantidade():
                nova_quantidade = quantidade_entry.get()
                if nova_quantidade.isdigit():
                    peca.quantidade = int(nova_quantidade)
                    seccao.commit()
                    edit_window.destroy()
                    atualizar_tabela()
                else:
                    print("Quantidade inválida")

            edit_window = ctk.CTkToplevel(self)
            edit_window.title(f"Editar Quantidade de {peca.nome}")
            ctk.CTkLabel(edit_window, text="Nova Quantidade:").pack(pady=50)
            edit_window.geometry("400x500")
            quantidade_entry = ctk.CTkEntry(edit_window)
            quantidade_entry.insert(0, str(peca.quantidade))
            quantidade_entry.pack(pady=10)
            ctk.CTkButton(edit_window, text="Salvar", command=salvar_quantidade).pack(pady=20)

        def atualizar_tabela(lista_pecas=None):
            if lista_pecas is None:
                lista_pecas = pecas

            for widget in frame_tabela.winfo_children():
                widget.destroy()

            for i, peca in enumerate(lista_pecas):
                nome_label = ctk.CTkLabel(frame_tabela, text=peca.nome, font=("Arial", 16), width=75)
                nome_label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
                quantidade_label = ctk.CTkLabel(frame_tabela, text=str(peca.quantidade), font=("Arial", 16), width=100)
                quantidade_label.grid(row=i, column=1, padx=5, pady=5, sticky="w")
                editar_button = ctk.CTkButton(frame_tabela, text="Editar", command=lambda p=peca: editar_quantidade(p))
                editar_button.grid(row=i, column=2, padx=10, pady=5)

            self.btn_voltar = ctk.CTkButton(self, text="VOLTAR",font=("Century Gothic bold", 42),width=225,
                                        corner_radius=360,command=self.criar_tela_de_quando_entra_em_estoque)
            self.btn_voltar.grid(pady=30)

        def filtrar_pecas(event=None):
            termo = barra_busca.get().lower()
            pecas_filtradas = [p for p in pecas if termo in p.nome.lower()]
            atualizar_tabela(pecas_filtradas)

        barra_busca = ctk.CTkEntry(self, placeholder_text="Buscar peça...")
        barra_busca.grid(padx=10, pady=10, sticky="we")
        barra_busca.bind("<KeyRelease>", filtrar_pecas)

        canvas = Canvas(self, bg="black", highlightthickness=0)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview, bg="white", troughcolor="black",
                              activebackground="gray")

        scrollable_frame = ctk.CTkFrame(canvas, fg_color="black")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=2, column=0, padx=2, pady=10, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")

        frame_tabela = ctk.CTkFrame(scrollable_frame, fg_color="black")
        frame_tabela.pack(fill="both", expand=True)

        atualizar_tabela()

    def criar_tela_inicial(self):
        self.limpar_tela()

        self.label = ctk.CTkLabel(self, text="Bem-vindo à tela de serviços",
                                  font=("Century Gothic bold", 24),
                                  text_color="yellow")
        self.label.pack(pady=(20, 10))

        self.botao_cadastrar = ctk.CTkButton(self, text="Cadastrar Serviço",
                                             font=("Century Gothic bold", 18),
                                             width=300, corner_radius=15,
                                             command=self.tela_cadastrar_servico)
        self.botao_cadastrar.pack(pady=10)

        self.botao_lista_servicos = ctk.CTkButton(self, text="Listar Serviços",
                                                  font=("Century Gothic bold", 18),
                                                  width=300, corner_radius=15,
                                                  command=self.tela_listar_servicos)
        self.botao_lista_servicos.pack(pady=10)

        self.botao_clientes_servicos = ctk.CTkButton(self, text="Clientes/Serviços",
                                                     font=("Century Gothic bold", 18),
                                                     width=300, corner_radius=15,
                                                     command=self.tela_clientes_servicos)
        self.botao_clientes_servicos.pack(pady=10)

        self.botao_sair = ctk.CTkButton(self, text="Voltar", font=("Century Gothic bold", 18),
                                        width=300, corner_radius=15,
                                        command=self.criar_tela_entrar)
        self.botao_sair.pack(pady=10)

    def tela_cadastrar_servico(self):
        self.limpar_tela()

        self.label_nome_servico = ctk.CTkLabel(self, text="Nome do Serviço",
                                               font=("Century Gothic bold", 18),
                                               text_color="white")
        self.label_nome_servico.pack(pady=10)

        self.entry_nome_servico = ctk.CTkEntry(self, placeholder_text="Digite o nome do serviço",
                                               justify="center", border_width=2,
                                               border_color="gray", font=("Century Gothic", 14),
                                               width=300, height=40, corner_radius=10)
        self.entry_nome_servico.pack(pady=10)

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.pack(pady=20)

        self.botao_voltar = ctk.CTkButton(self.frame_botoes, text="Voltar",
                                          font=("Arial", 14), command=self.criar_tela_inicial)
        self.botao_voltar.grid(row=0, column=0, padx=10)

        self.botao_cadastrar = ctk.CTkButton(self.frame_botoes, text="Cadastrar",
                                             font=("Arial", 14), command=self.salvar_servico)
        self.botao_cadastrar.grid(row=0, column=1, padx=10)

    def salvar_servico(self):
        nome_servico = self.entry_nome_servico.get().strip()

        if not nome_servico:
            self.mostrar_erro("O nome do serviço não pode estar vazio.")
            return

        try:
            novo_servico = Servico(nome=nome_servico)
            sessio.add(novo_servico)
            sessio.commit()
            self.mostrar_sucesso("Serviço cadastrado com sucesso!")
            self.criar_tela_inicial()
        except Exception as e:
            sessio.rollback()
            self.mostrar_erro(f"Erro ao cadastrar serviço: {e}")

    def tela_listar_servicos(self):
        self.limpar_tela()

        self.label_lista = ctk.CTkLabel(self, text="Serviços Cadastrados",
                                        font=("Century Gothic bold", 20),
                                        text_color="yellow")
        self.label_lista.pack(pady=10)

        frame_lista = ctk.CTkFrame(self)
        frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.treeview = ttk.Treeview(frame_lista, columns=("Nome"), show="headings", height=10, yscrollcommand=scrollbar.set)
        self.treeview.heading("Nome", text="Nome do Serviço")
        self.treeview.column("Nome", anchor="center")
        self.treeview.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.treeview.yview)

        self.carregar_servicos()

        self.botao_voltar = ctk.CTkButton(self, text="Voltar", font=("Century Gothic", 14),
                                          command=self.criar_tela_inicial)
        self.botao_voltar.pack(pady=10)

    def carregar_servicos(self):
        for servico in sessio.query(Servico).all():
            self.treeview.insert("", "end", values=(servico.nome,))


    def carregar_clientes_servicos(self):
        self.treeview.delete(*self.treeview.get_children())
        for cliente in secao.query(Cliente).all():
            self.treeview.insert("", "end", values=(
                cliente.nome, cliente.marca_carro, cliente.placa_carro, "Serviço Placeholder",
                cliente.pecas_utilizadas, cliente.valor
            ))

    def tela_clientes_servicos(self):
        self.limpar_tela()

        self.label = ctk.CTkLabel(self, text="Clientes e Serviços",
                                  font=("Century Gothic bold", 20),
                                  text_color="yellow")
        self.label.pack(pady=10)

        frame_lista = ctk.CTkFrame(self)
        frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        colunas = ("Nome do Cliente", "Marca do Carro", "Placa do Carro", "Serviços", "Peças Utilizadas", "Valor Cobrado")
        self.treeview = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=10, yscrollcommand=scrollbar.set)

        for coluna in colunas:
            self.treeview.heading(coluna, text=coluna)
            self.treeview.column(coluna, anchor="center")

        self.treeview.bind("<Double-1>", self.editar_cliente)
        self.treeview.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.treeview.yview)

        self.carregar_clientes_servicos()

        self.botao_voltar = ctk.CTkButton(self, text="Voltar", font=("Century Gothic", 14),
                                          command=self.criar_tela_inicial)
        self.botao_voltar.pack(pady=10)


    def editar_cliente(self, event):
        item_selecionado = self.treeview.selection()
        if not item_selecionado:
            return

        cliente_nome = self.treeview.item(item_selecionado, "values")[0]
        cliente = secao.query(Cliente).filter_by(nome=cliente_nome).first()
        if cliente:
            self.limpar_tela()
            self.label_editar = ctk.CTkLabel(self, text=f"Editar Cliente: {cliente.nome}",
                                             font=("Century Gothic bold", 18), text_color="yellow")
            self.label_editar.pack(pady=10)

            self.entry_nome = ctk.CTkEntry(self, placeholder_text="Nome",
                                           font=("Century Gothic", 14), width=300)
            self.entry_nome.insert(0, cliente.nome  )
            self.entry_nome.pack(pady=5)

            self.entry_marca_carro = ctk.CTkEntry(self, placeholder_text="Marca do Carro",
                                                 font=("Century Gothic", 14), width=300)
            self.entry_marca_carro.insert(0, cliente.marca_carro)
            self.entry_marca_carro.pack(pady=5)

            self.entry_placa_carro = ctk.CTkEntry(self, placeholder_text="Placa do Carro",
                                                 font=("Century Gothic", 14), width=300)
            self.entry_placa_carro.insert(0, cliente.placa_carro)
            self.entry_placa_carro.pack(pady=5)

            self.entry_pecas = ctk.CTkEntry(self, placeholder_text="Peças Utilizadas",
                                            font=("Century Gothic", 14), width=300)
            self.entry_pecas.insert(0, cliente.pecas_utilizadas or "Não informado")
            self.entry_pecas.pack(pady=5)

            self.entry_valor = ctk.CTkEntry(self, placeholder_text="Valor Cobrado",
                                            font=("Century Gothic", 14), width=300)
            self.entry_valor.insert(0, str(cliente.valor) or "Não informado")
            self.entry_valor.pack(pady=5)
            self.entry_valor.bind("<KeyRelease>", self.formatar_valor)
            self.botao_salvar = ctk.CTkButton(self, text="Salvar Alterações",
                                              font=("Century Gothic", 14),
                                              command=lambda: self.salvar_edicao(cliente))
            self.botao_salvar.pack(pady=10)

            self.botao_voltar = ctk.CTkButton(self, text="Voltar", font=("Century Gothic", 14),
                                              command=self.tela_clientes_servicos)
            self.botao_voltar.pack(pady=5)

    def formatar_valor(self, event):
        texto = self.entry_valor.get()

        if texto.startswith("R$"):
            texto = texto[2:]

        texto = ''.join(c for c in texto if c.isdigit())

        if not texto:
            texto = "0"

        valor = int(texto) / 100

        self.entry_valor.delete(0, ctk.END)
        self.entry_valor.insert(0, f"R${valor:,.2f}".replace(",", "."))  # Garantir ponto decimal

    def salvar_edicao(self, cliente):
        try:
            cliente.nome = self.entry_nome.get().strip()
            cliente.marca_carro = self.entry_marca_carro.get().strip()
            cliente.placa_carro = self.entry_placa_carro.get().strip()
            cliente.pecas_utilizadas = self.entry_pecas.get().strip()
            cliente.valor = float(self.entry_valor.get().strip())

            secao.commit()
            self.mostrar_sucesso("Cliente atualizado com sucesso!")
            self.tela_clientes_servicos()
        except Exception as e:
            secao.rollback()
            self.mostrar_erro(f"Erro ao salvar alterações: {e}")

    def mostrar_erro(self, mensagem):
        messagebox.showerror("Erro", mensagem)

    def mostrar_sucesso(self, mensagem):
        self.label_sucesso = ctk.CTkLabel(self, text=mensagem, text_color="green",
                                          font=("Century Gothic", 14))
        self.label_sucesso.pack(pady=(10, 0))
        self.after(3000, self.label_sucesso.destroy )


    def criar_tela_de_escolha(self):
        self.limpar_tela()
        self._configurar_tela()
        self.label_de_boas_vindas = ctk.CTkLabel(self, text="Escolha Qual Relatorio Deseja:", font=("Century Gothic bold", 24), text_color="yellow")
        self.label_de_boas_vindas.grid(padx=35, pady=30)

        self.btn_ver_relatorio_diario = ctk.CTkButton(self, text="Relatorio Diario", font=("Century Gothic bold", 24), command=self.abrir_calendario_diario)
        self.btn_ver_relatorio_diario.grid(pady=10)

        self.btn_ver_relatorio_mensal = ctk.CTkButton(self, text="Relatorio Mensal", font=("Century Gothic bold", 24), command=self.abrir_calendario_mensal)
        self.btn_ver_relatorio_mensal.grid(pady=10)

        self.btn_ver_relatorio_anual = ctk.CTkButton(self, text="Relatorio Anual", font=("Century Gothic bold", 24), command=self.abrir_calendario_anual)
        self.btn_ver_relatorio_anual.grid(pady=10)

        self.btn_voltar = ctk.CTkButton(self, text="Voltar", font=("Century Gothic bold", 24),command=self.criar_tela_entrar)
        self.btn_voltar.grid(pady=30)


    def abrir_calendario_diario(self):
        self.limpar_tela()
        self.label_data_atual = ctk.CTkLabel(self, text=f"Data Atual: {datetime.now().strftime('%Y-%m-%d')}",
                                             font=("Century Gothic bold", 18), text_color="yellow")
        self.label_data_atual.grid(padx=20, pady=10)

        self.calendario = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendario.grid(pady=10)

        self.btn_confirmar = ctk.CTkButton(self, text="Confirmar", font=("Century Gothic bold", 18),
                                           command=self.gerar_relatorio_diario)
        self.btn_confirmar.grid(pady=10)

        self.btn_voltar = ctk.CTkButton(self, text="Voltar", font=("Century Gothic bold", 18),
                                        command=self.criar_tela_de_escolha)
        self.btn_voltar.grid(pady=10)

    def gerar_relatorio_diario(self):
        data_selecionada = self.calendario.get_date()
        clientes = secao.query(Cliente).filter(Cliente.data_entrada == data_selecionada).all()

        self.limpar_tela()
        self.geometry("900x700")
        self.label_titulo = ctk.CTkLabel(self, text=f"Relatório Diário ({data_selecionada})",
                                         font=("Century Gothic bold", 18), text_color="yellow")
        self.label_titulo.grid(padx=20, pady=10)

        total_pago = 0
        total_pendente = 0
        for cliente in clientes:

            status_pagamento = "Pago" if cliente.forma_pagamento else "Pendente"
            valor_pago = cliente.valor if status_pagamento == "Pago" else 0
            valor_pendente = cliente.valor - valor_pago if status_pagamento == "Pendente" else 0

            status_saida = "Sim" if cliente.data_saida else "Não"

            total_pago += valor_pago
            total_pendente += valor_pendente

            info_cliente = (
                f"Nome: {cliente.nome}, Peças: {cliente.pecas_utilizadas}, "
                f"Carro: {cliente.marca_carro}, Placa: {cliente.placa_carro}, "
                f"Pagamento: {status_pagamento}, Saída: {status_saida}"
            )
            ctk.CTkLabel(self, text=info_cliente, font=("Century Gothic", 14), text_color="white").grid(padx=10, pady=5)

        resumo = f"Total Faturado: R$ {total_pago:.2f} | Total Pendente: R$ {total_pendente:.2f}"
        ctk.CTkLabel(self, text=resumo, font=("Century Gothic bold", 16), text_color="yellow").grid(padx=10, pady=20)

        self.btn_voltar = ctk.CTkButton(self, text="Voltar", font=("Century Gothic bold", 18),
                                        command=self.criar_tela_de_escolha)
        self.btn_voltar.grid(pady=10)

    def abrir_calendario_mensal(self):
        self.limpar_tela()
        self.label_data_atual = ctk.CTkLabel(self, text=f"Data Atual: {datetime.now().strftime('%Y-%m-%d')}",
                                             font=("Century Gothic bold", 18), text_color="yellow")
        self.label_data_atual.grid(padx=20, pady=10)

        self.calendario = Calendar(self, selectmode="day",
                                   date_pattern="yyyy-mm-dd")
        self.calendario.grid(pady=20)

        self.btn_confirmar = ctk.CTkButton(self, text="Confirmar", font=("Century Gothic bold", 18),
                                           command=self.gerar_relatorio_mensal)
        self.btn_confirmar.grid(pady=10)

        self.btn_voltar = ctk.CTkButton(self, text="Voltar", font=("Century Gothic bold", 18),
                                        command=self.criar_tela_de_escolha)
        self.btn_voltar.grid(pady=10)



    def gerar_relatorio_mensal(self):
        self.geometry("900x700")
        data_selecionada = self.calendario.get_date()
        ano, mes, _ = data_selecionada.split("-")

        clientes = secao.query(Cliente).filter(
            Cliente.data_entrada.like(f"{ano}-{mes}-%")
        ).all()

        self.limpar_tela()

        frame_scroll = self.criar_frame_com_scroll()

        label_titulo = ctk.CTkLabel(frame_scroll, text=f"Relatório Mensal ({mes}/{ano})",
                                    font=("Century Gothic bold", 18), text_color="yellow")
        label_titulo.grid(padx=20, pady=10)

        total_pago, total_pendente = 0, 0
        movimentacao_dias = Counter()

        for cliente in clientes:
            status_pagamento = "Pago" if cliente.forma_pagamento else "Pendente"
            valor_pago = cliente.valor or 0 if status_pagamento == "Pago" else 0
            valor_pendente = (cliente.valor or 0) - valor_pago if status_pagamento == "Pendente" else 0

            status_saida = "Sim" if cliente.data_saida else "Não"

            total_pago += valor_pago
            total_pendente += valor_pendente

            movimentacao_dias[cliente.data_entrada.day] += 1

            info_cliente = (
                f"Nome: {cliente.nome}, Peças: {cliente.pecas_utilizadas}, "
                f"Carro: {cliente.marca_carro}, Placa: {cliente.placa_carro}, "
                f"Pagamento: {status_pagamento}, Saída: {status_saida}"
            )
            ctk.CTkLabel(frame_scroll, text=info_cliente, font=("Century Gothic", 14), text_color="white").grid(padx=10,
                                                                                                                pady=5)

        dia_mais_movimentado = movimentacao_dias.most_common(1)[0] if movimentacao_dias else ("Nenhum", 0)
        resumo = (
            f"Total Faturado: R$ {total_pago:.2f} | Total Pendente: R$ {total_pendente:.2f}\n"
            f"Total Clientes: {len(clientes)} | Dia mais movimentado: {dia_mais_movimentado[0]} ({dia_mais_movimentado[1]} clientes)"
        )
        ctk.CTkLabel(frame_scroll, text=resumo, font=("Century Gothic bold", 16), text_color="yellow").grid(padx=10,
                                                                                                            pady=20)

        btn_voltar = ctk.CTkButton(frame_scroll, text="Voltar", font=("Century Gothic bold", 18),
                                   command=self.criar_tela_de_escolha)
        btn_voltar.grid(pady=10)

    def abrir_calendario_anual(self):
        self.limpar_tela()
        self.label_data_atual = ctk.CTkLabel(self, text=f"Data Atual: {datetime.now().strftime('%Y-%m-%d')}",
                                             font=("Century Gothic bold", 18), text_color="yellow")
        self.label_data_atual.grid(padx=20, pady=10)

        self.label_selecione_ano = ctk.CTkLabel(self, text="Selecione o Ano:", font=("Century Gothic bold", 16),
                                                text_color="white")
        self.label_selecione_ano.grid(padx=20, pady=10)

        # Adicionando Spinbox para selecionar o ano
        self.spinbox_ano = ctk.CTkEntry(self, width=100)
        self.spinbox_ano.insert(0, datetime.now().year)
        self.spinbox_ano.grid(pady=10)

        self.btn_confirmar = ctk.CTkButton(self, text="Confirmar", font=("Century Gothic bold", 18),
                                           command=self.gerar_relatorio_anual)
        self.btn_confirmar.grid(pady=10)

        self.btn_voltar = ctk.CTkButton(self, text="Voltar", font=("Century Gothic bold", 18),
                                        command=self.criar_tela_de_escolha)
        self.btn_voltar.grid(pady=10)

    def gerar_relatorio_anual(self):
        try:
            ano = int(self.spinbox_ano.get())
        except ValueError:
            self.limpar_tela()
            ctk.CTkLabel(self, text="Ano inválido. Por favor, insira um número.", font=("Century Gothic bold", 14),
                         text_color="red").grid(pady=10)
            btn_voltar = ctk.CTkButton(self, text="Voltar", font=("Century Gothic bold", 18),
                                       command=self.criar_tela_de_escolha)
            btn_voltar.grid(pady=10)
            return

        clientes = secao.query(Cliente).filter(
            Cliente.data_entrada.between(f"{ano}-01-01", f"{ano}-12-31")
        ).all()

        self.limpar_tela()
        self.geometry("900x700")

        frame_scroll = self.criar_frame_com_scroll()

        label_titulo = ctk.CTkLabel(frame_scroll, text=f"Relatório Anual ({ano})",
                                    font=("Century Gothic bold", 18), text_color="yellow")
        label_titulo.grid(padx=20, pady=10)

        total_pago, total_pendente = 0, 0
        movimentacao_meses = Counter()

        for cliente in clientes:
            status_pagamento = "Pago" if cliente.forma_pagamento else "Pendente"
            valor_pago = cliente.valor or 0 if status_pagamento == "Pago" else 0
            valor_pendente = (cliente.valor or 0) - valor_pago if status_pagamento == "Pendente" else 0

            status_saida = "Sim" if cliente.data_saida else "Não"

            total_pago += valor_pago
            total_pendente += valor_pendente

            movimentacao_meses[cliente.data_entrada.month] += 1

            info_cliente = (
                f"Nome: {cliente.nome}, Peças: {cliente.pecas_utilizadas}, "
                f"Carro: {cliente.marca_carro}, Placa: {cliente.placa_carro}, "
                f"Pagamento: {status_pagamento}, Saída: {status_saida}"
            )
            ctk.CTkLabel(frame_scroll, text=info_cliente, font=("Century Gothic", 14), text_color="white").grid(padx=10,
                                                                                                                pady=5)

        mes_mais_movimentado = movimentacao_meses.most_common(1)[0] if movimentacao_meses else ("Nenhum", 0)
        resumo = (
            f"Total Faturado: R$ {total_pago:.2f} | Total Pendente: R$ {total_pendente:.2f}\n"
            f"Total Clientes: {len(clientes)} | Mês mais movimentado: {mes_mais_movimentado[0]} ({mes_mais_movimentado[1]} clientes)"
        )
        ctk.CTkLabel(frame_scroll, text=resumo, font=("Century Gothic bold", 16), text_color="yellow").grid(padx=10,
                                                                                                            pady=20)

        btn_voltar = ctk.CTkButton(frame_scroll, text="Voltar", font=("Century Gothic bold", 18),
                                   command=self.criar_tela_de_escolha)
        btn_voltar.grid(pady=10)

    def criar_frame_com_scroll(self, largura=800, altura=600):

        canvas = ctk.CTkCanvas(self, bg="#2b2b2b", highlightthickness=0, width=largura, height=altura)
        scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=canvas.yview)

        frame_scroll = ctk.CTkFrame(canvas, fg_color="#2b2b2b")
        frame_scroll.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=frame_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return frame_scroll



def gerar_pdf(cliente):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    img_path = '/home/semil/Área de Trabalho/oficina/img_do_carro.png'
    img_width, img_height = 75.7, 39.4
    img_x = (pdf.w - img_width) / 2
    img_y = 50
    pdf.image(img_path, x=img_x, y=img_y, w=img_width, h=img_height)

    pdf.set_y(100)
    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)

    dados = [
        ("NOME", cliente['nome']),
        ("CPF", cliente['cpf'] or "Não informado"),
        ("EMAIL", cliente['email'] or "Não informado"),
        ("TELEFONE", cliente['telefone'] or "Não informado"),
        ("MARCA DO CARRO", cliente['marca_carro'] or "Não informado"),
        ("PLACA DO CARRO", cliente['placa_carro'] or "Não informado"),
        ("Peças Utilizadas", cliente['pecas_utilizadas'] or "Não informado"),
        ("Valor Total", f"R${cliente['valor']:.2f}" if cliente['valor'] else "Não informado"),
        ("Forma de Pagamento", cliente['forma_pagamento'] or "Não informado"),
    ]

    for campo, valor in dados:
        pdf.cell(50, 10, campo, border=1, align='L', fill=True)
        pdf.cell(0, 10, valor, border=1, ln=True, align='L')

    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(0, 10,
                   'Em caso de dúvidas, não hesite em nos contatar! Estamos à disposição para esclarecer qualquer questão e garantir que você tenha a melhor experiência com a PWS.')

    root = Tk()
    root.withdraw()
    caminho_arquivo = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        initialfile=f"{cliente['nome']}_orcamento.pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Salvar PDF"
    )
    if caminho_arquivo:
        pdf.output(caminho_arquivo)
        print(f"PDF salvo em: {caminho_arquivo}")
    else:
        print("Salvamento cancelado!")


class PDF(FPDF):
    def header(self):
        self.set_fill_color(59, 55, 126)
        self.rect(0, 0, self.w, self.h, 'F')
        self.set_font('Arial', 'I', 37)
        self.set_text_color(255, 255, 255)
        self.set_y(10)
        self.cell(0, 20, 'Orçamento - PWS DO IRMÃO', border=False, ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

class Ver_clientes(ctk.CTk):
    def imprimir_orcamento(self, cliente):
        gerar_pdf(cliente)



if __name__ == "__main__":
    tela = Tela()
    tela.mainloop()
