"""Serviço de gestão de serviços da oficina."""
from __future__ import annotations

from pws.models import Servico


class ServicoJaExisteError(Exception):
    """Lançada quando o serviço já está cadastrado."""


class ServicoNaoEncontradoError(Exception):
    """Lançada quando o serviço não existe."""


class ServicoService:
    """Operações de negócio sobre serviços."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def criar_servico(self, nome: str) -> Servico:
        """Cadastra um novo serviço."""
        nome = (nome or "").strip().upper()
        if not nome:
            raise ValueError("O nome do serviço não pode estar vazio.")

        session = self.session_factory()
        try:
            existente = session.query(Servico).filter_by(nome=nome).first()
            if existente:
                raise ServicoJaExisteError("Serviço já cadastrado.")
            servico = Servico(nome=nome)
            session.add(servico)
            session.commit()
            session.refresh(servico)
            return servico
        except Exception:
            session.rollback()
            raise
        finally:
            self.session_factory.remove()

    def listar_servicos(self) -> list[Servico]:
        """Lista todos os serviços cadastrados."""
        session = self.session_factory()
        try:
            return session.query(Servico).order_by(Servico.nome).all()
        finally:
            self.session_factory.remove()

    def obter_servico(self, servico_id: int) -> Servico:
        """Busca um serviço por id."""
        session = self.session_factory()
        try:
            servico = session.get(Servico, servico_id)
            if not servico:
                raise ServicoNaoEncontradoError("Serviço não encontrado.")
            return servico
        finally:
            self.session_factory.remove()

    def excluir_servico(self, servico_id: int) -> None:
        """Exclui um serviço pelo id."""
        session = self.session_factory()
        try:
            servico = session.get(Servico, servico_id)
            if not servico:
                raise ServicoNaoEncontradoError("Serviço não encontrado.")
            session.delete(servico)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            self.session_factory.remove()
