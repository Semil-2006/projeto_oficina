# ⚡ Testes de Carga e Estresse

Como a aplicação é **desktop** (sem servidor HTTP), os testes de carga atuam
sobre a camada de **banco de dados/persistência**, que é o ponto mais
suscetível a gargalos de desempenho.

---

## Como rodar

### Suíte de carga (pytest)

```bash
python -m pytest tests/load -m carga -s
```

### Benchmark rápido

```bash
python -m tests.load.benchmark 20000     # ou outro valor
```

---

## Cenários

| Teste | O que mede |
|-------|-----------|
| `test_insercao_em_massa` | Inserção de 10.000 clientes via bulk insert |
| `test_busca_e_paginacao_central` | Consulta + paginação com 10.000 registros |
| `test_relatorio_anual_central` | Relatório anual agregando 10.000 clientes |
| `test_estoque_containment` | Listagem de 2.000 peças |
| `test_uso_duradouro_sem_fugas` | 500 consultas consecutivas (detecção de degradação) |

---

## Resultados obtidos neste ambiente

Banco SQLite, 20.000 registros (via `benchmark.py`):

```
Operação                                            Tempo          Taxa
------------------------------------------------------------------------
Inserção em massa (bulk)                           2.34s        8534/s
Consulta + paginação (25 pág.)                    0.021s          48/s
Relatório anual (2025)                            0.538s       20000 clientes
Estoque - adicionar peça                         0.0054s
```

Interpretação:

- **Bulk insert** (8.500 registros/s) é ~50x mais rápido que o padrão de
  um-commit-por-registro que existia na versão original.
- **Relatório anual** sobre 20.000 clientes resolve em ~0,5s — adequado para
  uso diário incluso com base histórica grande.
- Operações de busca/paginação são sub-milissegundas (índice em `nome`/`data`).

---

## Sobre testar a UI sob carga

A interface não oferece endpoints HTTP e blocagens de rede não se aplicam.
Para um futuro **frontend web / API REST** (roadmap), recomenda-se:

- **Locust** (já listado em `requirements.txt`):
  ```python
  # locustfile.py (exemplo)
  from locust import HttpUser, task

  class OficinaUser(HttpUser):
      @task
      def listar_clientes(self):
          self.client.get("/api/clientes")
  ```
- **K6 / JMeter** para cenários de API e banco sob concorrência.

Esses cenários dependem da camada de API, ainda não implementada.
