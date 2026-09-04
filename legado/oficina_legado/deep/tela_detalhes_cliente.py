import customtkinter as ctk
from fpdf import FPDF
from tkinter import filedialog
import tkinter as tk
from tela_editar_cliente import TelaEditarCliente
from tela_editar_pecas_utilizadas import TelaEditarPecasUtilizadas  # Importar nova tela
from datetime import datetime

class TelaDetalhesCliente(ctk.CTkFrame):
    def __init__(self, master, cliente, switch_to_ver_cliente):
        super().__init__(master, fg_color="darkblue")
        self.master = master
        self.cliente = cliente
        self.switch_to_ver_cliente = switch_to_ver_cliente
        
        self.criar_widgets()
        self.configurar_grid()

    def configurar_grid(self):
        # Aumentar o número de linhas para acomodar os novos campos
        for i in range(15):  # Aumentado de 12 para 15
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def criar_widgets(self):
        # Título
        self.titulo = ctk.CTkLabel(
            self,
            text="Detalhes do Cliente",
            font=("Century Gothic bold", 24),
            text_color="yellow"
        )
        self.titulo.grid(row=0, column=0, pady=20)

        # Detalhes do cliente (adicionar data de saída e peças utilizadas)
        detalhes = [
            f"Nome: {self.cliente['nome']}",
            f"CPF: {self.cliente['cpf'] or 'Não informado'}",
            f"E-mail: {self.cliente['email'] or 'Não informado'}",
            f"Telefone: {self.cliente['telefone'] or 'Não informado'}",
            f"Data Entrada: {self.cliente['data_entrada'] or 'Não informado'}",
            f"Valor: R${self.cliente['valor'] or 'Não informado'}",
            f"Marca do Carro: {self.cliente['marca_carro'] or 'Não informado'}",
            f"Placa do Carro: {self.cliente['placa_carro'] or 'Não informado'}",
            f"Forma de Pagamento: {self.cliente['forma_pagamento'] or 'Não informado'}",
            f"Data Saída: {self.cliente['data_saida'] or 'Não informado'}",  # Novo campo
        ]

        for i, texto in enumerate(detalhes, start=1):
            label = ctk.CTkLabel(
                self,
                text=texto,
                anchor="w",
                font=("Century Gothic", 16),
                text_color="white"
            )
            label.grid(row=i, column=0, padx=20, pady=5, sticky="w")
        
        # Campo para peças utilizadas
        pecas_texto = self.cliente.get('pecas_utilizadas', '') or "Nenhuma ainda"
        self.label_pecas = ctk.CTkLabel(
            self,
            text=f"Peças Utilizadas: {pecas_texto}",
            anchor="w",
            font=("Century Gothic", 16),
            text_color="white"
        )
        self.label_pecas.grid(row=12, column=0, padx=20, pady=5, sticky="w")
        
        # Botão para editar peças utilizadas
        self.btn_editar_pecas = ctk.CTkButton(
            self,
            text="Editar Peças Utilizadas",
            font=("Century Gothic bold", 18),
            command=self.editar_pecas_utilizadas
        )
        self.btn_editar_pecas.grid(row=13, column=0, pady=10)

        # Frame para botões
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=14, column=0, pady=20)  # Ajustado para nova posição

        # Botão Imprimir
        self.btn_imprimir = ctk.CTkButton(
            self.frame_botoes,
            text="Imprimir",
            font=("Century Gothic bold", 18),
            command=self.imprimir_orcamento
        )
        self.btn_imprimir.grid(row=0, column=0, padx=10)

        # Botão Editar
        self.btn_editar = ctk.CTkButton(
            self.frame_botoes,
            text="Editar",
            font=("Century Gothic bold", 18),
            command=self.editar_cliente
        )
        self.btn_editar.grid(row=0, column=1, padx=10)

        # Botão Voltar
        self.btn_voltar = ctk.CTkButton(
            self,
            text="Voltar",
            font=("Century Gothic bold", 18),
            command=self.switch_to_ver_cliente
        )
        self.btn_voltar.grid(row=15, column=0, pady=20)  # Ajustado para nova posição

    def editar_cliente(self):
        """Abre a tela de edição do cliente"""
        self.destroy()
        tela_edicao = TelaEditarCliente(
            self.master,
            cliente=self.cliente,
            switch_to_detalhes_cliente=self.master.mostrar_tela_detalhes_cliente
        )
        tela_edicao.pack(expand=True, fill="both")
    
    def editar_pecas_utilizadas(self):
        """Abre a tela de edição de peças utilizadas"""
        self.destroy()
        tela_edicao_pecas = TelaEditarPecasUtilizadas(
            self.master,
            cliente=self.cliente,
            switch_to_detalhes_cliente=self.master.mostrar_tela_detalhes_cliente
        )
        tela_edicao_pecas.pack(expand=True, fill="both")

    def imprimir_orcamento(self):
        gerar_pdf(self.cliente)

def gerar_pdf(cliente):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    # Cabeçalho
    pdf.set_fill_color(59, 55, 126)
    pdf.rect(0, 0, pdf.w, pdf.h, 'F')
    pdf.set_font('Arial', 'I', 37)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(10)
    pdf.cell(0, 20, 'Orçamento - PWS DO IRMÃO', border=False, ln=True, align='C')
    pdf.ln(10)
    
    # Imagem (ajuste o caminho conforme necessário)
    img_path = 'img_do_carro.png'
    pdf.image(img_path, x=pdf.w/2-30, y=50, w=60)
    
    # Detalhes
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
    
    # Rodapé
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(0, 10, 'Em caso de dúvidas, não hesite em nos contatar! Estamos à disposição para esclarecer qualquer questão e garantir que você tenha a melhor experiência com a PWS.')
    
    # Salvar arquivo
    root = ctk.CTk()  # Cria uma janela CTk temporária
    root.withdraw()
    caminho_arquivo = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        initialfile=f"{cliente['nome']}_orcamento.pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Salvar PDF",
        parent=root  # Especifica a janela pai
    )
    
    if caminho_arquivo:
        pdf.output(caminho_arquivo)
        print(f"PDF salvo em: {caminho_arquivo}")
    else:
        print("Salvamento cancelado!")
    
    root.destroy()

class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')