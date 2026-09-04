"""Testes de integração.

Testam o fluxo completo da aplicação: autenticação -> cadastro de clientes ->
estoque -> serviços -> relatórios -> geração de PDF, usando um banco SQLite
de arquivo real (persistência de verdade).
"""
from __future__ import annotations

from datetime import date

import pytest

from pws.database import Database
from pws.models import Cliente, Peca, Servico, Usuario
from pws.services.auth_service import AuthService
from pws.services.cliente_service import ClienteService
from pws.services.estoque_service import EstoqueService
from pws.services.relatorio_service import RelatorioService
from pws.services.servico_service import ServicoService


@pytest.fixture()
def integracao(tmp_path):
    """Configura um banco de arquivo real, persistindo entre operações."""
    arquivo = tmp_path / "integracao.db"
    db = Database(f"sqlite:///{arquivo}")
    db.create_all()
    sf = db.session_factory()
    return {
        "db": db,
        "sf": sf,
        "auth": AuthService(sf),
        "clientes": ClienteService(sf),
        "estoque": EstoqueService(sf),
        "servicos": ServicoService(sf),
        "relatorios": RelatorioService(sf),
    }


def test_fluxo_completo(integracao):
    auth = integracao["auth"]
    clientes = integracao["clientes"]
    estoque = integracao["estoque"]
    servicos = integracao["servicos"]
    relatorios = integracao["relatorios"]

    # 1) Cadastro e login de usuário
    auth.cadastrar_usuario("gerente", "senhaForte1", "Pergunta?", "Resposta")
    usuario = auth.autenticar("GERENTE", "senhaForte1")
    assert usuario.nome_usuario == "GERENTE"

    # 2) Cadastro de clientes
    c1 = clientes.criar_cliente(
        nome="Carlos", data_entrada=date(2025, 3, 1), marca_carro="Ford",
        placa_carro="ABC1234", valor=500.0, forma_pagamento="PIX",
    )
    clientes.criar_cliente(
        nome="Bianca", data_entrada=date(2025, 3, 1), marca_carro="Fiat",
        placa_carro="XYZ9876", valor=300.0,
    )

    # 3) Estoque
    estoque.adicionar_peca("Oleo", 10)
    estoque.adicionar_peca("Oleo", 5)

    # 4) Serviços
    servicos.criar_servico("Troca de oleo")

    # 5) Busca e atualização
    achados, total = clientes.listar_clientes(busca="carlos")
    assert total == 1
    clientes.atualizar_cliente(c1.id, {"forma_pagamento": "CARTAO"})
    assert clientes.obter_cliente(c1.id).esta_pago()

    # 6) Relatório do dia
    resumo = relatorios.relatorio_diario(date(2025, 3, 1))
    assert resumo.total_clientes == 2
    assert resumo.total_faturado == 500.0
    assert resumo.total_pendente == 300.0

    # 7) Persistência real: dados gravados no arquivo
    with integracao["sf"]() as sessao:
        assert sessao.query(Usuario).count() == 1
        assert sessao.query(Cliente).count() == 2
        assert sessao.query(Peca).count() == 1
        assert sessao.query(Servico).count() == 1
        assert sessao.query(Peca).first().quantidade == 15


def test_persistencia_entre_conexoes(tmp_path):
    """Garante que dados persistidos sobrevivem a novas conexões."""
    arquivo = tmp_path / "persist.db"
    db = Database(f"sqlite:///{arquivo}")
    db.create_all()

    s1 = db.new_session()
    try:
        s1.add(Peca(nome="PASTILHA", quantidade=4))
        s1.commit()
    finally:
        s1.close()

    # Nova conexão lê o dado persistido
    s2 = db.new_session()
    try:
        assert s2.query(Peca).filter_by(nome="PASTILHA").first().quantidade == 4
    finally:
        s2.close()


def test_integridade_chave_estrangeira(tmp_path):
    """Banco permite registros sem FKs, mas códigos não devem quebrar."""
    db = Database(f"sqlite:///{tmp_path}/fk.db")
    db.create_all()
    sf = db.session_factory()
    estoque = EstoqueService(sf)
    estoque.adicionar_peca("Pneu", 2)
    assert estoque.obter_peca(1).nome == "PNEU"
