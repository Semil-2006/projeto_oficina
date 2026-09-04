"""Serviço de controle de estoque (peças)."""
from __future__ import annotations

from pws.models import Peca


class PecaNaoEncontradaError(Exception):
    """Lançada quando uma peça não existe no estoque."""


class EstoqueService:
    """Operações de negócio sobre o estoque de peças."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def adicionar_peca(self, nome: str, quantidade: int) -> Peca:
        """Adiciona uma peça, somando quantidade se já existir."""
        nome = (nome or "").strip().upper()
        if not nome:
            raise ValueError("O campo Nome da Peça é obrigatório!")

        try:
            quantidade = int(quantidade)
        except (TypeError, ValueError):
            raise ValueError("A quantidade deve ser um número inteiro.")
        if quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa.")

        session = self.session_factory()
        try:
            existente = session.query(Peca).filter_by(nome=nome).first()
            if existente:
                existente.quantidade += quantidade
                peca = existente
            else:
                peca = Peca(nome=nome, quantidade=quantidade)
                session.add(peca)
            session.commit()
            session.refresh(peca)
            return peca
        except Exception:
            session.rollback()
            raise
        finally:
            self.session_factory.remove()

    def listar_pecas(self, filtro: str = "") -> list[Peca]:
        """Lista peças do estoque, com filtro opcional por nome."""
        session = self.session_factory()
        try:
            query = session.query(Peca)
            if filtro:
                query = query.filter(Peca.nome.ilike(f"%{filtro}%"))
            return query.order_by(Peca.nome).all()
        finally:
            self.session_factory.remove()

    def obter_peca(self, peca_id: int) -> Peca:
        """Busca uma peça por id."""
        session = self.session_factory()
        try:
            peca = session.get(Peca, peca_id)
            if not peca:
                raise PecaNaoEncontradaError("Peça não encontrada.")
            return peca
        finally:
            self.session_factory.remove()

    def atualizar_quantidade(self, peca_id: int, nova_quantidade: int) -> Peca:
        """Altera a quantidade de uma peça."""
        try:
            nova_quantidade = int(nova_quantidade)
        except (TypeError, ValueError):
            raise ValueError("A quantidade deve ser um número inteiro.")
        if nova_quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa.")

        session = self.session_factory()
        try:
            peca = session.get(Peca, peca_id)
            if not peca:
                raise PecaNaoEncontradaError("Peça não encontrada.")
            peca.quantidade = nova_quantidade
            session.commit()
            session.refresh(peca)
            return peca
        except Exception:
            session.rollback()
            raise
        finally:
            self.session_factory.remove()

    def excluir_peca(self, peca_id: int) -> None:
        """Exclui uma peça do estoque."""
        session = self.session_factory()
        try:
            peca = session.get(Peca, peca_id)
            if not peca:
                raise PecaNaoEncontradaError("Peça não encontrada.")
            session.delete(peca)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            self.session_factory.remove()
