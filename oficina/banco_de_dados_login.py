from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, Sequence('usuario_id_seq'), primary_key=True)
    nome_usuario = Column(String(50), nullable=False, unique=True)
    senha_hash = Column(String(128), nullable=False)
    pergunta_seguranca = Column(String(100), nullable=False)
    resposta_seguranca = Column(String(100), nullable=False)

def inicializar_banco_de_dados(url_banco='sqlite:///usuarios.db'):
    # Criar engine do banco de dados
    engine = create_engine(url_banco)
    # Criar todas as tabelas no banco
    Base.metadata.create_all(engine)
    return engine

if __name__ == "__main__":
    # Inicializar o banco de dados SQLite
    engine = inicializar_banco_de_dados()
    # Criar uma sessão para interagir com o banco
    Session = sessionmaker(bind=engine)
    session = Session()


    import hashlib
    def hash_senha(senha):
        """Gera um hash seguro para a senha."""
        return hashlib.sha256(senha.encode('utf-8')).hexdigest()


    novo_usuario = Usuario(
        nome_usuario="usuario_exemplo",
        senha_hash=hash_senha("senha123"),
        pergunta_seguranca="Qual estado você nasceu?",
        resposta_seguranca="São Paulo"
    )

    session.add(novo_usuario)
    session.commit()
    print("Usuário adicionado ao banco de dados!")
