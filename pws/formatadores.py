"""Formatadores de dados de entrada.

Replica de forma pura (sem tkinter) as funções de formatação que estavam
embutidas na interface, permitindo testes unitários diretos.
"""
from __future__ import annotations

import re


def formatar_telefone(texto: str) -> str:
    """Formata um telefone brasileiro como (DDD) NNNNN-NNNN.

    Suporta números fixos (10 dígitos) e móveis (11 dígitos).
    Idempotente: formatar um valor já formatado produz o mesmo resultado,
    o que permite uso direto em máscaras de entrada real-time.
    """
    texto = "".join(filter(str.isdigit, texto or ""))
    if texto.startswith("55") and len(texto) > 11:
        texto = texto[2:]
    texto = texto[-11:]

    if not texto:
        return ""

    ddd = texto[:2]
    numero = texto[2:]
    if len(numero) <= 2:
        return f"({ddd}) {numero}"
    if len(numero) == 8:
        return f"({ddd}) {numero[:4]}-{numero[4:]}"
    if len(numero) == 9:
        return f"({ddd}) {numero[:5]}-{numero[5:]}"
    if len(numero) < 8:
        return f"({ddd}) {numero}"
    return f"({ddd}) {numero[:5]}-{numero[5:]}"



def formatar_placa(texto: str) -> str:
    """Formata uma placa alfanumérica, ex: ABC1D23 -> ABC1D23 / ABC1234 -> ABC-1234."""
    texto = "".join(c for c in (texto or "").upper() if c.isalnum())[:7]
    if len(texto) > 3:
        return texto[:3] + "-" + texto[3:]
    return texto


def formatar_cpf(cpf: str) -> str:
    """Formata um CPF como XXX.XXX.XXX-XX."""
    cpf = "".join(filter(str.isdigit, cpf or ""))[:11]
    if len(cpf) > 9:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    if len(cpf) > 6:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:]}"
    if len(cpf) > 3:
        return f"{cpf[:3]}.{cpf[3:]}"
    return cpf


def formatar_valor_entrada(texto: str) -> str:
    """Formata um valor digitado em centavos, ex: 123456 -> 'R$ 1.234,56'."""
    valor = re.sub(r"\D", "", texto or "")
    if not valor:
        return "R$ 0,00"
    inteiro = int(valor)
    reais = inteiro // 100
    centavos = inteiro % 100
    reais_formatado = f"{reais:,.0f}".replace(",", ".")
    return f"R$ {reais_formatado},{centavos:02d}"


def formatar_valor_monetario(valor: float) -> str:
    """Formata um float como string monetária brasileira, ex: 1234.5 -> 'R$ 1.234,50'."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
