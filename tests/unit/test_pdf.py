"""Testes unitários da geração de PDF."""

import os

from pws.pdf import montar_dados_orcamento, gerar_pdf_para_caminho


def _cliente(overrides=None):
    dados = {
        "nome": "João Silva",
        "cpf": "529.982.247-25",
        "email": "joao@example.com",
        "telefone": "(11) 91234-5678",
        "marca_carro": "Toyota",
        "placa_carro": "ABC1234",
        "pecas_utilizadas": "Oleo, filtro",
        "valor": 1500.50,
        "forma_pagamento": "CARTAO",
    }
    if overrides:
        dados.update(overrides)
    return dados


class TestMontarDadosOrcamento:
    def test_campos_preenchidos(self):
        dados = montar_dados_orcamento(_cliente())
        valores = dict(dados)
        assert valores["NOME"] == "João Silva"
        assert valores["Valor Total"] == "R$1500.50"

    def test_campos_ausentes_nao_informado(self):
        dados = montar_dados_orcamento(_cliente({
            "cpf": None, "email": None, "valor": None,
        }))
        valores = dict(dados)
        assert valores["CPF"] == "Não informado"
        assert valores["Valor Total"] == "Não informado"

    def test_ordem_dos_campos(self):
        dados = montar_dados_orcamento(_cliente())
        campos = [c for c, _ in dados]
        assert campos == [
            "NOME", "CPF", "EMAIL", "TELEFONE", "MARCA DO CARRO",
            "PLACA DO CARRO", "Peças Utilizadas", "Valor Total",
            "Forma de Pagamento",
        ]


class TestGerarPDF:
    def test_gera_arquivo_pdf(self, tmp_path):
        caminho = os.path.join(str(tmp_path), "orcamento.pdf")
        gerar_pdf_para_caminho(_cliente(), caminho)
        assert os.path.exists(caminho)
        with open(caminho, "rb") as f:
            cabecalho = f.read(5)
        assert cabecalho == b"%PDF-"
