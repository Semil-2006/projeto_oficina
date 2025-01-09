from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Servico(Base):
    __tablename__ = 'servicos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)

    def __init__(self, nome):
        self.nome = nome


def inicializar_banco_de_dados(url_banco='sqlite:///oficina.db'):
    engine = create_engine(url_banco)
    Base.metadata.create_all(engine)
    return engine


def obter_sessio(engine):
    Sessio = sessionmaker(bind=engine)
    return Sessio()

engine = inicializar_banco_de_dados()
sessio = obter_sessio(engine)

# servicos = [
#     "Troca de óleo", "Troca de filtros de óleo", "Alinhamento de direção", "Balanceamento de rodas",
#     "Troca de pastilhas de freio", "Troca de discos de freio", "Revisão de suspensão", "Troca de amortecedores",
#     "Troca de velas", "Troca de correias", "Troca de cabos de vela", "Troca de bomba d'água",
#     "Troca de radiador", "Troca de bateria", "Limpeza de bicos injetores", "Troca de fluido de freio",
#     "Troca de fluido de direção hidráulica", "Troca de fluido de transmissão", "Troca de fluido de arrefecimento",
#     "Troca de óleo de câmbio automático", "Ajuste de embreagem", "Troca de sensor de oxigênio",
#     "Troca de bomba de combustível", "Troca de filtro de combustível", "Inspeção e regulagem do motor",
#     "Troca de kit de embreagem", "Reparos em motor", "Troca de suportes de motor", "Reparos em câmbio",
#     "Troca de correia dentada", "Troca de diferencial", "Revisão geral do carro", "Inspeção de sistema de ar condicionado",
#     "Reparo de ar condicionado automotivo", "Troca de compressor de ar condicionado", "Inspeção de sistema elétrico",
#     "Reparos em alternador", "Troca de fusíveis e relés", "Reparos em faróis e lanternas", "Troca de lâmpadas",
#     "Troca de para-brisa", "Reparos em sistema de escape", "Troca de catalisador", "Troca de silenciador",
#     "Inspeção de sistemas de suspensão", "Ajuste de direção", "Troca de pneus", "Reparos de rodas amassadas",
#     "Inspeção de freios", "Reparo de pintura automotiva"
# ]
#
# for nome_servico in servicos:
#     servico = Servico(nome=nome_servico)
#     session.add(servico)
#
# session.commit()
#
# resultados = session.query(Servico).all()
# for servico in resultados:
#     print(servico)
#
# session.close()
