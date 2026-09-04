"""Testes dos modelos ORM."""

from datetime import date

import pytest

from pws.config import get_database_url
from pws.database import Database
from pws.models import Cliente, Peca, Servico, Usuario


class TestUsuarioModel:
    def test_senha_nao_pode_ser_lida(self, session_factory):
        session = session_factory()
        try:
            u = Usuario("JOAO", "senha123", "P", "R")
            session.add(u)
            session.commit()
            session.refresh(u)
            with pytest.raises(AttributeError):
                _ = u.senha
            # mas verifica corretamente
            assert u.verificar_senha("senha123") is True
            assert u.verificar_senha("errada") is False
        finally:
            session_factory.remove()

    def test_resposta_nao_pode_ser_lida(self, session_factory):
        session = session_factory()
        try:
            u = Usuario("MARIA", "senha123", "P", "RESPOSTA")
            session.add(u)
            session.commit()
            session.refresh(u)
            with pytest.raises(AttributeError):
                _ = u.resposta_seguranca
            # bcrypt é sensível a maiúsculas: deve bater exatamente
            assert u.verificar_resposta("RESPOSTA") is True
            assert u.verificar_resposta("resposta") is False
        finally:
            session_factory.remove()

    def test_senha_int_lanca_tipo_erro(self):
        u = Usuario("A", "senha123", "P", "R")
        with pytest.raises(TypeError):
            u.senha = 123  # não é string


class TestClienteModel:
    def test_esta_pago(self):
        pago = Cliente(
            nome="A", data_entrada=date(2025, 1, 1), marca_carro="X",
            placa_carro="ABC1234", valor=10, forma_pagamento="PIX",
        )
        nao_pago = Cliente(
            nome="B", data_entrada=date(2025, 1, 1), marca_carro="X",
            placa_carro="ABC1234",
        )
        assert pago.esta_pago() is True
        assert nao_pago.esta_pago() is False


class TestDatabaseConfig:
    def test_get_database_url_padrao(self, monkeypatch):
        monkeypatch.delenv("DATABASE_URL", raising=False)
        url = get_database_url()
        assert url.startswith("sqlite:///")

    def test_get_database_url_env(self, monkeypatch):
        monkeypatch.setenv("DATABASE_URL", "sqlite:///custom.db")
        assert get_database_url() == "sqlite:///custom.db"

    def test_database_cria_tabelas(self, tmp_path):
        from sqlalchemy import text

        arquivo = tmp_path / "pws_test.db"
        db = Database(f"sqlite:///{arquivo}")
        db.create_all()
        with db.engine.connect() as conn:
            tabelas = set(
                row[0]
                for row in conn.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table'")
                )
            )
        assert {"usuarios", "clientes", "pecas", "servicos"} <= tabelas
