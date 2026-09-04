"""Geração de orçamentos em PDF.

Versão corrigida da geração de PDF que originalmente usava um caminho
absoluto e hardcoded para a imagem do logotipo.
"""
from __future__ import annotations

import os
from typing import Mapping

from fpdf import FPDF

from pws.config import LOGO_PATH

HEADER_COLOR = (59, 55, 126)  # #3B377E (azul PWS)
CELL_BG_COLOR = (255, 255, 255)
CELL_TEXT_COLOR = (0, 0, 0)


class OrcamentoPDF(FPDF):
    """PDF de orçamento com cabeçalho/rodapé padronizados."""

    def header(self):
        self.set_fill_color(*HEADER_COLOR)
        self.rect(0, 0, self.w, self.h, "F")
        self.set_font("Arial", "I", 37)
        self.set_text_color(255, 255, 255)
        self.set_y(10)
        self.cell(0, 20, "Orçamento - PWS DO IRMÃO", border=False, ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")


def montar_dados_orcamento(cliente: Mapping) -> list[tuple[str, str]]:
    """Prepara a lista campo/valor do orçamento a partir de um dict de cliente."""
    return [
        ("NOME", cliente.get("nome") or "Não informado"),
        ("CPF", cliente.get("cpf") or "Não informado"),
        ("EMAIL", cliente.get("email") or "Não informado"),
        ("TELEFONE", cliente.get("telefone") or "Não informado"),
        ("MARCA DO CARRO", cliente.get("marca_carro") or "Não informado"),
        ("PLACA DO CARRO", cliente.get("placa_carro") or "Não informado"),
        ("Peças Utilizadas", cliente.get("pecas_utilizadas") or "Não informado"),
        (
            "Valor Total",
            f"R${cliente['valor']:.2f}" if cliente.get("valor") is not None else "Não informado",
        ),
        ("Forma de Pagamento", cliente.get("forma_pagamento") or "Não informado"),
    ]


def gerar_pdf_para_caminho(cliente: Mapping, caminho_arquivo: str) -> None:
    """Gera o PDF do orçamento para um caminho específico (sem janela de diálago)."""
    pdf = OrcamentoPDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    # Logotipo (só se existir, tolerando ausência).
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=(pdf.w - 75.7) / 2, y=50, w=75.7, h=39.4)

    pdf.set_y(100)
    pdf.set_fill_color(*CELL_BG_COLOR)
    pdf.set_text_color(*CELL_TEXT_COLOR)

    for campo, valor in montar_dados_orcamento(cliente):
        pdf.cell(50, 10, campo, border=1, align="L", fill=True)
        pdf.cell(0, 10, valor, border=1, ln=True, align="L")

    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(
        0,
        10,
        "Em caso de dúvidas, não hesite em nos contatar! Estamos à disposição "
        "para esclarecer qualquer questão e garantir que você tenha a melhor "
        "experiência com a PWS.",
    )
    pdf.output(caminho_arquivo)
