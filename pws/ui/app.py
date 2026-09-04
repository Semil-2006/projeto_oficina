"""Janela principal do Sistema de Gerenciamento para Oficina PWS.

A interface foi desacoplada da lógica: toda a regra de negócio vive em
``pws.services``, ``pws.validators`` e ``pws.formatadores``, que são
testáveis de forma unitária sem janela.
"""
from __future__ import annotations

import os
from datetime import datetime

import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from tkcalendar import Calendar

from pws.config import LOGO_PATH, get_relatorios_dir
from pws.database import database
from pws.formatadores import (
    formatar_cpf,
    formatar_placa,
    formatar_telefone,
    formatar_valor_entrada,
)
from pws.pdf import gerar_pdf_para_caminho
from pws.services.auth_service import AuthService
from pws.services.cliente_service import ClienteService
from pws.services.estoque_service import EstoqueService
from pws.services.relatorio_service import RelatorioService
from pws.services.servico_service import ServicoService


class Tela(ctk.CTk):
    """Janela principal que navega entre as telas do sistema."""

    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento - Oficina PWS")
        self.geometry("450x700")
        self.minsize(450, 700)
        self.configure(fg_color="darkblue")

        # Dependências (serviços) — injetáveis para testes.
        self.session_factory = database.session_factory()
        self.auth = AuthService(self.session_factory)
        self.clientes = ClienteService(self.session_factory)
        self.estoque = EstoqueService(self.session_factory)
        self.servicos = ServicoService(self.session_factory)
        self.relatorios = RelatorioService(self.session_factory)

        self._imagens = {}  # evita que PhotoImage seja coletado pelo GC.

        self.mostrar_login()

    # ------------------------------------------------------------------ UI #
    def limpar(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _rotulo_imagem(self, parent=None, largura=250, altura=150):
        if os.path.exists(LOGO_PATH):
            imagem = Image.open(LOGO_PATH).resize((largura, altura))
            foto = ImageTk.PhotoImage(imagem)
            self._imagens["logo"] = foto
            return ctk.CTkLabel(parent or self, image=foto, text=None)
        return ctk.CTkLabel(parent or self, text="PWS", font=("Century Gothic bold", 32))

    # ----------------------------------------------------------- AUTH UI #
    def mostrar_login(self):
        self.limpar()
        self._rotulo_imagem().grid(row=1, column=0, padx=105, pady=(40, 10))
        ctk.CTkLabel(
            self, text="Seja Bem Vindo", font=("Century Gothic bold", 32),
            text_color="#FF0000",
        ).grid(row=2, column=0, pady=5)

        self.ver_usuario = ctk.CTkEntry(
            self, placeholder_text="Usuario", justify="center", width=250,
            height=40, font=("Century Gothic bold", 20), corner_radius=45,
            border_width=3, border_color="black",
        )
        self.ver_usuario.grid(row=3, column=0, pady=(15, 10))

        self.ver_senha = ctk.CTkEntry(
            self, placeholder_text="Senha", justify="center", width=250,
            height=40, font=("Century Gothic bold", 20), corner_radius=45,
            border_width=3, border_color="black", show="*",
        )
        self.ver_senha.grid(row=4, column=0, pady=10)

        self.mostrar_senha_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            self, text="Mostrar senha", variable=self.mostrar_senha_var,
            command=self._toggle_senha, font=("Arial", 16),
            text_color="white", corner_radius=30, border_color="black",
            border_width=2,
        ).grid(row=5, column=0, pady=5)

        ctk.CTkButton(
            self, text="Esqueci minha senha", command=self.mostrar_esqueci_senha,
            fg_color="transparent", hover_color="#d1d1d1",
            font=("Arial", 18), text_color="blue", width=0,
        ).grid(row=6, column=0, pady=5)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=7, column=0, pady=15)
        ctk.CTkButton(
            frame, text="Entrar", width=110, height=40, corner_radius=40,
            font=("Century Gothic bold", 18), fg_color="white", text_color="gray",
            command=self.verificar_login,
        ).grid(row=0, column=0, padx=8)
        ctk.CTkButton(
            frame, text="Cadastrar", width=110, height=40, corner_radius=40,
            font=("Century Gothic bold", 18), command=self.mostrar_cadastro,
        ).grid(row=0, column=1, padx=8)

    def _toggle_senha(self):
        show = "" if self.mostrar_senha_var.get() else "*"
        self.ver_senha.configure(show=show)

    def verificar_login(self):
        try:
            self.usuario_logado = self.auth.autenticar(
                self.ver_usuario.get(), self.ver_senha.get()
            )
            self.mostrar_menu_principal()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def mostrar_cadastro(self):
        self.limpar()
        ctk.CTkLabel(
            self, text="Cadastro", font=("Century Gothic bold", 42),
            text_color="green",
        ).grid(padx=120, pady=(40, 0))
        ctk.CTkLabel(
            self, text="--" * 12, font=("Century Gothic bold", 24),
            text_color="green",
        ).grid()

        self.criar_usuario = self._entrada("Criar Usuario", 26)
        self.criar_usuario.grid(pady=(25, 10))
        self.criar_senha = self._entrada("Criar Senha", 26, show="*")
        self.criar_senha.grid()
        self.repetir_senha = self._entrada("Repita a Senha", 26, show="*")
        self.repetir_senha.grid(pady=(10, 10))

        opcoes = [
            "Qual estado você nasceu?",
            "Qual é o nome do seu melhor amigo?",
            "Qual o nome do seu primeiro animal?",
        ]
        self.pergunta_seguranca = ctk.CTkComboBox(
            self, values=opcoes, width=275, height=38,
            font=("Arial", 18), state="readonly",
        )
        self.pergunta_seguranca.grid(pady=10)
        self.resposta_seguranca = self._entrada("Resposta", 24)
        self.resposta_seguranca.grid()

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(pady=20)
        ctk.CTkButton(
            frame, text="Criar conta", font=("Century Gothic bold", 24),
            corner_radius=40, command=self.cadastrar_usuario,
        ).grid(row=0, column=0, padx=8)
        ctk.CTkButton(
            frame, text="Voltar", font=("Century Gothic bold", 24),
            corner_radius=40, command=self.mostrar_login,
        ).grid(row=0, column=1, padx=8)

    def _entrada(self, placeholder, tamanho=20, show=None):
        return ctk.CTkEntry(
            self, placeholder_text=placeholder, font=("Century Gothic bold", tamanho),
            width=250, height=40, justify="center", corner_radius=45,
            border_width=3, border_color="black", show=show,
        )

    def cadastrar_usuario(self):
        try:
            self.auth.cadastrar_usuario(
                self.criar_usuario.get(),
                self.criar_senha.get(),
                self.pergunta_seguranca.get(),
                self.resposta_seguranca.get(),
            )
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.mostrar_login()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def mostrar_esqueci_senha(self):
        self.limpar()
        ctk.CTkLabel(
            self, text="Vamos recuperar sua senha!", font=("Century Gothic bold", 24),
            text_color="green",
        ).grid(pady=(200, 25))
        self.ver_usuario = self._entrada("Usuario", 24)
        self.ver_usuario.grid(padx=75)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(pady=20)
        ctk.CTkButton(
            frame, text="Voltar", font=("Century Gothic bold", 20),
            command=self.mostrar_login,
        ).grid(row=0, column=0, padx=8)
        ctk.CTkButton(
            frame, text="Continuar", font=("Century Gothic bold", 20),
            command=self._verificar_usuario_recuperacao,
        ).grid(row=0, column=1, padx=8)

    def _verificar_usuario_recuperacao(self):
        usuario = self.ver_usuario.get().strip().upper()
        if not usuario:
            messagebox.showerror("Erro", "O campo 'Usuário' deve ser preenchido.")
            return
        if self.auth.verificar_existe(usuario):
            self.mostrar_pergunta()
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")

    def mostrar_pergunta(self):
        usuario = self.auth.buscar_usuario(self.ver_usuario.get().strip().upper())
        self.limpar()
        if not usuario:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            self.mostrar_login()
            return
        ctk.CTkLabel(
            self, text=f"Pergunta: {usuario.pergunta_seguranca}",
            font=("Century Gothic bold", 18), text_color="blue",
        ).grid(padx=20, pady=(80, 20))
        self.resposta = self._entrada("Resposta", 24)
        self.resposta.grid(padx=50)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(pady=30)
        ctk.CTkButton(
            frame, text="Voltar", width=120, command=self.mostrar_login,
        ).grid(row=0, column=0, padx=8)
        ctk.CTkButton(
            frame, text="Confirmar", width=120, command=self._verificar_resposta,
        ).grid(row=0, column=1, padx=8)

    def _verificar_resposta(self):
        try:
            ok = self.auth.verificar_resposta(
                self.ver_usuario.get().strip().upper(), self.resposta.get()
            )
            if ok:
                self.mostrar_redefinir_senha()
            else:
                messagebox.showerror("Erro", "Resposta incorreta.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def mostrar_redefinir_senha(self):
        self.limpar()
        ctk.CTkLabel(
            self, text="Redefinir Senha", font=("Century Gothic bold", 32),
            text_color="green",
        ).grid(pady=(80, 20))
        self.nova_senha = self._entrada("Nova Senha", 24, show="*")
        self.nova_senha.grid(pady=8)
        self.confirmar_nova_senha = self._entrada("Confirmar Nova Senha", 24, show="*")
        self.confirmar_nova_senha.grid(pady=8)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(pady=25)
        ctk.CTkButton(
            frame, text="Voltar", command=self.mostrar_login,
        ).grid(row=0, column=0, padx=8)
        ctk.CTkButton(
            frame, text="Redefinir", command=self._redefinir_senha,
        ).grid(row=0, column=1, padx=8)

    def _redefinir_senha(self):
        nova = self.nova_senha.get()
        confirma = self.confirmar_nova_senha.get()
        if nova != confirma:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
        try:
            self.auth.redefinir_senha(
                self.ver_usuario.get().strip().upper(), nova
            )
            messagebox.showinfo("Sucesso", "Senha redefinida com sucesso!")
            self.mostrar_login()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # -------------------------------------------------------- MENU PRINCIPAL #
    def mostrar_menu_principal(self):
        self.limpar()
        self.geometry("450x700")
        ctk.CTkLabel(
            self, text="Qual função deseja?", text_color="yellow",
            font=("Century Gothic bold", 32),
        ).grid(padx=60, pady=(50, 60))

        botoes = [
            ("Clientes", self.mostrar_menu_clientes),
            ("Serviços", self.mostrar_menu_servicos),
            ("Estoque", self.mostrar_menu_estoque),
            ("Relatórios", self.mostrar_menu_relatorios),
            ("Sair", self.quit),
        ]
        for i, (texto, comando) in enumerate(botoes):
            ctk.CTkButton(
                self, text=texto, font=("Century Gothic bold", 36),
                width=280, corner_radius=40, command=comando,
                fg_color="red" if texto == "Sair" else None,
            ).grid(pady=(0, 15))

    def _titulo(self, texto, cor="yellow"):
        self.limpar()
        self.geometry("450x700")
        ctk.CTkLabel(
            self, text=texto, font=("Century Gothic bold", 34), text_color=cor,
        ).grid(padx=20, pady=(40, 30))
        return self

    def _menu_botoes(self, botoes):
        for i, (texto, comando) in enumerate(botoes):
            ctk.CTkButton(
                self, text=texto, font=("Century Gothic bold", 26),
                width=280, corner_radius=40, command=comando,
            ).grid(pady=(0, 12))

    def mostrar_menu_clientes(self):
        self._titulo("Clientes")
        self._menu_botoes([
            ("Cadastrar Cliente", self.tela_cadastrar_cliente),
            ("Ver Clientes", self.tela_ver_clientes),
            ("Voltar", self.mostrar_menu_principal),
        ])

    def mostrar_menu_servicos(self):
        self._titulo("Serviços")
        self._menu_botoes([
            ("Cadastrar Serviço", self.tela_cadastrar_servico),
            ("Listar Serviços", self.tela_listar_servicos),
            ("Voltar", self.mostrar_menu_principal),
        ])

    def mostrar_menu_estoque(self):
        self._titulo("Estoque")
        self._menu_botoes([
            ("Adicionar Peças", self.tela_cadastrar_peca),
            ("Ver Estoque", self.tela_ver_estoque),
            ("Voltar", self.mostrar_menu_principal),
        ])

    def mostrar_menu_relatorios(self):
        self._titulo("Relatórios", cor="yellow")
        self._menu_botoes([
            ("Relatório Diário", self.abrir_calendario_diario),
            ("Relatório Mensal", self.abrir_calendario_mensal),
            ("Relatório Anual", self.tela_relatorio_anual),
            ("Voltar", self.mostrar_menu_principal),
        ])

    # ------------------------------------------------------------- CLIENTES #
    def tela_cadastrar_cliente(self):
        self._titulo("Cadastrar Cliente", cor="green")

        self.entry_nome = self._entrada("Nome do Cliente", 18)
        self.entry_nome.grid(pady=5)
        self.entry_cpf = self._entrada("CPF (opcional)", 18)
        self.entry_cpf.grid(pady=5)
        self.entry_cpf.bind("<KeyRelease>", self._mascara_cpf)
        self.entry_email = self._entrada("E-mail (opcional)", 18)
        self.entry_email.grid(pady=5)
        self.entry_telefone = self._entrada("Telefone (opcional)", 18)
        self.entry_telefone.grid(pady=5)
        self.entry_telefone.bind("<KeyRelease>", self._mascara_telefone)

        self.entry_data_entrada = self._entrada("Data de Entrada (AAAA-MM-DD)", 18)
        self.entry_data_entrada.grid(pady=5)
        self.entry_data_entrada.bind("<Button-1>", self._calendario_data_entrada)

        self.entry_valor = self._entrada("Valor (R$)", 18)
        self.entry_valor.grid(pady=5)
        self.entry_valor.bind("<KeyRelease>", self._mascara_valor)

        self.entry_marca = self._entrada("Marca do carro", 18)
        self.entry_marca.grid(pady=5)
        self.entry_placa = self._entrada("Placa do carro", 18)
        self.entry_placa.grid(pady=5)
        self.entry_placa.bind("<KeyRelease>", self._mascara_placa)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(pady=15)
        ctk.CTkButton(
            frame, text="VOLTAR", font=("Century Gothic bold", 20),
            command=self.mostrar_menu_clientes,
        ).grid(row=0, column=0, padx=10)
        ctk.CTkButton(
            frame, text="CADASTRAR", font=("Century Gothic bold", 20),
            command=self.cadastrar_cliente,
        ).grid(row=0, column=1, padx=10)

    def cadastrar_cliente(self):
        from pws.validators import converter_valor_para_float

        valor = None
        if self.entry_valor.get().strip():
            valor = converter_valor_para_float(self.entry_valor.get())
        data_entrada = self.entry_data_entrada.get().strip()
        try:
            from datetime import date

            data = datetime.strptime(data_entrada, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror(
                "Erro", "Data de Entrada inválida! Use o formato AAAA-MM-DD."
            )
            return

        try:
            self.clientes.criar_cliente(
                nome=self.entry_nome.get(),
                cpf=self.entry_cpf.get(),
                email=self.entry_email.get(),
                telefone=self.entry_telefone.get(),
                data_entrada=data,
                valor=valor,
                marca_carro=self.entry_marca.get(),
                placa_carro=self.entry_placa.get(),
            )
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.mostrar_menu_clientes()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _aplicar_mascara(self, entry, formatador):
        """Aplica uma máscara a um campo, sem atrapalhar o cursor.

        Só reescreve o conteúdo se o valor formatado for diferente do atual;
        assim, enquanto o usuário digita normalmente (sem o separador), o
        cursor não é reposicionado e a máscara aparece conforme a digitação.
        """
        atual = entry.get()
        if not atual:
            return
        formatado = formatador(atual)
        if formatado != atual:
            entry.delete(0, "end")
            entry.insert(0, formatado)
            entry.icursor("end")

    def _mascara_cpf(self, _event=None):
        self._aplicar_mascara(self.entry_cpf, formatar_cpf)

    def _mascara_telefone(self, _event=None):
        self._aplicar_mascara(self.entry_telefone, formatar_telefone)

    def _mascara_placa(self, _event=None):
        self._aplicar_mascara(self.entry_placa, formatar_placa)

    def _mascara_valor(self, _event=None):
        self._aplicar_mascara(self.entry_valor, formatar_valor_entrada)

    def _calendario_data_entrada(self, _event=None):
        popup = ctk.CTkToplevel(self)
        popup.title("Selecione a Data")
        popup.geometry("300x300")

        calendario = Calendar(popup, selectmode="day", date_pattern="yyyy-mm-dd")
        calendario.pack(pady=10)

        def confirmar():
            self.entry_data_entrada.delete(0, "end")
            self.entry_data_entrada.insert(0, calendario.get_date())
            popup.destroy()

        ctk.CTkButton(popup, text="Confirmar", command=confirmar).pack(pady=10)

    def tela_ver_clientes(self):
        self._titulo("Buscar Cliente", cor="green")
        self.geometry("780x700")

        self.search_var = ctk.StringVar()
        ctk.CTkEntry(
            self, textvariable=self.search_var, placeholder_text="Buscar por nome...",
            width=480, font=("Century Gothic", 15),
        ).grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
        ctk.CTkButton(
            self, text="Buscar", command=self._atualizar_lista_clientes,
            font=("Century Gothic bold", 15),
        ).grid(row=1, column=1, padx=5, pady=5)

        self.frame_lista = ctk.CTkScrollableFrame(self, width=760, height=460)
        self.frame_lista.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self._clientes_pagina_atual = 0
        self._clientes_por_pagina = 10
        self._clientes_cache = []

        ctk.CTkButton(
            self, text="Voltar", command=self.mostrar_menu_clientes,
            font=("Century Gothic bold", 20),
        ).grid(pady=10)
        self._atualizar_lista_clientes()

    def _atualizar_lista_clientes(self):
        clientes, _total = self.clientes.listar_clientes(
            busca=self.search_var.get(), pagina=self._clientes_pagina_atual,
            por_pagina=self._clientes_por_pagina,
        )
        self._clientes_cache = clientes
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        cabecalho = ["Nome", "Data", "Marca", "Placa", "Pago"]
        for col, texto in enumerate(cabecalho):
            ctk.CTkLabel(
                self.frame_lista, text=texto, width=120, fg_color="#A9A9A9",
                text_color="white", font=("Century Gothic bold", 14),
            ).grid(row=0, column=col, padx=3, pady=3)

        for linha, cliente in enumerate(clientes, start=1):
            ctk.CTkButton(
                self.frame_lista, text=cliente.nome, width=120,
                font=("Century Gothic bold", 16),
                command=lambda c=cliente: self.tela_detalhes_cliente(c),
            ).grid(row=linha, column=0, padx=3, pady=3)
            ctk.CTkLabel(
                self.frame_lista, text=str(cliente.data_entrada or "-"),
                font=("Century Gothic bold", 14),
            ).grid(row=linha, column=1, padx=3, pady=3)
            ctk.CTkLabel(
                self.frame_lista, text=cliente.marca_carro, font=("Century Gothic bold", 14),
            ).grid(row=linha, column=2, padx=3, pady=3)
            ctk.CTkLabel(
                self.frame_lista, text=cliente.placa_carro, font=("Century Gothic bold", 14),
            ).grid(row=linha, column=3, padx=3, pady=3)
            ctk.CTkLabel(
                self.frame_lista, text="Sim" if cliente.esta_pago() else "Não",
                font=("Century Gothic bold", 14),
            ).grid(row=linha, column=4, padx=3, pady=3)

    def tela_detalhes_cliente(self, cliente):
        self._titulo("Detalhes do Cliente", cor="green")
        dados = [
            ("Nome", cliente.nome),
            ("CPF", cliente.cpf or "Não informado"),
            ("E-mail", cliente.email or "Não informado"),
            ("Telefone", cliente.telefone or "Não informado"),
            ("Data Entrada", str(cliente.data_entrada or "Não informado")),
            ("Valor", f"R$ {cliente.valor or 0:.2f}".replace(".", ",") if cliente.valor else "Não informado"),
            ("Marca do Carro", cliente.marca_carro),
            ("Placa do Carro", cliente.placa_carro),
            ("Forma de Pagamento", cliente.forma_pagamento or "Não informado"),
            ("Data Saída", str(cliente.data_saida or "Não informado")),
            ("Peças Utilizadas", cliente.pecas_utilizadas or "Não informado"),
        ]
        for i, (campo, valor) in enumerate(dados):
            ctk.CTkLabel(
                self, text=f"{campo}: {valor}", anchor="w", width=700,
                font=("Century Gothic", 16),
            ).grid(row=i + 1, column=0, columnspan=2, padx=20, pady=3, sticky="w")

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=len(dados) + 2, column=0, pady=15)
        ctk.CTkButton(
            frame, text="Imprimir", command=lambda: self.imprimir_orcamento(cliente),
        ).grid(row=0, column=0, padx=8)
        ctk.CTkButton(
            frame, text="Voltar", command=self.tela_ver_clientes,
        ).grid(row=0, column=1, padx=8)

    def imprimir_orcamento(self, cliente):
        dados = self.clientes.para_dict(cliente)
        caminho = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=f"{cliente.nome}_orcamento.pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Salvar PDF",
        )
        if caminho:
            try:
                gerar_pdf_para_caminho(dados, caminho)
                messagebox.showinfo("Sucesso", f"Orçamento salvo em: {caminho}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao gerar PDF: {e}")

    # ------------------------------------------------------------- SERVIÇOS #
    def tela_cadastrar_servico(self):
        self._titulo("Cadastrar Serviço", cor="green")
        self.entry_servico = self._entrada("Nome do Serviço", 20)
        self.entry_servico.grid(pady=30)
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(pady=25)
        ctk.CTkButton(
            frame, text="Voltar", command=self.mostrar_menu_servicos,
        ).grid(row=0, column=0, padx=8)
        ctk.CTkButton(
            frame, text="Cadastrar", command=self._salvar_servico,
        ).grid(row=0, column=1, padx=8)

    def _salvar_servico(self):
        try:
            self.servicos.criar_servico(self.entry_servico.get())
            messagebox.showinfo("Sucesso", "Serviço cadastrado com sucesso!")
            self.mostrar_menu_servicos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def tela_listar_servicos(self):
        self._titulo("Serviços Cadastrados", cor="green")
        servicos = self.servicos.listar_servicos()
        frame = ctk.CTkScrollableFrame(self, width=400, height=400)
        frame.grid(pady=10)
        for servico in servicos:
            linha = ctk.CTkFrame(frame, fg_color="transparent")
            linha.pack(fill="x", padx=5, pady=2)
            ctk.CTkLabel(
                linha, text=servico.nome, font=("Century Gothic bold", 18),
            ).pack(side="left", padx=10)
            ctk.CTkButton(
                linha, text="Excluir", width=80,
                command=lambda s=servico: self._excluir_servico(s),
            ).pack(side="right")
        if not servicos:
            ctk.CTkLabel(self, text="Nenhum serviço cadastrado.", font=("Century Gothic", 16)).grid()
        ctk.CTkButton(
            self, text="Voltar", font=("Century Gothic bold", 20),
            command=self.mostrar_menu_servicos,
        ).grid(pady=10)

    def _excluir_servico(self, servico):
        try:
            self.servicos.excluir_servico(servico.id)
            messagebox.showinfo("Sucesso", "Serviço excluído!")
            self.tela_listar_servicos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ---------------------------------------------------------------- ESTOQUE #
    def tela_cadastrar_peca(self):
        self._titulo("Cadastrar Peça", cor="green")
        self.entry_peca_nome = self._entrada("Nome da Peça", 20)
        self.entry_peca_nome.grid(pady=20)
        self.entry_peca_qtd = self._entrada("Quantidade", 20)
        self.entry_peca_qtd.grid()
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(pady=30)
        ctk.CTkButton(
            frame, text="Voltar", command=self.mostrar_menu_estoque,
        ).grid(row=0, column=0, padx=8)
        ctk.CTkButton(
            frame, text="Cadastrar", command=self._salvar_peca,
        ).grid(row=0, column=1, padx=8)

    def _salvar_peca(self):
        try:
            self.estoque.adicionar_peca(
                self.entry_peca_nome.get(), self.entry_peca_qtd.get()
            )
            messagebox.showinfo("Sucesso", "Peça cadastrada com sucesso!")
            self.mostrar_menu_estoque()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def tela_ver_estoque(self):
        self._titulo("Estoque", cor="green")
        self.geometry("650x700")
        frame = ctk.CTkScrollableFrame(self, width=560, height=480)
        frame.grid(pady=10)
        for peca in self.estoque.listar_pecas():
            linha = ctk.CTkFrame(frame, fg_color="transparent")
            linha.pack(fill="x", padx=5, pady=3)
            ctk.CTkLabel(
                linha, text=peca.nome, font=("Century Gothic bold", 18),
            ).pack(side="left", padx=10)
            ctk.CTkLabel(
                linha, text=str(peca.quantidade), font=("Century Gothic bold", 18),
            ).pack(side="left", padx=20)
            ctk.CTkButton(
                linha, text="Editar", width=80,
                command=lambda p=peca: self._editar_peca(p),
            ).pack(side="right")
        ctk.CTkButton(
            self, text="Voltar", font=("Century Gothic bold", 20),
            command=self.mostrar_menu_estoque,
        ).grid(pady=10)

    def _editar_peca(self, peca):
        popup = ctk.CTkToplevel(self)
        popup.title(f"Editar Quantidade de {peca.nome}")
        popup.geometry("400x250")
        ctk.CTkLabel(popup, text="Nova Quantidade:", font=("Century Gothic bold", 16)).pack(pady=15)
        entrada = ctk.CTkEntry(popup)
        entrada.insert(0, str(peca.quantidade))
        entrada.pack(pady=10)

        def salvar():
            try:
                self.estoque.atualizar_quantidade(peca.id, entrada.get())
                popup.destroy()
                self.tela_ver_estoque()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ctk.CTkButton(popup, text="Salvar", command=salvar).pack(pady=10)

    # -------------------------------------------------------------- RELATÓRIOS #
    def abrir_calendario_diario(self):
        self._titulo("Relatório Diário", cor="green")
        self.calendario = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendario.grid(pady=15)
        ctk.CTkButton(
            self, text="Confirmar", font=("Century Gothic bold", 20),
            command=self._gerar_relatorio_diario,
        ).grid(pady=8)
        ctk.CTkButton(
            self, text="Voltar", command=self.mostrar_menu_relatorios,
        ).grid(pady=5)

    def _gerar_relatorio_diario(self):
        try:
            data = datetime.strptime(self.calendario.get_date(), "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Erro", "Data inválida.")
            return
        resumo = self.relatorios.relatorio_diario(data)
        self._mostrar_resumo(
            f"Relatório Diário ({data})", resumo,
            "dia mais movimentado: --",
        )

    def abrir_calendario_mensal(self):
        self._titulo("Relatório Mensal", cor="green")
        self.calendario = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendario.grid(pady=15)
        ctk.CTkButton(
            self, text="Confirmar", command=self._gerar_relatorio_mensal,
        ).grid(pady=8)
        ctk.CTkButton(
            self, text="Voltar", command=self.mostrar_menu_relatorios,
        ).grid(pady=5)

    def _gerar_relatorio_mensal(self):
        ano, mes, _ = self.calendario.get_date().split("-")
        resumo = self.relatorios.relatorio_mensal(int(ano), int(mes))
        topo = resumo.topo_movimentacao
        texto_topo = f"Dia mais movimentado: {topo[0]} ({topo[1]} clientes)"
        self._mostrar_resumo(f"Relatório Mensal ({mes}/{ano})", resumo, texto_topo)

    def tela_relatorio_anual(self):
        self._titulo("Relatório Anual", cor="green")
        self.entry_ano = self._entrada("Digite o Ano", 20)
        self.entry_ano.insert(0, str(datetime.now().year))
        self.entry_ano.grid(pady=30)
        ctk.CTkButton(
            self, text="Confirmar", command=self._gerar_relatorio_anual,
        ).grid(pady=8)
        ctk.CTkButton(
            self, text="Voltar", command=self.mostrar_menu_relatorios,
        ).grid(pady=5)

    def _gerar_relatorio_anual(self):
        try:
            ano = int(self.entry_ano.get())
        except ValueError:
            messagebox.showerror("Erro", "Ano inválido. Insira um número.")
            return
        resumo = self.relatorios.relatorio_anual(ano)
        topo = resumo.topo_movimentacao
        texto_topo = f"Mês mais movimentado: {topo[0]} ({topo[1]} clientes)"
        self._mostrar_resumo(f"Relatório Anual ({ano})", resumo, texto_topo)

    def _mostrar_resumo(self, titulo, resumo, extra=""):
        self._titulo(titulo, cor="green")
        self.geometry("780x700")
        frame = ctk.CTkScrollableFrame(self, width=760, height=520)
        frame.grid(pady=10)

        texto = (
            f"Total Faturado: R$ {resumo.total_faturado:.2f}\n"
            f"Total Pendente: R$ {resumo.total_pendente:.2f}\n"
            f"Total de Clientes: {resumo.total_clientes}\n"
            f"{extra}"
        )
        ctk.CTkLabel(
            frame, text=texto, font=("Century Gothic bold", 16),
            text_color="yellow", justify="left",
        ).grid(padx=20, pady=10, sticky="w")

        for cliente in resumo.detalhes:
            info = (
                f"{cliente.nome} | Peças: {cliente.pecas_utilizadas or '-'} | "
                f"Carro: {cliente.marca_carro} | Placa: {cliente.placa_carro} | "
                f"{'Pago' if cliente.esta_pago() else 'Pendente'}"
            )
            ctk.CTkLabel(
                frame, text=info, font=("Century Gothic", 14), text_color="white",
            ).grid(padx=10, pady=3, sticky="w")

        ctk.CTkButton(
            self, text="Voltar", command=self.mostrar_menu_relatorios,
        ).grid(pady=10)


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    # Garante que as tabelas existam antes de abrir a interface (idempotente).
    database.create_all()
    app = Tela()
    app.mainloop()


if __name__ == "__main__":
    main()
