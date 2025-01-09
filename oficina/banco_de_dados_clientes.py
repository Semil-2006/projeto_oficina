from sqlalchemy import create_engine, Column, Integer, String, Sequence, Float,Date,Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=False, nullable=True)
    email = Column(String(100), nullable=True)
    telefone = Column(String(15), nullable=True)
    data_entrada = Column(Date, nullable=False)
    valor = Column(Float, nullable=True)
    marca_carro = Column(String(50), nullable=False)
    placa_carro = Column(String(10), unique=False, nullable=False)
    forma_pagamento = Column(Text, nullable=True)
    data_saida = Column(Date, nullable=True)
    pecas_utilizadas = Column(Text, nullable=True)
    # quantidade_pecas = Column(Integer, nullable=True)


    def __init__(self, nome,cpf,email,telefone,data_entrada,valor,marca_carro,placa_carro,forma_pagamento, data_saida,
                 pecas_utilizadas):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.data_entrada = data_entrada
        self.valor = valor
        self.marca_carro = marca_carro
        self.placa_carro = placa_carro
        self.forma_pagamento = forma_pagamento
        self.data_saida = data_saida
        self.pecas_utilizadas = pecas_utilizadas


def inicializar_banco_de_dados(url_banco='sqlite:///clientes.db'):
    engine = create_engine(url_banco)
    Base.metadata.create_all(engine)
    return engine


def obter_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

engine = inicializar_banco_de_dados()
secao = obter_session(engine)


from datetime import date

