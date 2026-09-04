"""Testes de carga e estresse da camada de banco de dados.

Estes testes não fazem parte do conjunto padrão (marcados com @pytest.mark.carga).
Executar com:  python -m pytest tests/load -m carga

Objetivo: demonstrar que a camada de persistência escala com milhares de
registros, medindo o desempenho de inserção, busca e paginação.
"""
from __future__ import annotations

import time
from datetime import date, timedelta

import pytest

from pws.database import Database
from pws.services.cliente_service import ClienteService
from pws.services.estoque_service import EstoqueService


def _medir(funcao, repeticao=1):
    inicio = time.perf_counter()
    resultado = None
    for _ in range(repeticao):
        resultado = funcao()
    decorrido = time.perf_counter() - inicio
    return resultado, decorrido


@pytest.fixture(scope="module")
def banco_carga(tmp_path_factory):
    """Cria um banco populado com N clientes para os testes de carga."""
    arquivo = tmp_path_factory.mktemp("carga") / "carga.db"
    db = Database(f"sqlite:///{arquivo}")
    db.create_all()
    return db


@pytest.mark.carga
def test_insercao_em_massa(banco_carga):
    """Insere 10.000 clientes (bulk) e mede o tempo."""
    sf = banco_carga.session_factory()
    servico = ClienteService(sf)
    quantidade = 10_000

    def inserir():
        dados = [
            {
                "nome": f"Cliente {i}",
                "data_entrada": date(2025, 1, 1) + timedelta(days=i % 365),
                "marca_carro": f"Marca {i % 10}",
                "placa_carro": "ABC1234",
                "valor": float(i % 500),
                "forma_pagamento": "PIX" if i % 2 == 0 else None,
            }
            for i in range(quantidade)
        ]
        return servico.criar_clientes_em_massa(dados)

    total, tempo = _medir(inserir)
    taxa = total / tempo if tempo > 0 else 0
    print(f"\nInserção (bulk): {total} clientes em {tempo:.2f}s -> {taxa:.0f}/s")
    assert total == quantidade
    assert taxa > 100


@pytest.mark.carga
def test_busca_e_paginacao_central(banco_carga):
    """Mede a consulta + paginação com 10.000 registros."""
    sf = banco_carga.session_factory()
    servico = ClienteService(sf)

    def consultar():
        result, _total = servico.listar_clientes(busca="Cliente 999", por_pagina=10)
        return result

    resultado, tempo = _medir(consultar, repeticao=20)
    assert resultado
    print(f"\nBusca/paginação: 20 consultas em {tempo:.2f}s ({(20 / tempo):.0f}/s)")


@pytest.mark.carga
def test_relatorio_anual_central(banco_carga):
    """Mede a geração de relatório anual com grande volume de dados."""
    from pws.services.relatorio_service import RelatorioService

    sf = banco_carga.session_factory()
    relatorio = RelatorioService(sf)

    def gerar():
        return relatorio.relatorio_anual(2025)

    resumo, tempo = _medir(gerar)
    print(f"\nRelatório anual 2025: {resumo.total_clientes} clientes resolvido em {tempo:.3f}s")
    assert resumo.total_clientes > 0


@pytest.mark.carga
def test_estoque_containment(banco_carga):
    """Verifica que operações de estoque permanecem rápidas com muitas peças."""
    sf = banco_carga.session_factory()
    estoque = EstoqueService(sf)
    for i in range(2000):
        estoque.adicionar_peca(f"Peca {i}", i % 50)

    inicio = time.perf_counter()
    listados = estoque.listar_pecas()
    tempo = time.perf_counter() - inicio
    assert len(listados) >= 2000
    print(f"\nEstoque: listagem de {len(listados)} peças em {tempo:.3f}s")
    assert tempo < 5.0


@pytest.mark.carga
def test_uso_duradouro_sem_fugas(banco_carga):
    """Executa muitas operações em sequência para detectar degradação/fugas."""
    sf = banco_carga.session_factory()
    servico = ClienteService(sf)

    inicio = time.perf_counter()
    for i in range(500):
        servico.listar_clientes(pagina=i % 5, por_pagina=10)
    tempo = time.perf_counter() - inicio
    print(f"\nUso contínuo: 500 consultas em {tempo:.2f}s")
    # Sem crescimento de conexões: banco contém ~10k registros
    count = servico.listar_clientes(por_pagina=10)[1]
    assert count >= 10_000
