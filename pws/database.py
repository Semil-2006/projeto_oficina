"""Camada de banco de dados reutilizável.

Consolida os quatro bancos SQLite separados da versão original em um único
gerenciador de sessões, simplificando a manutenção e tornando os serviços
testáveis com um banco isolado.
"""
from __future__ import annotations

from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker

from pws.config import get_database_url
from pws.models import Base


def _enable_foreign_keys(dbapi_connection, _connection_record):
    """Habilita suporte a chaves estrangeiras no SQLite por conexão."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_engine_from_url(url: str | None = None):
    """Cria um engine SQLAlchemy a partir de uma URL (ou da padrão)."""
    engine = create_engine(url or get_database_url(), pool_pre_ping=True)
    if engine.dialect.name == "sqlite":
        event.listens_for(engine, "connect")(_enable_foreign_keys)
    return engine


class Database:
    """Gerencia engine e sessões do banco de dados."""

    def __init__(self, url: str | None = None):
        self.url = url or get_database_url()
        self.engine = create_engine_from_url(self.url)

    def create_all(self):
        """Cria as tabelas caso ainda não existam."""
        Base.metadata.create_all(self.engine)

    def drop_all(self):
        """Remove todas as tabelas (usado em testes)."""
        Base.metadata.drop_all(self.engine)

    def session_factory(self):
        return scoped_session(
            sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)
        )

    def new_session(self):
        """Cria uma nova sessão (use como context manager ou feche manualmente)."""
        factory = self.session_factory()
        session = factory()
        return session


# Instância padrão da aplicação (banco de produção).
database = Database()
