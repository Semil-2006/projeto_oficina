"""Fixtures de teste compartilhadas.

Fornece um banco de dados SQLite isolado (em memória) para cada teste,
garantindo que os testes sejam independentes e não afetem o banco de produção.
"""
from __future__ import annotations

import pytest

from pws.database import Database
from pws.models import Base


@pytest.fixture()
def db():
    """Cria um banco isolado em memória com as tabelas criadas."""
    database = Database("sqlite:///:memory:")
    database.create_all()
    return database


@pytest.fixture()
def session_factory(db):
    """Retorna a fábrica de sessões vinculada ao banco isolado."""
    return db.session_factory()


@pytest.fixture()
def commit_session(request, session_factory):
    """Sessão para criar dados no banco (remove ao final)."""
    session = session_factory()
    request.addfinalizer(session_factory.remove)
    return session


@pytest.fixture(autouse=True)
def _limpar_tabelas(request, db):
    """Garante que o banco em memória comece vazio a cada teste."""
    yield
    db.drop_all()
    db.create_all()
