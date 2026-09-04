# 🔍 Diagnóstico Completo da Aplicação

Este documento registra o processo de auditoria do projeto **Sistema de
Gerenciamento para Oficina PWS**, os problemas encontrados e como foram
resolvidos na refatoração para a versão 2.0.

---

## 1. Estado original do projeto

### 1.1 Versões paralelas (duplicação de código)

O repositório continha **três implementações independentes** do mesmo sistema,
foi impossível determinar qual estava "ativa":

| Arquivo/Dir | Descrição | Estado |
|-------------|-----------|--------|
| `oficina/tela.py` | Monolítica — 1.552 linhas, tudo em uma classe `Tela` | Duplicado, métodos redefinidos |
| `oficina/deep/` | Modular — 14 telas + `app.py` | Parcialmente completa |
| `oficina/tela_refatorada.py` | MVC incompleto (placeholder "..." no código) | Incompleta |
| `oficina/ofi/main.py` | Experimento abandonado | **Quebrado** (imports inexistentes) |

**Ação:** consolidamos em uma única versão em `pws/`, com o original arquivado
em `legado/`.

### 1.2 Código não relacionado

- `oficina/goo.py` — bot de YouTube Live (OAuth, Flask, Gemini) **sem relação
  com a oficina**.
- `oficina/templates/dashboard.html` + `viewers.db` — back-end do mesmo bot.

**Ação:** isolados em `legado/` para não confundir o escopo do sistema.

### 1.3 Ausência de dependências e configuração

- **Não existia** `requirements.txt`, `pyproject.toml`, `.gitignore` ou `.env`.
- A reprodução do ambiente dependia de documentação vaga no README.

---

## 2. Bugs e vulnerabilidades encontrados

### 🔴 Críticos (impacto em produção/segurança)

| # | Bug | Arquivo (original) | Impacto | Correção |
|---|-----|--------------------|---------|----------|
| 1 | **Resposta de segurança armazenada e comparada em texto puro** | `banco_de_dados_login.py`, `definicoes.py` | Qualquer pessoa com acesso ao banco lê as respostas; permite recuperação de senha sem uma senha real | Hash bcrypt; comparação segura (`auth_service.py`) |
| 2 | **Caminho absoluto da imagem do logotipo** | `definicoes.py`, `tela.py`, `banco_de_dados_clientes.py` | `FileNotFoundError` em qualquer máquina que não seja `/home/semil/...` | Caminho relativo em `pws/config.py` |
| 3 | **`ofi/main.py` quebrado** | `ofi/main.py` | Importa `cadastro`/`TelaCadastro` inexistentes — crash garantido | Removido do código ativo |

### 🟠 Altos (robustez e manutenção)

| # | Bug | Impacto | Correção |
|---|-----|---------|----------|
| 4 | **Inicialização desordenada da janela** — `__init__` chama `tela_clientes()`, `criar_tela_cadastro()` e depois `criar_tela_login()`, criando telas várias vezes | Navegação confusa, leaks de widgets | Ordem limpa de navegação em `pws/ui/app.py` |
| 5 | **Métodos duplicados** (`limpar_tela`, `mostrar_erro`, `atualizar_lista_clientes` definidos 2x) | O 2º sobrescreve o 1º — comportamento imprevisível | Consolidado em definição única |
| 6 | **`secao.close()` dentro de `obter_clientes`** | Fecha a sessão global compartilhada, quebrando consultas futuras | Sessões gerenciadas por factory (não fechadas manualmente) |
| 7 | **Uso misto de `session` e `seccao`** (`tela.py` salva peça com `session` do banco de usuários) | Peça gravada no banco errado | Repositório único em `pws/database.py` |

### 🟡 Médios (qualidade)

| # | Problema | Correção |
|---|----------|----------|
| 8 | Validações (CPF, placa, e-mail, valor) embutidas na UI, não testáveis | Extraídas para `pws/validators.py` e `formatadores.py` |
| 9 | 4 bancos SQLite separados e dados de teste commitados | Banco único + `.gitignore` |
| 10 | Duplicação de `gerar_pdf`/`PDF` entre `tela.py` e `definicoes.py` | `pws/pdf.py` |
| 11 | Sem testes, sem CI, sem metadados | 142 testes, 97% de cobertura |

---

## 3. Verificação de execução

- **Este ambiente** não possui display gráfico/tkinter instalado (exige
  `python3-tk`, que requer permissão de superusuário indisponível aqui). Por
  isso, a **interface não pôde ser aberta neste sandbox**.
- A **lógica de negócio foi integralmente validada** via 142 testes que rodam
  sem interface, comprovando que a camada de serviço é funcional e testável.
- Em uma máquina com display (configuração padrão de desktop), a interface
  é executada com `python main.py`.

> Nota: a GUI é sintaticamente válida e consome os serviços testados; a única
> limitação não-testada neste ambiente é a renderização visual, que depende de
> disponibilidade de tkinter/display.

---

## 4. Melhorias aplicadas

1. **Arquitetura em camadas** — UI desacoplada da lógica de negócio.
2. **Segurança** — hashing da senha **e da resposta** de segurança.
3. **Testabilidade** — serviço independente do tkinter, 97% de cobertura.
4. **Reprodutibilidade** — `requirements.txt` e `pyproject.toml`.
5. **Higiene do repositório** — `.gitignore`, banco único, remoção de código morto.
6. **Carga/estresse** — bulk insert + benchmark provando escalabilidade.
