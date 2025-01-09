from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random

Base = declarative_base()


class Peca(Base):
    __tablename__ = 'pecas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)

    def __init__(self, nome, quantidade):
        self.nome = nome
        self.quantidade = quantidade


def inicializar_banco_de_dados(url_banco='sqlite:///pecas.db'):
    engine = create_engine(url_banco)
    Base.metadata.create_all(engine)
    return engine


def obter_seccao(engine):
    Session = sessionmaker(bind=engine)
    return Session()

engine = inicializar_banco_de_dados()
seccao = obter_seccao(engine)


'''# Função para adicionar 50 peças
def adicionar_pecas():
    nomes = ["Parafuso", "Prego", "Martelo", "Serra", "Chave inglesa", "Furadeira", "Alicate", "Lixa", "Régua",
             "Cinto de segurança"]

    for _ in range(50):
        nome_peca = random.choice(nomes)  # Escolher aleatoriamente um nome
        quantidade_peca = random.randint(1, 100)  # Quantidade aleatória entre 1 e 100
        peca = Peca(nome=nome_peca, quantidade=quantidade_peca)
        session.add(peca)

    session.commit()


# Adicionar as 50 peças
adicionar_pecas()

# Verificar se as peças foram adicionadas
pecas = session.query(Peca).all()
for peca in pecas:
    print(f"{peca.id} - {peca.nome}: {peca.quantidade}")

# Fechar a sessão
session.close()'''
