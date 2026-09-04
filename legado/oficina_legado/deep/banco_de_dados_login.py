from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, Sequence('usuario_id_seq'), primary_key=True)
    nome_usuario = Column(String(50), nullable=False, unique=True)
    senha = Column(String(128), nullable=False)
    pergunta_seguranca = Column(String(100), nullable=False)
    resposta_seguranca = Column(String(100), nullable=False)

    def __init__(self, nome_usuario, senha, pergunta_seguranca, resposta_seguranca):
        self.nome_usuario = nome_usuario
        self.senha = senha
        self.pergunta_seguranca = pergunta_seguranca
        self.resposta_seguranca = resposta_seguranca


def inicializar_banco_de_dados(url_banco='sqlite:///usuarios.db'):
    engine = create_engine(url_banco)
    Base.metadata.create_all(engine)
    return engine


def obter_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

engine = inicializar_banco_de_dados()
session = obter_session(engine)
