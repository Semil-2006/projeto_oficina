"""Interface gráfica (CustomTkinter).

Consolida as três versões paralelas da interface original em uma única
implementação que consome a camada de serviços (pws.services). A lógica de
negócio permanece fora da UI, o que permite testá-la de forma unitária.
"""
from pws.ui.app import Tela  # noqa: F401

__all__ = ["Tela"]
