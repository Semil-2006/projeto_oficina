"""Benchmark CLI da camada de persistência.

Executa os mesmos cenários dos testes de carga e imprime um relatório de
desempenho, útil para demonstrar escalabilidade a um entrevistador.

Uso:
    python -m tests.load.benchmark [quantidade]
"""
from __future__ import annotations

import sys
import time
from datetime import date, timedelta

from pws.database import Database
from pws.services.cliente_service import ClienteService
from pws.services.estoque_service import EstoqueService
from pws.services.relatorio_service import RelatorioService


def _medir(funcao):
    inicio = time.perf_counter()
    resultado = funcao()
    return resultado, time.perf_counter() - inicio


def rodar(quantidade: int = 10_000) -> None:
    print(f"Benchmark da camada de banco de dados ({quantidade} registros)\n")
    print(f"{'Operação':<45}{'Tempo':>12}{'Taxa':>14}")
    print("-" * 72)

    db = Database("sqlite:///:memory:")
    db.create_all()
    sf = db.session_factory()
    clientes = ClienteService(sf)

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
    total, t = _medir(lambda: clientes.criar_clientes_em_massa(dados))
    print(f"{'Inserção em massa (bulk)':<45}{t:>10.2f}s{total / t:>12.0f}/s")

    def consulta():
        clientes.listar_clientes(pagina=0, por_pagina=25)

    _, t = _medir(consulta)
    print(f"{'Consulta + paginação (25 pág.)':<45}{t:>10.3f}s{1 / t:>12.0f}/s")

    relatorio = RelatorioService(sf)
    r, t = _medir(lambda: relatorio.relatorio_anual(2025))
    print(f"{'Relatório anual (2025)':<45}{t:>10.3f}s{r.total_clientes:>12} clientes")

    estoque = EstoqueService(sf)
    e, t = _medir(lambda: estoque.adicionar_peca("Pneus", 20))
    print(f"{'Estoque - adicionar peça':<45}{t:>10.4f}s")

    print("\nBenchmark concluído.")


if __name__ == "__main__":
    qtd = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000
    rodar(qtd)
