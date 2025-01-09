import bcrypt
from tkinter import messagebox
from banco_de_dados_login import Usuario,session
from banco_de_dados_clientes import Cliente, secao
import tkinter as tk
import customtkinter as ctk
from banco_de_dados_clientes import Cliente, secao
from tkcalendar import Calendar
import re
from tkinter import messagebox
from banco_de_dados_clientes import Cliente,secao
import customtkinter as ctk
import os
from tkinter import filedialog
import customtkinter as ctk
from fpdf import FPDF
from tkinter import filedialog, Tk

def limpar_tela(self):
    for widget in self.winfo_children():
        widget.grid_forget()

def hash_senha(senha):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode('utf-8'), salt)


def verificar_resposta(usuario_entry, resposta_entry, callback_sucesso):
    usuario = usuario_entry.get().strip().upper()
    resposta_usuario = resposta_entry.get().strip().upper()

    if not resposta_usuario:
        messagebox.showerror("Erro", "O campo 'Resposta' deve ser preenchido.")
        return

    usuario_encontrado = session.query(Usuario).filter_by(nome_usuario=usuario).first()

    if usuario_encontrado:
        if usuario_encontrado.resposta_seguranca == resposta_usuario:
            callback_sucesso()  # Chama o callback para exibir a tela de sucesso
        else:
            messagebox.showerror("Erro", "Resposta incorreta.")
    else:
        messagebox.showerror("Erro", "Usuário não encontrado.")

def verificar_usuario_existe(usuario_entry, callback_pergunta):
    usuario = usuario_entry.get().strip().upper()
    if not usuario:
        messagebox.showerror("Erro", "O campo 'Usuário' deve ser preenchido.")
        return

    usuario_encontrado = session.query(Usuario).filter_by(nome_usuario=usuario).first()

    if usuario_encontrado:
        callback_pergunta()
    else:
        messagebox.showerror("Erro", "Usuário não encontrado.")



def cadastrar_usuario(usuario_entry, senha_entry, repetir_senha_entry, pergunta_combo, resposta_entry, callback_login):
    usuario = usuario_entry.get().strip().upper()
    senha = senha_entry.get().strip()
    repetir_senha = repetir_senha_entry.get().strip()
    pergunta = pergunta_combo.get().strip()
    resposta = resposta_entry.get().strip().upper()

    if senha != repetir_senha:
        messagebox.showerror("Erro", "As senhas não coincidem. Tente novamente.")
        return

    if not usuario:
        messagebox.showerror("Erro", "O campo 'Usuário' deve ser preenchido.")
        return
    if not senha:
        messagebox.showerror("Erro", "O campo 'Senha' deve ser preenchido.")
        return
    if not pergunta:
        messagebox.showerror("Erro", "Selecione uma pergunta de segurança.")
        return
    if not resposta:
        messagebox.showerror("Erro", "O campo 'Resposta' deve ser preenchido.")
        return

    usuario_existente = session.query(Usuario).filter_by(nome_usuario=usuario).first()
    if usuario_existente:
        messagebox.showerror("Erro", "Nome de usuário já cadastrado. Escolha outro.")
        return

    novo_usuario = Usuario(
        nome_usuario=usuario,
        senha=hash_senha(senha),
        pergunta_seguranca=pergunta,
        resposta_seguranca=resposta
    )

    try:
        session.add(novo_usuario)
        session.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        callback_login()  # Volta à tela de login
    except Exception as e:
        session.rollback()
        messagebox.showerror("Erro", "Ocorreu um erro ao cadastrar o usuário. Tente novamente.")

def imprimir_orcamento(self, cliente):
    gerar_pdf(cliente)

def gerar_pdf(cliente):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    # Adicionar imagem do carro
    img_path = '/home/semil/Área de Trabalho/oficina/img_do_carro.png'
    img_width, img_height = 75.7, 39.4
    img_x = (pdf.w - img_width) / 2
    img_y = 50
    pdf.image(img_path, x=img_x, y=img_y, w=img_width, h=img_height)

    # Adicionar dados do cliente
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

    # Mensagem final
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(0, 10,
                   'Em caso de dúvidas, não hesite em nos contatar! Estamos à disposição para esclarecer qualquer questão e garantir que você tenha a melhor experiência com a PWS.')

    # Abrir janela de "Salvar como"
    root = Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
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

    # Classe PDF para o layout
class PDF(FPDF):
    def header(self):
        self.set_fill_color(59, 55, 126)  # Fundo azul
        self.rect(0, 0, self.w, self.h, 'F')  # Preencher toda a página
        self.set_font('Arial', 'I', 37)
        self.set_text_color(255, 255, 255)  # Texto branco
        self.set_y(10)
        self.cell(0, 20, 'Orçamento - PWS DO IRMÃO', border=False, ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')
