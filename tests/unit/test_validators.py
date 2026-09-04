"""Testes unitários dos validadores."""

from pws.validators import (
    converter_valor_para_float,
    validar_cpf,
    validar_email,
    validar_placa,
    validar_telefone,
    validar_valor,
)


class TestValidarCpf:
    def test_cpf_valido(self):
        assert validar_cpf("529.982.247-25") is True

    def test_cpf_somente_digitos(self):
        assert validar_cpf("52998224725") is True

    def test_cpf_invalido(self):
        assert validar_cpf("111.111.111-11") is False

    def test_cpf_curto(self):
        assert validar_cpf("1234") is False

    def test_cpf_vazio(self):
        assert validar_cpf("") is False

    def test_cpf_none(self):
        assert validar_cpf(None) is False

    def test_cpf_com_letras(self):
        assert validar_cpf("abc.def.ghi-jk") is False


class TestValidarEmail:
    def test_email_valido(self):
        assert validar_email("joao@example.com") is True

    def test_email_sem_arroba(self):
        assert validar_email("joaoexample.com") is False

    def test_email_sem_ponto(self):
        assert validar_email("joao@examplecom") is False

    def test_email_vazio(self):
        assert validar_email("") is False

    def test_email_none(self):
        assert validar_email(None) is False


class TestValidarTelefone:
    def test_telefone_10_digitos(self):
        assert validar_telefone("(11) 1234-5678") is True

    def test_telefone_11_digitos(self):
        assert validar_telefone("(11) 91234-5678") is True

    def test_telefone_curto(self):
        assert validar_telefone("123") is False

    def test_telefone_vazio(self):
        assert validar_telefone("") is False


class TestValidarPlaca:
    def test_placa_antiga(self):
        assert validar_placa("ABC1234") is True

    def test_placa_mercosul(self):
        assert validar_placa("ABC1D23") is True

    def test_placa_curta(self):
        assert validar_placa("ABC123") is False

    def test_placa_com_hifen(self):
        assert validar_placa("ABC-1234") is True

    def test_placa_invalida(self):
        assert validar_placa("1234567") is False


class TestValidarValor:
    def test_valor_none_eh_aceito(self):
        assert validar_valor(None) is True

    def test_valor_positivo(self):
        assert validar_valor(10.5) is True

    def test_valor_zero(self):
        assert validar_valor(0) is True

    def test_valor_negativo(self):
        assert validar_valor(-1) is False

    def test_valor_texto_invalido(self):
        assert validar_valor("abc") is False


class TestConverterValor:
    def test_converte_br(self):
        assert converter_valor_para_float("R$ 1.234,56") == 1234.56

    def test_converte_simples(self):
        assert converter_valor_para_float("100,50") == 100.50

    def test_vazio_lanca_erro(self):
        try:
            converter_valor_para_float("")
            assert False, "deveria lançar"
        except ValueError:
            pass

    def test_none_lanca_erro(self):
        try:
            converter_valor_para_float(None)
            assert False, "deveria lançar"
        except ValueError:
            pass
