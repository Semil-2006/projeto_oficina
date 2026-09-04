"""Serviço de relatórios de faturamento (diário, mensal e anual).

Centraliza a lógica de agregação que estava espalhada na interface gráfica,
tornando-a testável e reutilizável.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Iterable

from pws.models import Cliente


@dataclass
class ResumoRelatorio:
    """Resumo agregado de um relatório de faturamento."""

    total_faturado: float = 0.0
    total_pendente: float = 0.0
    total_clientes: int = 0
    topo_movimentacao: tuple = None
    detalhes: list = field(default_factory=list)


def _calcular_totais(clientes: Iterable[Cliente]) -> tuple[float, float, int]:
    """Calcula total pago, total pendente e número de clientes."""
    total_pago = 0.0
    total_pendente = 0.0
    quantidade = 0
    for cliente in clientes:
        valor = cliente.valor or 0.0
        if cliente.esta_pago():
            total_pago += valor
        else:
            total_pendente += valor
        quantidade += 1
    return total_pago, total_pendente, quantidade


class RelatorioService:
    """Gera relatórios de faturamento a partir do banco."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def _clientes_no_periodo(self, condicao) -> list[Cliente]:
        session = self.session_factory()
        try:
            clientes = session.query(Cliente).filter(condicao).all()
            # Garante acesso seguro aos atributos antes de fechar a sessão.
            dados = list(clientes)
            return dados
        finally:
            self.session_factory.remove()

    def relatorio_diario(self, data) -> ResumoRelatorio:
        """Relatório de um dia específico."""
        clientes = self._clientes_no_periodo(Cliente.data_entrada == data)
        total_pago, total_pendente, quantidade = _calcular_totais(clientes)
        return ResumoRelatorio(
            total_faturado=total_pago,
            total_pendente=total_pendente,
            total_clientes=quantidade,
            detalhes=clientes,
        )

    def relatorio_mensal(self, ano: int, mes: int) -> ResumoRelatorio:
        """Relatório de um mês (ano/mês), com dia mais movimentado."""
        clientes = self._clientes_no_periodo(
            Cliente.data_entrada.like(f"{ano:04d}-{mes:02d}-%")
        )
        total_pago, total_pendente, quantidade = _calcular_totais(clientes)

        movimentacao_dias = Counter(c.data_entrada.day for c in clientes if c.data_entrada)
        topo = movimentacao_dias.most_common(1)
        return ResumoRelatorio(
            total_faturado=total_pago,
            total_pendente=total_pendente,
            total_clientes=quantidade,
            topo_movimentacao=topo[0] if topo else ("Nenhum", 0),
            detalhes=clientes,
        )

    def relatorio_anual(self, ano: int) -> ResumoRelatorio:
        """Relatório de um ano, com mês mais movimentado."""
        clientes = self._clientes_no_periodo(
            Cliente.data_entrada.between(f"{ano:04d}-01-01", f"{ano:04d}-12-31")
        )
        total_pago, total_pendente, quantidade = _calcular_totais(clientes)

        movimentacao_meses = Counter(c.data_entrada.month for c in clientes if c.data_entrada)
        topo = movimentacao_meses.most_common(1)
        return ResumoRelatorio(
            total_faturado=total_pago,
            total_pendente=total_pendente,
            total_clientes=quantidade,
            topo_movimentacao=topo[0] if topo else ("Nenhum", 0),
            detalhes=clientes,
        )
