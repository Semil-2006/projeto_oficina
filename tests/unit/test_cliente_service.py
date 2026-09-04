"""Testes unitários do ClienteService."""

from datetime import date

import pytest

from pws.services.cliente_service import ClienteNaoEncontradoError, ClienteService


@pytest.fixture()
def service(session_factory):
    return ClienteService(session_factory)


def _criar(service, **kwargs):
    dados = {
        "nome": "João Silva",
        "data_entrada": date(2025, 1, 15),
        "marca_carro": "Toyota",
        "placa_carro": "ABC1234",
    }
    dados.update(kwargs)
    return service.criar_cliente(**dados)


class TestCriarCliente:
    def test_sucesso(self, service):
        cliente = _criar(service, valor=1500.50, forma_pagamento="CARTAO")
        assert cliente.id is not None
        assert cliente.nome == "JOÃO SILVA"

    def test_nome_obrigatorio(self, service):
        with pytest.raises(ValueError):
            _criar(service, nome="")

    def test_data_obrigatoria(self, service):
        with pytest.raises(ValueError):
            _criar(service, data_entrada=None)

    def test_marca_obrigatoria(self, service):
        with pytest.raises(ValueError):
            _criar(service, marca_carro="")

    def test_placa_obrigatoria(self, service):
        with pytest.raises(ValueError):
            _criar(service, placa_carro="")

    def test_campos_opcionais_none(self, service):
        cliente = _criar(service)
        assert cliente.cpf is None
        assert cliente.email is None

    def test_esta_pago(self, service):
        pago = _criar(service, forma_pagamento="PIX")
        nao_pago = _criar(service, nome="Maria")
        assert pago.esta_pago() is True
        assert nao_pago.esta_pago() is False


class TestListar:
    def test_lista_vazia(self, service):
        clientes, total = service.listar_clientes()
        assert clientes == []
        assert total == 0

    def test_lista_com_paginacao(self, service):
        for i in range(15):
            _criar(service, nome=f"Cliente {i}")
        pagina1, total = service.listar_clientes(por_pagina=10)
        pagina2, _ = service.listar_clientes(pagina=1, por_pagina=10)
        assert total == 15
        assert len(pagina1) == 10
        assert len(pagina2) == 5

    def test_busca_por_nome(self, service):
        _criar(service, nome="Marcos Pereira")
        _criar(service, nome="Ana Souza")
        clientes, total = service.listar_clientes(busca="pereira")
        assert total == 1
        assert clientes[0].nome == "MARCOS PEREIRA"


class TestObter:
    def test_obter_existente(self, service):
        cliente = _criar(service)
        obtido = service.obter_cliente(cliente.id)
        assert obtido.id == cliente.id

    def test_obter_inexistente(self, service):
        with pytest.raises(ClienteNaoEncontradoError):
            service.obter_cliente(9999)


class TestAtualizar:
    def test_atualizar_sucesso(self, service):
        cliente = _criar(service)
        service.atualizar_cliente(cliente.id, {"valor": 2000.0, "forma_pagamento": "DINHEIRO"})
        atualizado = service.obter_cliente(cliente.id)
        assert atualizado.valor == 2000.0
        assert atualizado.forma_pagamento == "DINHEIRO"

    def test_atualizar_inexistente(self, service):
        with pytest.raises(ClienteNaoEncontradoError):
            service.atualizar_cliente(9999, {"valor": 1})

    def test_atualizar_campo_invalido_ignorado(self, service):
        cliente = _criar(service)
        service.atualizar_cliente(cliente.id, {"campo_inexistente": 1})
        assert service.obter_cliente(cliente.id).nome == "JOÃO SILVA"


class TestExcluir:
    def test_excluir_sucesso(self, service):
        cliente = _criar(service)
        service.excluir_cliente(cliente.id)
        clientes, total = service.listar_clientes()
        assert total == 0

    def test_excluir_inexistente(self, service):
        with pytest.raises(ClienteNaoEncontradoError):
            service.excluir_cliente(9999)


class TestParaDict:
    def test_para_dict(self, service):
        cliente = _criar(service, valor=100.0, cpf="52998224725")
        dados = service.para_dict(cliente)
        assert dados["nome"] == "JOÃO SILVA"
        assert dados["valor"] == 100.0
        assert dados["placa_carro"] == "ABC1234"


class TestCriarEmMassa:
    def test_cria_varios(self, service):
        dados = [
            {"nome": "A", "data_entrada": date(2025, 1, 1), "marca_carro": "X",
             "placa_carro": "ABC1234"},
            {"nome": "B", "data_entrada": date(2025, 1, 2), "marca_carro": "Y",
             "placa_carro": "XYZ9876"},
        ]
        assert service.criar_clientes_em_massa(dados) == 2
        _, total = service.listar_clientes()
        assert total == 2

    def test_lista_vazia(self, service):
        assert service.criar_clientes_em_massa([]) == 0

    def test_ignora_invalidos(self, service):
        dados = [
            {"nome": "", "data_entrada": date(2025, 1, 1), "marca_carro": "X",
             "placa_carro": "ABC1234"},
            {"nome": "OK", "data_entrada": date(2025, 1, 1), "marca_carro": "X",
             "placa_carro": "ABC1234"},
        ]
        assert service.criar_clientes_em_massa(dados) == 1
        _, total = service.listar_clientes()
        assert total == 1
