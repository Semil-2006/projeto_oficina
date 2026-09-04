from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    func,
    text,
    inspect,
)
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy.exc import OperationalError
from passlib.context import CryptContext
import os

# Segurança: hashing com bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_usuario = Column(String(50), nullable=False, unique=True, index=True)
    _senha_hash = Column("senha", String(128), nullable=False)
    pergunta_seguranca = Column(String(100), nullable=False)
    resposta_seguranca_hash = Column(String(128), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)

    def __init__(self, nome_usuario: str, senha: str, pergunta_seguranca: str, resposta_seguranca: str):
        self.nome_usuario = nome_usuario
        self.senha = senha
        self.pergunta_seguranca = pergunta_seguranca
        self.resposta_seguranca = resposta_seguranca

    @property
    def senha(self) -> str:
        raise AttributeError("A senha não pode ser lida diretamente")

    @senha.setter
    def senha(self, senha_plana: str):
        self._senha_hash = pwd_context.hash(senha_plana)

    def verificar_senha(self, senha_plana: str) -> bool:
        return pwd_context.verify(senha_plana, self._senha_hash)

    @property
    def resposta_seguranca(self) -> str:
        raise AttributeError("A resposta de segurança não pode ser lida diretamente")

    @resposta_seguranca.setter
    def resposta_seguranca(self, resposta_plana: str):
        self.resposta_seguranca_hash = pwd_context.hash(resposta_plana)

    def verificar_resposta(self, resposta_plana: str) -> bool:
        return pwd_context.verify(resposta_plana, self.resposta_seguranca_hash)


def get_database_url() -> str:
    return os.getenv('DATABASE_URL', 'sqlite:///usuarios.db')


def criar_engine(echo: bool = False, pool_pre_ping: bool = True):
    url = get_database_url()
    return create_engine(url, echo=echo, pool_pre_ping=pool_pre_ping)

# Sessão configurada
SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=criar_engine(),
        expire_on_commit=False,
    )
)


def inicializar_banco_de_dados(drop_existing: bool = False):
    engine = criar_engine(echo=False)

    if drop_existing:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        return engine

    # Primeiro cria tabela se não existir
    Base.metadata.create_all(engine)

    # Auto-migração simples: adiciona colunas que faltam
    inspector = inspect(engine)
    cols = {c['name'] for c in inspector.get_columns(Usuario.__tablename__)}
    with engine.connect() as conn:
        if 'resposta_seguranca_hash' not in cols:
            conn.execute(text('ALTER TABLE usuarios ADD COLUMN resposta_seguranca_hash VARCHAR(128) NOT NULL DEFAULT ""'))
        if 'ativo' not in cols:
            conn.execute(text('ALTER TABLE usuarios ADD COLUMN ativo BOOLEAN NOT NULL DEFAULT 1'))
        if 'atualizado_em' not in cols:
            conn.execute(text('ALTER TABLE usuarios ADD COLUMN atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP'))
        conn.commit()
    return engine


def get_session():
    """Obtem uma sessão; use com 'with' ou feche manualmente."""
    return SessionLocal()


# Exemplo de uso
def main():
    # Se quiser resetar em dev: inicializar_banco_de_dados(drop_existing=True)
    engine = inicializar_banco_de_dados()
    with get_session() as session:
        novo = Usuario(
            nome_usuario='joao',
            senha='minha_senha_forte',
            pergunta_seguranca='Cor da sua camisa favorita?',
            resposta_seguranca='azul',
        )
        session.add(novo)
        session.commit()
        print(f'Usuário criado: {novo.id}')

if __name__ == '__main__':
    main()