# Supondo que você já tenha o código da classe Cliente, do banco e da sessão
'''
# Criando 20 clientes diferentes
clientes = [
    Cliente(nome="João Silva", cpf="123.456.789-00", email="joao.silva@email.com", telefone="1234567890", data_entrada=date(2025, 1, 1), valor=1500.50, marca_carro="Toyota", placa_carro="ABC1234", forma_pagamento="Cartão", data_saida=date(2025, 1, 3), pecas_utilizadas="Pneu, óleo"),
    Cliente(nome="Maria Souza", cpf="234.567.890-11", email="maria.souza@email.com", telefone="2345678901", data_entrada=date(2025, 1, 2), valor=2200.75, marca_carro="Honda", placa_carro="XYZ5678", forma_pagamento="Dinheiro", data_saida=date(2025, 1, 4), pecas_utilizadas="Bateria, filtro de ar"),
    Cliente(nome="Carlos Oliveira", cpf="345.678.901-22", email="carlos.oliveira@email.com", telefone="3456789012", data_entrada=date(2025, 1, 3), valor=1800.00, marca_carro="Ford", placa_carro="LMN9012", forma_pagamento="Cheque", data_saida=date(2025, 1, 5), pecas_utilizadas="Amortecedor"),
    Cliente(nome="Ana Costa", cpf="456.789.012-33", email="ana.costa@email.com", telefone="4567890123", data_entrada=date(2025, 1, 4), valor=1200.00, marca_carro="Chevrolet", placa_carro="OPQ3456", forma_pagamento="Cartão", data_saida=date(2025, 1, 6), pecas_utilizadas="Filtro de combustível, óleo"),
    Cliente(nome="Ricardo Pereira", cpf="567.890.123-44", email="ricardo.pereira@email.com", telefone="5678901234", data_entrada=date(2025, 1, 5), valor=2100.30, marca_carro="Fiat", placa_carro="RST6789", forma_pagamento="Dinheiro", data_saida=date(2025, 1, 7), pecas_utilizadas="Correia dentada, vela de ignição"),
    Cliente(nome="Fernanda Lima", cpf="678.901.234-55", email="fernanda.lima@email.com", telefone="6789012345", data_entrada=date(2025, 1, 6), valor=950.25, marca_carro="Volkswagen", placa_carro="UVW1234", forma_pagamento="Cheque", data_saida=date(2025, 1, 8), pecas_utilizadas="Pastilhas de freio"),
    Cliente(nome="Eduardo Santos", cpf="789.012.345-66", email="eduardo.santos@email.com", telefone="7890123456", data_entrada=date(2025, 1, 7), valor=1700.90, marca_carro="Nissan", placa_carro="XYZ4321", forma_pagamento="Cartão", data_saida=date(2025, 1, 9), pecas_utilizadas="Disco de freio, filtro de óleo"),
    Cliente(nome="Patrícia Rocha", cpf="890.123.456-77", email="patricia.rocha@email.com", telefone="8901234567", data_entrada=date(2025, 1, 8), valor=2000.00, marca_carro="Renault", placa_carro="ABC9876", forma_pagamento="Dinheiro", data_saida=date(2025, 1, 10), pecas_utilizadas="Escapamento, óleo"),
    Cliente(nome="Vinícius Ferreira", cpf="901.234.567-88", email="vinicius.ferreira@email.com", telefone="9012345678", data_entrada=date(2025, 1, 9), valor=1100.55, marca_carro="Hyundai", placa_carro="DEF2468", forma_pagamento="Cheque", data_saida=date(2025, 1, 11), pecas_utilizadas="Correia de alternador"),
    Cliente(nome="Juliana Alves", cpf="012.345.678-99", email="juliana.alves@email.com", telefone="0123456789", data_entrada=date(2025, 1, 10), valor=1900.00, marca_carro="Peugeot", placa_carro="GHI1357", forma_pagamento="Cartão", data_saida=date(2025, 1, 12), pecas_utilizadas="Amortecedor"),
    Cliente(nome="Fábio Martins", cpf="123.456.789-01", email="fabio.martins@email.com", telefone="1234567890", data_entrada=date(2025, 1, 11), valor=1500.00, marca_carro="Kia", placa_carro="JKL2580", forma_pagamento="Dinheiro", data_saida=date(2025, 1, 13), pecas_utilizadas="Farois"),
    Cliente(nome="Marta Costa", cpf="234.567.890-12", email="marta.costa@email.com", telefone="2345678901", data_entrada=date(2025, 1, 12), valor=1300.00, marca_carro="Mitsubishi", placa_carro="LMN3691", forma_pagamento="Cheque", data_saida=date(2025, 1, 14), pecas_utilizadas="Filtro de óleo, velas de ignição"),
    Cliente(nome="Gustavo Silva", cpf="345.678.901-23", email="gustavo.silva@email.com", telefone="3456789012", data_entrada=date(2025, 1, 13), valor=2200.00, marca_carro="BMW", placa_carro="OPQ4802", forma_pagamento="Cartão", data_saida=date(2025, 1, 15), pecas_utilizadas="Rodas, pneus"),
    Cliente(nome="Raquel Pinto", cpf="456.789.012-34", email="raquel.pinto@email.com", telefone="4567890123", data_entrada=date(2025, 1, 14), valor=1600.00, marca_carro="Mercedes", placa_carro="RST5913", forma_pagamento="Dinheiro", data_saida=date(2025, 1, 16), pecas_utilizadas="Jogo de suspensão"),
    Cliente(nome="Leonardo Souza", cpf="567.890.123-45", email="leonardo.souza@email.com", telefone="5678901234", data_entrada=date(2025, 1, 15), valor=2300.00, marca_carro="Audi", placa_carro="UVW6024", forma_pagamento="Cheque", data_saida=date(2025, 1, 17), pecas_utilizadas="Escapamento, filtro de ar"),
    Cliente(nome="Carla Mendes", cpf="678.901.234-56", email="carla.mendes@email.com", telefone="6789012345", data_entrada=date(2025, 1, 16), valor=1900.00, marca_carro="Volvo", placa_carro="XYZ7135", forma_pagamento="Cartão", data_saida=date(2025, 1, 18), pecas_utilizadas="Filtro de combustível"),
    Cliente(nome="Gustavo Oliveira", cpf="789.012.345-67", email="gustavo.oliveira@email.com", telefone="7890123456", data_entrada=date(2025, 1, 17), valor=2100.00, marca_carro="Toyota", placa_carro="ABC8247", forma_pagamento="Dinheiro", data_saida=date(2025, 1, 19), pecas_utilizadas="Jogo de pneus"),
    Cliente(nome="Tatiane Dias", cpf="890.123.456-78", email="tatiane.dias@email.com", telefone="8901234567", data_entrada=date(2025, 1, 18), valor=1800.00, marca_carro="Chevrolet", placa_carro="DEF9358", forma_pagamento="Cheque", data_saida=date(2025, 1, 20), pecas_utilizadas="Faróis, bateria"),
    Cliente(nome="Ricardo Ramos", cpf="901.234.567-89", email="ricardo.ramos@email.com", telefone="9012345678", data_entrada=date(2025, 1, 19), valor=1200.00, marca_carro="Honda", placa_carro="GHI0469", forma_pagamento="Cartão", data_saida=date(2025, 1, 21), pecas_utilizadas="Pastilhas de freio"),
    Cliente(nome="Luiz Henrique", cpf="111.222.333-44", email="luiz.henrique@email.com", telefone="9876543210",
            data_entrada=date(2024, 1, 15), valor=1500.00, marca_carro="Toyota", placa_carro="ABC5678",
            forma_pagamento="Dinheiro", data_saida=date(2024, 1, 20), pecas_utilizadas="Óleo, filtro de ar"),
    Cliente(nome="Camila Ramos", cpf="222.333.444-55", email="camila.ramos@email.com", telefone="8765432109",
            data_entrada=date(2024, 2, 10), valor=2100.50, marca_carro="Honda", placa_carro="XYZ7890",
            forma_pagamento="Cartão", data_saida=date(2024, 2, 15), pecas_utilizadas="Pastilhas de freio"),
    Cliente(nome="Bruno Almeida", cpf="333.444.555-66", email="bruno.almeida@email.com", telefone="7654321098",
            data_entrada=date(2024, 3, 5), valor=1700.75, marca_carro="Ford", placa_carro="LMN3456",
            forma_pagamento="Cheque", data_saida=date(2024, 3, 10), pecas_utilizadas="Correia dentada"),
    Cliente(nome="Beatriz Ferreira", cpf="444.555.666-77", email="beatriz.ferreira@email.com", telefone="6543210987",
            data_entrada=date(2024, 4, 20), valor=2000.00, marca_carro="Chevrolet", placa_carro="OPQ9012",
            forma_pagamento="Dinheiro", data_saida=date(2024, 4, 25), pecas_utilizadas="Amortecedor"),
    Cliente(nome="Rodrigo Nunes", cpf="555.666.777-88", email="rodrigo.nunes@email.com", telefone="5432109876",
            data_entrada=date(2024, 5, 10), valor=1850.25, marca_carro="Fiat", placa_carro="RST2345",
            forma_pagamento="Cartão", data_saida=date(2024, 5, 15), pecas_utilizadas="Disco de freio"),
    Cliente(nome="Sabrina Vieira", cpf="666.777.888-99", email="sabrina.vieira@email.com", telefone="4321098765",
            data_entrada=date(2024, 6, 25), valor=1900.00, marca_carro="Volkswagen", placa_carro="UVW6789",
            forma_pagamento="Cheque", data_saida=date(2024, 6, 30), pecas_utilizadas="Filtro de combustível"),
    Cliente(nome="André Oliveira", cpf="777.888.999-00", email="andre.oliveira@email.com", telefone="3210987654",
            data_entrada=date(2024, 7, 5), valor=2200.40, marca_carro="Nissan", placa_carro="XYZ4567",
            forma_pagamento="Dinheiro", data_saida=date(2024, 7, 10), pecas_utilizadas="Bateria"),
    Cliente(nome="Carolina Martins", cpf="888.999.000-11", email="carolina.martins@email.com", telefone="2109876543",
            data_entrada=date(2024, 8, 18), valor=1300.30, marca_carro="Renault", placa_carro="ABC8901",
            forma_pagamento="Cartão", data_saida=date(2024, 8, 23), pecas_utilizadas="Óleo, filtro de ar"),
    Cliente(nome="Marcelo Silva", cpf="999.000.111-22", email="marcelo.silva@email.com", telefone="1098765432",
            data_entrada=date(2024, 9, 12), valor=1950.00, marca_carro="Hyundai", placa_carro="DEF5678",
            forma_pagamento="Cheque", data_saida=date(2024, 9, 17), pecas_utilizadas="Velas de ignição"),
    Cliente(nome="Larissa Dias", cpf="000.111.222-33", email="larissa.dias@email.com", telefone="9876543211",
            data_entrada=date(2024, 10, 8), valor=1400.00, marca_carro="Peugeot", placa_carro="GHI2468",
            forma_pagamento="Dinheiro", data_saida=date(2024, 10, 13), pecas_utilizadas="Amortecedor"),
    Cliente(nome="Eduardo Lima", cpf="111.222.333-44", email="eduardo.lima@email.com", telefone="8765432110",
            data_entrada=date(2024, 11, 3), valor=2000.00, marca_carro="Kia", placa_carro="JKL1357",
            forma_pagamento="Cartão", data_saida=date(2024, 11, 8), pecas_utilizadas="Disco de freio"),
    Cliente(nome="Viviane Mendes", cpf="222.333.444-55", email="viviane.mendes@email.com", telefone="7654321109",
            data_entrada=date(2024, 12, 15), valor=1550.75, marca_carro="Mitsubishi", placa_carro="LMN9876",
            forma_pagamento="Dinheiro", data_saida=date(2024, 12, 20), pecas_utilizadas="Óleo, filtro de óleo")
]

for cliente in clientes:
    secao.add(cliente)

secao.commit()

from fpdf import FPDF
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# Configurar o PDF
class PDF(FPDF):
    def header(self):
        # Fundo azul em toda a página
        self.set_fill_color(59, 55, 126)  # Cor #3B377E
        self.rect(0, 0, self.w, self.h, 'F')  # Preencher toda a página
        self.set_font('Arial', 'I', 37)
        self.set_text_color(255, 255, 255)  # Texto branco
        self.set_y(10)
        self.cell(0, 20, 'Orçamento - PWS DO IRMÃO', border=False, ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(255, 255, 255)  # Texto branco no rodapé
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# Conexão com o banco de dados
engine = inicializar_banco_de_dados()
Session = sessionmaker(bind=engine)
session = Session()

# Consultar os dados do cliente
cliente_id = 1  # Substituir pelo ID desejado
cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()

if cliente:
    # Gerar o PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    # Adicionar a imagem do carro centralizada
    img_path = '/home/semil/Área de Trabalho/oficina/img_do_carro.png'
    img_width = 75.7  # Largura em mm
    img_height = 39.4  # Altura em mm
    img_x = (pdf.w - img_width) / 2  # Calcular posição X para centralizar
    img_y = 50  # Posição Y
    pdf.image(img_path, x=img_x, y=img_y, w=img_width, h=img_height)

    # Criar tabela para dados do cliente
    pdf.set_y(100)
    pdf.set_fill_color(255, 255, 255)  # Branco para células da tabela
    pdf.set_text_color(0, 0, 0)  # Texto preto para células

    dados = [
        ("NOME", cliente.nome),
        ("CPF", cliente.cpf),
        ("EMAIL", cliente.email),
        ("TELEFONE", cliente.telefone),
        ("MARCA DO CARRO", cliente.marca_carro),
        ("PLACA DO CARRO", cliente.placa_carro),
        ("Peças Utilizadas", cliente.pecas_utilizadas),
        ("Valor Total", f"R${cliente.valor:.2f}"),
        ("Forma de Pagamento", cliente.forma_pagamento),
    ]

    for campo, valor in dados:
        pdf.cell(50, 10, campo, border=1, align='L', fill=True)
        pdf.cell(0, 10, valor, border=1, ln=True, align='L')

    # Mensagem final
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(255, 255, 255)  # Texto branco para mensagem final
    pdf.multi_cell(0, 10, 'Em caso de dúvidas, não hesite em nos contatar! Estamos à disposição para esclarecer qualquer questão e garantir que você tenha a melhor experiência com a PWS.')

    # Salvar o PDF
    pdf.output('orcamento.pdf')
    print("PDF gerado com sucesso!")
else:
    print("Cliente não encontrado!")'''
