"""Testes unitários dos formatadores."""

from pws.formatadores import (
    formatar_cpf,
    formatar_placa,
    formatar_telefone,
    formatar_valor_entrada,
    formatar_valor_monetario,
)


class TestFormatarTelefone:
    def test_11_digitos(self):
        assert formatar_telefone("11912345678") == "(11) 91234-5678"

    def test_10_digitos(self):
        assert formatar_telefone("1112345678") == "(11) 1234-5678"

    def test_vazio(self):
        assert formatar_telefone("") == ""

    def test_ja_formatado(self):
        assert formatar_telefone("(11) 91234-5678") == "(11) 91234-5678"

    def test_idempotente_durante_digitacao(self):
        """Réplica o comportamento da GUI: reformatar o valor exibido a cada tecla."""
        valor = ""
        for tecla in "11912345678":
            valor += tecla
            valor = formatar_telefone(valor)
        assert valor == "(11) 91234-5678"


class TestFormatarPlaca:
    def test_placa_antiga(self):
        assert formatar_placa("ABC1234") == "ABC-1234"

    def test_placa_encurta_para_7(self):
        assert formatar_placa("ABC1234567") == "ABC-1234"

    def test_placa_curta(self):
        assert formatar_placa("AB") == "AB"

    def test_placa_com_hifen_removido(self):
        assert formatar_placa("abc-1234") == "ABC-1234"


class TestFormatarCpf:
    def test_cpf_completo(self):
        assert formatar_cpf("52998224725") == "529.982.247-25"

    def test_cpf_parcial(self):
        assert formatar_cpf("529982") == "529.982"

    def test_cpf_vazio(self):
        assert formatar_cpf("") == ""

    def test_cpf_remove_formatacao(self):
        assert formatar_cpf("529.982.247-25") == "529.982.247-25"


class TestFormatarValorEntrada:
    def test_formatar_centavos(self):
        assert formatar_valor_entrada("123456") == "R$ 1.234,56"

    def test_sem_valor(self):
        assert formatar_valor_entrada("") == "R$ 0,00"

    def test_centavos_sozinhos(self):
        assert formatar_valor_entrada("50") == "R$ 0,50"


class TestFormatarValorMonetario:
    def test_virgula_e_ponto(self):
        assert formatar_valor_monetario(1234.5) == "R$ 1.234,50"

    def test_inteiro(self):
        assert formatar_valor_monetario(100) == "R$ 100,00"
