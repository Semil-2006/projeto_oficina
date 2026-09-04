"""Validações de dados de domínio.

Reúne e corrige as validações que estavam espalhadas na interface, tornando-as
independentes do tkinter e, portanto, testáveis de forma unitária.
"""
from __future__ import annotations

import re

# Mascaras do Mercosul: ABC1D23 (7 caracteres alfanuméricos)
PLACA_MERCOSUL_RE = re.compile(r"^[A-Z]{3}\d[A-Z0-9]\d{2}$")
# Placa antiga: ABC1234
PLACA_ANTIGA_RE = re.compile(r"^[A-Z]{3}\d{4}$")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_cpf(cpf: str) -> bool:
    """Valida um CPF verificando dígitos verificadores."""
    cpf = "".join(filter(str.isdigit, cpf or ""))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
        digito = (soma * 10) % 11
        if digito == 10:
            digito = 0
        if digito != int(cpf[i]):
            return False
    return True


def validar_email(email: str) -> bool:
    """Valida um endereço de e-mail."""
    if not email:
        return False
    return EMAIL_RE.match(email) is not None


def validar_telefone(telefone: str) -> bool:
    """Valida um telefone brasileiro (DDD + número, 10 ou 11 dígitos)."""
    telefone = "".join(filter(str.isdigit, telefone or ""))
    return len(telefone) in (10, 11)


def validar_placa(placa: str) -> bool:
    """Valida uma placa de veículo (formato antigo ou Mercosul)."""
    placa = "".join(c for c in (placa or "").upper() if c.isalnum())
    if len(placa) != 7:
        return False
    return bool(PLACA_MERCOSUL_RE.match(placa) or PLACA_ANTIGA_RE.match(placa))


def validar_valor(valor) -> bool:
    """Valida se um valor é um número não-negativo."""
    if valor is None:
        return True
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return False
    return numero >= 0


def converter_valor_para_float(texto: str) -> float:
    """Converte uma string de valor (ex: 'R$ 1.234,56') para float."""
    if texto is None:
        raise ValueError("Valor vazio")
    limpo = texto.replace("R$", "").replace(".", "").replace(",", ".").strip()
    if not limpo:
        raise ValueError("Valor vazio")
    return float(limpo)
