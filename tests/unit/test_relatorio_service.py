"""Testes unitários do RelatorioService."""

from datetime import date

import pytest

from pws.services.cliente_service import ClienteService
from pws.services.relatorio_service import RelatorioService, _calcular_totais
from pws.models import Cliente


@pytest.fixture()
def setup(session_factory):
    clientes = ClienteService(session_factory)
    relatorio = RelatorioService(session_factory)
    return clientes, relatorio


def _popular(setup):
    clientes, _ = setup
    # 10/01/2025 -> faturado 100 (pago), pendente 200
    clientes.criar_cliente(
        nome="João", data_entrada=date(2025, 1, 10), marca_carro="Toyota",
        placa_carro="ABC1234", valor=100.0, forma_pagamento="CARTAO",
    )
    clientes.criar_cliente(
        nome="Maria", data_entrada=date(2025, 1, 10), marca_carro="Honda",
        placa_carro="XYZ9876", valor=200.0,
    )
    # fora do período (fevereiro)
    clientes.criar_cliente(
        nome="Ana", data_entrada=date(2025, 2, 5), marca_carro="Fiat",
        placa_carro="DEF1234", valor=300.0, forma_pagamento="PIX",
    )


class TestRelatorioDiario:
    def test_dia_com_clientes(self, setup):
        _, relatorio = setup
        _popular(setup)
        resumo = relatorio.relatorio_diario(date(2025, 1, 10))
        assert resumo.total_clientes == 2
        assert resumo.total_faturado == 100.0
        assert resumo.total_pendente == 200.0

    def test_dia_vazio(self, setup):
        _, relatorio = setup
        resumo = relatorio.relatorio_diario(date(2025, 3, 1))
        assert resumo.total_clientes == 0
        assert resumo.total_faturado == 0.0


class TestRelatorioMensal:
    def test_mes(self, setup):
        clientes, relatorio = setup
        _popular(setup)
        resumo = relatorio.relatorio_mensal(2025, 1)
        assert resumo.total_clientes == 2
        assert resumo.total_faturado == 100.0
        assert resumo.topo_movimentacao[0] == 10  # dia 10 mais movimentado
        assert resumo.topo_movimentacao[1] == 2

    def test_mes_vazio(self, setup):
        _, relatorio = setup
        resumo = relatorio.relatorio_mensal(2024, 12)
        assert resumo.total_clientes == 0


class TestRelatorioAnual:
    def test_ano(self, setup):
        clientes, relatorio = setup
        _popular(setup)
        resumo = relatorio.relatorio_anual(2025)
        assert resumo.total_clientes == 3
        assert resumo.total_faturado == 400.0
        assert resumo.total_pendente == 200.0

    def test_ano_vazio(self, setup):
        _, relatorio = setup
        resumo = relatorio.relatorio_anual(2020)
        assert resumo.total_clientes == 0


class TestCalcularTotais:
    def test_misto(self):
        cliente_pago = Cliente(
            nome="A", data_entrada=date(2025, 1, 1), marca_carro="X",
            placa_carro="ABC1234", valor=50.0, forma_pagamento="PIX",
        )
        cliente_pendente = Cliente(
            nome="B", data_entrada=date(2025, 1, 1), marca_carro="X",
            placa_carro="XYZ9876", valor=30.0,
        )
        pago, pendente, qtde = _calcular_totais([cliente_pago, cliente_pendente])
        assert pago == 50.0
        assert pendente == 30.0
        assert qtde == 2
