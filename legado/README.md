# Arquivo Legado (Código-fonte Original)

Esta pasta preserva o código-fonte **original** do projeto, conforme foi
desenvolvido antes da refatoração para a arquitetura atual (`pws/`).

## Por que existe?

O código original continha **três versões paralelas** da mesma aplicação, o
que dificultava manutenção e testes:

- `oficina/tela.py` — versão monolítica (1.552 linhas, tudo em uma classe)
- `oficina/deep/` — versão modular parcialmente completa
- `oficina/tela_refatorada.py` — tentativa de refatoração MVC (incompleta)
- `oficina/ofi/main.py` — experimento abandonado e quebrado (imports inexistentes)
- `oficina/goo.py` — bot de YouTube/Flask **não relacionado** ao sistema da oficina

## O que mudou

| Aspecto | Original | Refatorado (`pws/`) |
|---------|----------|---------------------|
| Estrutura | 3 versões + arquivos soltos | Um único pacote organizado |
| Banco de dados | 4 bancos SQLite separados | Um repositório gerenciado (`pws/database.py`) |
| Senha/resposta | Resposta em texto puro | Hash bcrypt para senha e resposta |
| Caminho da imagem | Absoluto e hardcoded | Relativo (`pws/config.py`) |
| Lógica de negócio | Embutida na UI (não testável) | Serviços independentes (`pws/services/`) |
| Testes | Não existiam | 142 testes (97% de cobertura) |

**Este diretório é apenas referência.** A versão ativa está em `pws/`, com a
lógica de negócio testável e a interface em `pws/ui/`.
