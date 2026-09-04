"""Modelos ORM do sistema.

Consolida os quatro modelos que originalmente viviam em bancos e arquivos
separados (Usuario, Cliente, Peca, Servico) em um único módulo, usando um
único Base compartilhado.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Usuario(Base):
    """Usuário do sistema com senha e resposta de segurança hasheadas."""

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_usuario = Column(String(50), nullable=False, unique=True, index=True)
    _senha_hash = Column("senha", String(128), nullable=False)
    pergunta_seguranca = Column(String(100), nullable=False)
    _resposta_seguranca_hash = Column("resposta_seguranca", String(128), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)

    def __init__(self, nome_usuario, senha, pergunta_seguranca, resposta_seguranca):
        self.nome_usuario = nome_usuario
        self.senha = senha
        self.pergunta_seguranca = pergunta_seguranca
        self.resposta_seguranca = resposta_seguranca

    @property
    def senha(self) -> str:
        raise AttributeError("A senha não pode ser lida diretamente.")

    @senha.setter
    def senha(self, senha_plana: str) -> None:
        from pws.services.auth_service import hash_senha

        if not isinstance(senha_plana, str):
            raise TypeError("A senha deve ser uma string.")
        self._senha_hash = hash_senha(senha_plana)

    def verificar_senha(self, senha_plana: str) -> bool:
        from pws.services.auth_service import verificar_senha

        return verificar_senha(senha_plana, self._senha_hash)

    @property
    def resposta_seguranca(self) -> str:
        raise AttributeError("A resposta de segurança não pode ser lida diretamente.")

    @resposta_seguranca.setter
    def resposta_seguranca(self, resposta_plana: str) -> None:
        from pws.services.auth_service import hash_senha

        if not isinstance(resposta_plana, str):
            raise TypeError("A resposta deve ser uma string.")
        self._resposta_seguranca_hash = hash_senha(resposta_plana)

    def verificar_resposta(self, resposta_plana: str) -> bool:
        from pws.services.auth_service import verificar_senha

        return verificar_senha(resposta_plana, self._resposta_seguranca_hash)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Usuario {self.nome_usuario}>"


class Cliente(Base):
    """Cliente atendido pela oficina associado a um veículo."""

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), nullable=True)
    email = Column(String(100), nullable=True)
    telefone = Column(String(20), nullable=True)
    data_entrada = Column(Date, nullable=False)
    valor = Column(Float, nullable=True)
    marca_carro = Column(String(50), nullable=False)
    placa_carro = Column(String(10), nullable=False)
    forma_pagamento = Column(Text, nullable=True)
    data_saida = Column(Date, nullable=True)
    pecas_utilizadas = Column(Text, nullable=True)

    def __init__(
        self,
        nome: str,
        data_entrada: date,
        marca_carro: str,
        placa_carro: str,
        cpf: Optional[str] = None,
        email: Optional[str] = None,
        telefone: Optional[str] = None,
        valor: Optional[float] = None,
        forma_pagamento: Optional[str] = None,
        data_saida: Optional[date] = None,
        pecas_utilizadas: Optional[str] = None,
        **kwargs,
    ):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.data_entrada = data_entrada
        self.valor = valor
        self.marca_carro = marca_carro
        self.placa_carro = placa_carro
        self.forma_pagamento = forma_pagamento
        self.data_saida = data_saida
        self.pecas_utilizadas = pecas_utilizadas

    def esta_pago(self) -> bool:
        """Considera o cliente pago quando há forma de pagamento informada."""
        return bool(self.forma_pagamento)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Cliente {self.nome} - {self.placa_carro}>"


class Peca(Base):
    """Peça do estoque."""

    __tablename__ = "pecas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    quantidade = Column(Integer, nullable=False, default=0)
    __table_args__ = (UniqueConstraint("nome", name="uq_peca_nome"),)

    def __init__(self, nome: str, quantidade: int = 0):
        self.nome = nome
        self.quantidade = quantidade

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Peca {self.nome}: {self.quantidade}>"


class Servico(Base):
    """Serviço oferecido pela oficina."""

    __tablename__ = "servicos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    __table_args__ = (UniqueConstraint("nome", name="uq_servico_nome"),)

    def __init__(self, nome: str):
        self.nome = nome

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Servico {self.nome}>"
