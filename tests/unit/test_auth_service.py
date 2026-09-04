"""Testes unitários do AuthService."""

import pytest

from pws.services.auth_service import (
    AuthService,
    CredenciaisInvalidasError,
    RespostaIncorretaError,
    UsuarioJaExisteError,
    UsuarioNaoEncontradoError,
    hash_senha,
    verificar_senha,
)


@pytest.fixture()
def service(session_factory):
    return AuthService(session_factory)


class TestHashSenha:
    def test_hash_e_verificacao(self):
        h = hash_senha("minhasenha")
        assert h != b"minhasenha"
        assert verificar_senha("minhasenha", h) is True
        assert verificar_senha("outra", h) is False

    def test_hash_eh_bytes(self):
        assert isinstance(hash_senha("x"), bytes)

    def test_verificar_com_string(self):
        h = hash_senha("abc")
        assert verificar_senha("abc", h.decode("utf-8")) is True


class TestCadastrarUsuario:
    def test_cadastro_sucesso(self, service, session_factory):
        u = service.cadastrar_usuario("Joao", "senha123", "Pergunta?", "Resposta")
        assert u.nome_usuario == "JOAO"
        assert u.id is not None

        # a resposta deve estar hasheada, não em texto puro
        assert not hasattr(u, "_resposta_seguranca_hash") is False
        assert u.verificar_resposta("RESPOSTA") is True

    def test_nome_obrigatorio(self, service):
        with pytest.raises(ValueError):
            service.cadastrar_usuario("", "senha", "P", "R")

    def test_senha_obrigatoria(self, service):
        with pytest.raises(ValueError):
            service.cadastrar_usuario("Joao", "", "P", "R")

    def test_senha_curta(self, service):
        with pytest.raises(ValueError):
            service.cadastrar_usuario("Joao", "123", "P", "R")

    def test_pergunta_obrigatoria(self, service):
        with pytest.raises(ValueError):
            service.cadastrar_usuario("Joao", "senha123", "", "R")

    def test_resposta_obrigatoria(self, service):
        with pytest.raises(ValueError):
            service.cadastrar_usuario("Joao", "senha123", "P", "")

    def test_duplicado(self, service):
        service.cadastrar_usuario("Joao", "senha123", "P", "R")
        with pytest.raises(UsuarioJaExisteError):
            service.cadastrar_usuario("joao", "senha123", "P", "R")


class TestAutenticar:
    def test_login_sucesso(self, service):
        service.cadastrar_usuario("Joao", "senha123", "P", "R")
        usuario = service.autenticar("JOAO", "senha123")
        assert usuario.nome_usuario == "JOAO"

    def test_login_usuario_inexistente(self, service):
        with pytest.raises(CredenciaisInvalidasError):
            service.autenticar("naoexiste", "senha")

    def test_login_senha_errada(self, service):
        service.cadastrar_usuario("Joao", "senha123", "P", "R")
        with pytest.raises(CredenciaisInvalidasError):
            service.autenticar("JOAO", "errada")

    def test_campos_vazios(self, service):
        with pytest.raises(CredenciaisInvalidasError):
            service.autenticar("", "")


class TestBuscarEVerificarExiste:
    def test_buscar_existente(self, service):
        service.cadastrar_usuario("Joao", "senha123", "P", "R")
        assert service.buscar_usuario("joao") is not None
        assert service.verificar_existe("JOAO") is True

    def test_buscar_inexistente(self, service):
        assert service.buscar_usuario("nada") is None
        assert service.verificar_existe("nada") is False


class TestVerificarResposta:
    def test_resposta_correta(self, service):
        service.cadastrar_usuario("Joao", "senha123", "P", "Resposta")
        assert service.verificar_resposta("JOAO", "resposta") is True

    def test_resposta_incorreta(self, service):
        service.cadastrar_usuario("Joao", "senha123", "P", "Resposta")
        assert service.verificar_resposta("JOAO", "errado") is False

    def test_usuario_inexistente(self, service):
        with pytest.raises(UsuarioNaoEncontradoError):
            service.verificar_resposta("nada", "r")

    def test_resposta_vazia(self, service):
        service.cadastrar_usuario("Joao", "senha123", "P", "Resposta")
        with pytest.raises(ValueError):
            service.verificar_resposta("JOAO", "")


class TestRedefinirSenha:
    def test_redefinir_sucesso(self, service):
        service.cadastrar_usuario("Joao", "senha123", "P", "R")
        service.redefinir_senha("JOAO", "novaSenha")
        assert service.autenticar("JOAO", "novaSenha").nome_usuario == "JOAO"

    def test_redefinir_usuario_inexistente(self, service):
        with pytest.raises(UsuarioNaoEncontradoError):
            service.redefinir_senha("nada", "novaSenha")

    def test_redefinir_senha_vazia(self, service):
        service.cadastrar_usuario("Joao", "senha123", "P", "R")
        with pytest.raises(ValueError):
            service.redefinir_senha("JOAO", "")
