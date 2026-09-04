"""Serviço de gestão de clientes: CRUD, busca e paginação."""
from __future__ import annotations

from datetime import date
from typing import Optional

from pws.models import Cliente


class ClienteNaoEncontradoError(Exception):
    """Lançada quando o cliente não existe."""


class ClienteService:
    """Operações de negócio sobre clientes."""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def criar_cliente(
        self,
        *,
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
    ) -> Cliente:
        """Registra um novo cliente validando os campos obrigatórios."""
        nome = (nome or "").strip().upper()
        marca_carro = (marca_carro or "").strip().upper()
        placa_carro = (placa_carro or "").strip().upper()

        if not nome:
            raise ValueError("O campo Nome do Cliente é obrigatório!")
        if data_entrada is None:
            raise ValueError("O campo Data de Entrada é obrigatório!")
        if not marca_carro:
            raise ValueError("O campo Marca do Carro é obrigatório!")
        if not placa_carro:
            raise ValueError("O campo Placa do Carro é obrigatório!")

        cliente = Cliente(
            nome=nome,
            data_entrada=data_entrada,
            marca_carro=marca_carro,
            placa_carro=placa_carro,
            cpf=cpf or None,
            email=email or None,
            telefone=telefone or None,
            valor=valor,
            forma_pagamento=forma_pagamento,
            data_saida=data_saida,
            pecas_utilizadas=pecas_utilizadas,
        )

        session = self.session_factory()
        try:
            session.add(cliente)
            session.commit()
            session.refresh(cliente)
            return cliente
        except Exception:
            session.rollback()
            raise
        finally:
            self.session_factory.remove()

    def criar_clientes_em_massa(self, dados: list[dict]) -> int:
        """Insere vários clientes em uma única transação (bulk insert).

        Usado em cenários de carga/seed para evitar commit por registro.
        Retorna o número de clientes inseridos.
        """
        if not dados:
            return 0
        session = self.session_factory()
        try:
            objs = []
            for item in dados:
                nome = (item.get("nome") or "").strip().upper()
                marca = (item.get("marca_carro") or "").strip().upper()
                placa = (item.get("placa_carro") or "").strip().upper()
                if not nome or not marca or not placa or item.get("data_entrada") is None:
                    continue
                objs.append(
                    Cliente(
                        nome=nome,
                        data_entrada=item["data_entrada"],
                        marca_carro=marca,
                        placa_carro=placa,
                        cpf=item.get("cpf"),
                        email=item.get("email"),
                        telefone=item.get("telefone"),
                        valor=item.get("valor"),
                        forma_pagamento=item.get("forma_pagamento"),
                        data_saida=item.get("data_saida"),
                        pecas_utilizadas=item.get("pecas_utilizadas"),
                    )
                )
            if objs:
                session.add_all(objs)
                session.commit()
            return len(objs)
        except Exception:
            session.rollback()
            raise
        finally:
            self.session_factory.remove()

    def listar_clientes(
        self, busca: str = "", pagina: int = 0, por_pagina: int = 10
    ) -> tuple[list[Cliente], int]:
        """Retorna (clientes, total) com busca opcional e paginação."""
        session = self.session_factory()
        try:
            query = session.query(Cliente)
            if busca:
                query = query.filter(Cliente.nome.ilike(f"%{busca}%"))
            total = query.count()
            clientes = (
                query.order_by(Cliente.data_entrada.desc())
                .offset(pagina * por_pagina)
                .limit(por_pagina)
                .all()
            )
            return clientes, total
        finally:
            self.session_factory.remove()

    def obter_cliente(self, cliente_id: int) -> Cliente:
        """Busca um cliente por id."""
        session = self.session_factory()
        try:
            cliente = session.get(Cliente, cliente_id)
            if not cliente:
                raise ClienteNaoEncontradoError("Cliente não encontrado.")
            return cliente
        finally:
            self.session_factory.remove()

    def atualizar_cliente(
        self, cliente_id: int, dados: dict
    ) -> Cliente:
        """Atualiza campos de um cliente existente."""
        session = self.session_factory()
        try:
            cliente = session.get(Cliente, cliente_id)
            if not cliente:
                raise ClienteNaoEncontradoError("Cliente não encontrado.")
            for chave, valor in dados.items():
                if hasattr(cliente, chave):
                    setattr(cliente, chave, valor)
            session.commit()
            session.refresh(cliente)
            return cliente
        except Exception:
            session.rollback()
            raise
        finally:
            self.session_factory.remove()

    def excluir_cliente(self, cliente_id: int) -> None:
        """Exclui um cliente pelo id."""
        session = self.session_factory()
        try:
            cliente = session.get(Cliente, cliente_id)
            if not cliente:
                raise ClienteNaoEncontradoError("Cliente não encontrado.")
            session.delete(cliente)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            self.session_factory.remove()

    def para_dict(self, cliente: Cliente) -> dict:
        """Serializa um Cliente para um dicionário (útil para UI/PDF)."""
        return {
            "id": cliente.id,
            "nome": cliente.nome,
            "cpf": cliente.cpf,
            "email": cliente.email,
            "telefone": cliente.telefone,
            "data_entrada": cliente.data_entrada,
            "valor": cliente.valor,
            "marca_carro": cliente.marca_carro,
            "placa_carro": cliente.placa_carro,
            "forma_pagamento": cliente.forma_pagamento,
            "data_saida": cliente.data_saida,
            "pecas_utilizadas": cliente.pecas_utilizadas,
        }
