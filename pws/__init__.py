"""Pacote principal do Sistema de Gerenciamento para Oficina PWS.

Contém a lógica de negócio desacoplada da interface gráfica, organizada em:
- config.py   : configuração de caminhos e ambiente
- database.py : conexão e sessões com o banco de dados (SQLite + SQLAlchemy)
- models.py   : modelos ORM (Usuario, Cliente, Peca, Servico)
- validators  : validação de CPF, e-mail, telefone, placa e valor
- formatadores: formatação de telefone, placa, CPF e valor monetário
- services    : serviços de aplicação (autenticação, clientes, estoque, serviços, relatórios)
- pdf.py      : geração de orçamentos em PDF
- ui/         : interface gráfica (CustomTkinter)
"""

__version__ = "2.0.0"
__title__ = "Sistema de Gerenciamento para Oficina PWS"
