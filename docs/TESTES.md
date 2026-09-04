# 🧪 Guia de Testes

Documentação da suíte de testes do Sistema de Gerenciamento para Oficina PWS.

---

## Visão geral

| Categoria | Arquivos | Qtd. testes | Objetivo |
|-----------|----------|------------:|----------|
| **Unitários** | `tests/unit/` | 131 | Valida lógica pura e serviços isolados |
| **Integração** | `tests/integration/` | 3 | Fluxo completo com banco real persistido |
| **Carga/estresse** | `tests/load/` | 5 | Escalabilidade da camada de dados |

**Total: 139 testes** (carga à parte, marcada com `@pytest.mark.carga`).

---

## Executando

### Conjunto padrão (unitários + integração)

```bash
python -m pytest
```

Saída esperada:

```
137 passed
```

### Com cobertura

```bash
python -m pytest --cov=pws --cov-report=term
python -m pytest --cov=pws --cov-report=html   # relatório em htmlcov/
```

**Cobertura atual da lógica de negócio: 97%.**

| Módulo | Cobertura |
|--------|----------:|
| `pws/config.py` | 82% |
| `pws/formatadores.py` | 89% |
| `pws/models.py` | 99% |
| `pws/services/auth_service.py` | 99% |
| `pws/services/cliente_service.py` | 94% |
| `pws/services/estoque_service.py` | 96% |
| `pws/validators.py` | 95% |
| `pws/database.py`, `pws/services/relatorio_service.py`, `pws/pdf.py` | 100% |

> A interface (`pws/ui/`) é excluída da medição por exigir display/tkinter —
> sua lógica está delegada aos serviços já cobertos.

### Testes de carga

```bash
python -m pytest tests/load -m carga -s
```

---

## Estratégia de isolamento (`tests/conftest.py`)

Cada teste usa um **banco SQLite em memória**:
- `db` — cria engine + tabelas.
- `session_factory` — fábrica de sessões vinculada ao banco isolado.
- `_limpar_tabelas` (autouse) — recria o banco entre testes, garantindo
  independência total e **sem tocar no banco de produção**.

---

## O que cada suíte cobre

### Unitários

- **`test_validators.py`** — CPF (dígitos verificadores), e-mail, telefone,
  placa (Mercosul/antiga), valor e conversão monetária.
- **`test_formatadores.py`** — telefone, placa, CPF e valor (R$).
- **`test_auth_service.py`** — hashing, cadastro, login, recuperação, redefinição
  de senha e todos os fluxos de exceção.
- **`test_cliente_service.py`** — CRUD, validações, busca, paginação, bulk insert.
- **`test_estoque_service.py`** — CRUD de peças, acumulação de quantidade.
- **`test_servico_service.py`** — CRUD de serviços, unicidade.
- **`test_relatorio_service.py`** — diário/mensal/anual, totalização pago/pendente.
- **`test_models.py`** — proteção de senha/resposta, estado de pagamento, schema.
- **`test_pdf.py`** — montagem de dados e geração real de `.pdf`.

### Integração

- **`test_fluxo_completo.py`** — simula o uso real: cadastro/login → cliente →
  estoque → serviço → busca/edição → relatório → verificação de persistência.
- Persistência entre conexões distintas.
