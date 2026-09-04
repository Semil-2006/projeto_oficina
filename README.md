# 🚗 Sistema de Gerenciamento para Oficina PWS

Sistema desktop para gestão de uma oficina mecânica: **usuários, clientes,
serviços, estoque e relatórios de faturamento**, com geração de orçamentos em
PDF.

> Versão **2.0** — refatorada para uma arquitetura **limpa e testável**, com a
> lógica de negócio desacoplada da interface gráfica. O código original está
> preservado em [`legado/`](legado/README.md).

---

## ✨ Funcionalidades

- **Autenticação**
  - Cadastro de usuários com **hash bcrypt** e pergunta de segurança (a resposta
    também é hasheada — corrige vulnerabilidade da versão original).
  - Login seguro, recuperação e redefinição de senha.
- **Clientes**
  - Cadastro com validação (CPF, e-mail, telefone, placa).
  - Listagem, busca, paginação e edição.
  - Impressão de orçamento em **PDF**.
- **Serviços**
  - Cadastro, listagem e exclusão de serviços da oficina.
- **Estoque**
  - Adicionar peças (acumula quantidade quando a peça já existe), listar e editar.
- **Relatórios**
  - Relatórios **diário, mensal e anual** com total faturado, total pendente e
    dia/mês mais movimentado.

---

## 🏗️ Arquitetura

```
projeto_oficina/
├── main.py                    # Ponto de entrada (executa a interface)
├── requirements.txt           # Dependências
├── pyproject.toml             # Config do pytest/coverage
├── pws/                       # Pacote principal
│   ├── config.py              # Caminhos e configuração de ambiente
│   ├── database.py            # Engine/sessões SQLAlchemy (SQLite)
│   ├── models.py              # Modelos ORM: Usuario, Cliente, Peca, Servico
│   ├── validators.py          # Validação de CPF, e-mail, telefone, placa, valor
│   ├── formatadores.py        # Formatação de telefone, placa, CPF, valor
│   ├── pdf.py                 # Geração de orçamento em PDF (FPDF)
│   ├── services/              # 🧠 Lógica de negócio (desacoplada da UI)
│   │   ├── auth_service.py        # Cadastro, login, recuperação de senha
│   │   ├── cliente_service.py     # CRUD de clientes + busca/paginação
│   │   ├── estoque_service.py     # Gestão de peças
│   │   ├── servico_service.py     # CRUD de serviços
│   │   └── relatorio_service.py   # Relatórios diário/mensal/anual
│   └── ui/
│       └── app.py             # Interface gráfica (CustomTkinter)
├── tests/
│   ├── conftest.py            # Fixtures (banco isolado em memória)
│   ├── unit/                  # Testes unitários (97% de cobertura)
│   ├── integration/           # Testes de integração (fluxo completo)
│   └── load/                  # Testes de carga/estresse + benchmark
├── docs/                      # Documentação detalhada
└── legado/                    # Código-fonte original (arquivado)
```

### Principio-chave: separação de responsabilidades

A **interface** (`pws/ui/app.py`) apenas coleta entrada e exibe resultado.
Toda regra de negócio — validação, hashing, persistência, cálculo de
relatórios — vive em `pws/services/`, `pws/validators.py`,
`pws/formatadores.py` e `pws/pdf.py`, **independentes do tkinter**. Isso
permite testar a lógica de forma unitária, sem abrir uma janela.

---

## 🚀 Como executar

### 1. Criar ambiente virtual (recomendado)

```bash
python3 -m venv .venv
source .venv/bin/activate       # Linux/macOS
# ou .venv\Scripts\activate     # Windows
```

> No Linux, se o tkinter não estiver disponível:
> `sudo apt-get install python3-tk`

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Rodar a aplicação

```bash
python main.py
```

A janela **Sistema de Gerenciamento - Oficina PWS** será exibida. Faça login,
cadastre-se ou recupere a senha pela pergunta de segurança.

---

## 🧪 Testes

### Testes unitários e de integração (conjunto padrão)

```bash
python -m pytest                      # 137 testes (unit + integração)
```

### Cobertura de código

```bash
python -m pytest --cov=pws --cov-report=html
```

> **Cobertura da lógica de negócio: 97%** (acima da meta de 90%).
> O relatório HTML fica em `htmlcov/`.

### Testes de carga e estresse

Marcados com `@pytest.mark.carga` (não entram no conjunto padrão):

```bash
python -m pytest tests/load -m carga -s
```

Benchmark rápido de linha de comando:

```bash
python -m tests.load.benchmark 20000
```

Resultados obtidos (20.000 registros):

| Operação                          |  Tempo  |         Taxa |
|-----------------------------------|--------:|-------------:|
| Inserção em massa (bulk)          |   2.34s |   8.534 reg/s |
| Consulta + paginação              |  0.021s |        48/s  |
| Relatório anual (2025)            |  0.538s | 20.000 cli.  |
| Estoque — adicionar peça          | 0.0054s |      185/s   |

---

## 🐛 Bugs corrigidos nesta versão

1. **Caminho absoluto da imagem** — `definicoes.py`, `tela.py` e o módulo de
   clientes usavam `/home/semil/Área de Trabalho/oficina/img_do_carro.png`,
   quebrando o app em qualquer outra máquina. ✅ Agora usa path relativo
   (`pws/config.py`).
2. **Resposta de segurança em texto puro** — comparada e armazenada sem hash.
   ✅ Agora hasheada com bcrypt e comparada de forma segura.
3. **Duplicação de métodos e telas** — `limpar_tela`, `mostrar_erro`, etc.
   definidos duas vezes; inicialização fora de ordem instável. ✅ Código
   consolidado e ordenado.
4. **`ofi/main.py` quebrado** — importava módulos inexistentes. ✅ Removido do
   código ativo e arquivado.
5. **`goo.py` não relacionado** — bot de YouTube poluindo o repositório.
   ✅ Isolado em `legado/`.
6. **Banco disperso em 4 arquivos + dados de teste commitados** —
   ✅ Consolidado em um gerenciador único; bancos e cache ignorados pelo `.gitignore`.
7. **Sem `requirements.txt`** — ✅ Adicionado para reprodutibilidade.
8. **Validações no tkinter (não testáveis)** — ✅ Extraídas para módulos puros.

---

## 🧑‍💻 Pilares de POO

- **Herança**: `Tela(ctk.CTk)`, `Usuario(Base)`, `ResumoRelatorio` (dataclass).
- **Encapsulamento**: senha e resposta de segurança protegidas (não podem ser
  lidas diretamente).
- **Abstração**: serviços expõem operações de alto nível, escondendo o ORM.
- **Polimorfismo**: `Cliente.esta_pago()` e reuso dos serviços pela UI.

---

## 📄 Documentação adicional

- [Diagnóstico completo (bugs encontrados)](docs/DIAGNOSTICO.md)
- [Guia de testes e cobertura](docs/TESTES.md)
- [Notas de carga/estresse](docs/CARGA.md)

---

## 🔮 Funcionalidades futuras (roadmap)

- API REST para consulta de preços de peças em tempo real.
- Dashboard gráfico de desempenho da oficina.
- Autenticação com mais fatores (2FA).

---

## 👥 Contribuições

Contribuições são bem-vindas! Abra uma *issue* ou envie um *pull request*.

Repositório: `https://github.com/Semil-2006/projeto_oficina`
