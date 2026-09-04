"""Testes unitários do ServicoService."""

import pytest

from pws.services.servico_service import (
    ServicoJaExisteError,
    ServicoNaoEncontradoError,
    ServicoService,
)


@pytest.fixture()
def service(session_factory):
    return ServicoService(session_factory)


class TestCriarServico:
    def test_sucesso(self, service):
        servico = service.criar_servico("Troca de oleo")
        assert servico.id is not None
        assert servico.nome == "TROCA DE OLEO"

    def test_nome_obrigatorio(self, service):
        with pytest.raises(ValueError):
            service.criar_servico("")

    def test_duplicado(self, service):
        service.criar_servico("Troca de oleo")
        with pytest.raises(ServicoJaExisteError):
            service.criar_servico("TROCA DE OLEO")


class TestListar:
    def test_vazio(self, service):
        assert service.listar_servicos() == []

    def test_varios(self, service):
        service.criar_servico("A")
        service.criar_servico("B")
        assert len(service.listar_servicos()) == 2


class TestObter:
    def test_obter_existente(self, service):
        servico = service.criar_servico("A")
        assert service.obter_servico(servico.id).nome == "A"

    def test_obter_inexistente(self, service):
        with pytest.raises(ServicoNaoEncontradoError):
            service.obter_servico(9999)


class TestExcluir:
    def test_excluir(self, service):
        servico = service.criar_servico("A")
        service.excluir_servico(servico.id)
        assert service.listar_servicos() == []

    def test_excluir_inexistente(self, service):
        with pytest.raises(ServicoNaoEncontradoError):
            service.excluir_servico(9999)
