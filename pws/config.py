"""Configuração central da aplicação.

Centraliza caminhos e parâmetros para evitar problemas como o caminho
absoluto e hardcoded da imagem que existia na versão monolítica.
"""
from __future__ import annotations

import os

# Diretório raiz do pacote (independe de onde o processo é iniciado).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho da imagem do logotipo (resolvido de forma relativa e segura).
LOGO_PATH = os.path.join(BASE_DIR, "img_do_carro.png")

# Nome do banco de dados padrão (arquivos SQLite).
DB_FILENAME = "pws.db"

# Diretório padrão para relatórios PDF gerados pelo usuário.
RELATORIOS_DIR = os.path.join(BASE_DIR, "relatorios")


def get_database_url() -> str:
    """Retorna a URL do banco de dados.

    Prioriza a variável de ambiente DATABASE_URL, permitindo que os testes
    usem um banco isolado sem alterar o código de produção.
    """
    return os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, DB_FILENAME)}")


def get_relatorios_dir() -> str:
    """Garante e retorna o diretório de relatórios."""
    os.makedirs(RELATORIOS_DIR, exist_ok=True)
    return RELATORIOS_DIR
