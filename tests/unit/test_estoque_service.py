"""Testes unitários do EstoqueService."""

import pytest

from pws.services.estoque_service import EstoqueService, PecaNaoEncontradaError


@pytest.fixture()
def service(session_factory):
    return EstoqueService(session_factory)


class TestAdicionarPeca:
    def test_adicionar_nova(self, service):
        peca = service.adicionar_peca("Oleo", 10)
        assert peca.id is not None
        assert peca.nome == "OLEO"
        assert peca.quantidade == 10

    def test_soma_quando_existe(self, service):
        service.adicionar_peca("Oleo", 10)
        service.adicionar_peca("Oleo", 5)
        pecas = service.listar_pecas()
        assert len(pecas) == 1
        assert pecas[0].quantidade == 15

    def test_nome_obrigatorio(self, service):
        with pytest.raises(ValueError):
            service.adicionar_peca("", 5)

    def test_quantidade_invalida(self, service):
        with pytest.raises(ValueError):
            service.adicionar_peca("Oleo", "abc")

    def test_quantidade_negativa(self, service):
        with pytest.raises(ValueError):
            service.adicionar_peca("Oleo", -1)


class TestListar:
    def test_lista_vazia(self, service):
        assert service.listar_pecas() == []

    def test_filtro_por_nome(self, service):
        service.adicionar_peca("Filtro de Oleo", 3)
        service.adicionar_peca("Pneu", 4)
        resultado = service.listar_pecas(filtro="filtro")
        assert len(resultado) == 1
        assert resultado[0].nome == "FILTRO DE OLEO"

    def test_ordem_alfabetica(self, service):
        service.adicionar_peca("Zebra", 1)
        service.adicionar_peca("Abacaxi", 1)
        nomes = [p.nome for p in service.listar_pecas()]
        assert nomes == ["ABACAXI", "ZEBRA"]


class TestObter:
    def test_obter_existente(self, service):
        peca = service.adicionar_peca("Oleo", 1)
        assert service.obter_peca(peca.id).nome == "OLEO"

    def test_obter_inexistente(self, service):
        with pytest.raises(PecaNaoEncontradaError):
            service.obter_peca(9999)


class TestAtualizarQuantidade:
    def test_atualizar(self, service):
        peca = service.adicionar_peca("Oleo", 1)
        service.atualizar_quantidade(peca.id, 20)
        assert service.obter_peca(peca.id).quantidade == 20

    def test_quantidade_invalida(self, service):
        peca = service.adicionar_peca("Oleo", 1)
        with pytest.raises(ValueError):
            service.atualizar_quantidade(peca.id, "abc")

    def test_negativa(self, service):
        peca = service.adicionar_peca("Oleo", 1)
        with pytest.raises(ValueError):
            service.atualizar_quantidade(peca.id, -1)

    def test_inexistente(self, service):
        with pytest.raises(PecaNaoEncontradaError):
            service.atualizar_quantidade(9999, 5)


class TestExcluir:
    def test_excluir(self, service):
        peca = service.adicionar_peca("Oleo", 1)
        service.excluir_peca(peca.id)
        assert service.listar_pecas() == []

    def test_excluir_inexistente(self, service):
        with pytest.raises(PecaNaoEncontradaError):
            service.excluir_peca(9999)
