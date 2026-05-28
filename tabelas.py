from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from SQL import Base 

class Especie(Base):
    __tablename__ = "especies"
    id_especie = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False) 
    frequencia_rega = Column(Integer)
    luminosidade = Column(String)
    categoria = Column(String)
    origem = Column(String)

    def __init__(self, nome, freq, luz, solo=None, cat=None, orig=None):
        self.nome = nome
        self.frequencia_rega = freq
        self.luminosidade = luz
        self.tipo_solo = solo
        self.categoria = cat
        self.origem = orig

class PlantaIndividual(Base):
    __tablename__ = "plantas_individuais"
    id_planta = Column(Integer, primary_key=True, index=True)
    id_especie = Column(Integer, ForeignKey("especies.id_especie"), nullable=False)
    data_plantio = Column(Date)
    status_saude = Column(String)
    setor_jardim = Column(String)
    altura_cm = Column(Float)

    def __init__(self, id_especie, setor, status="Saudável"):
        self.id_especie = id_especie
        self.setor_jardim = setor
        self.status_saude = status

class Funcionario(Base):
    __tablename__ = "funcionarios"
    id_funcionario = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cargo = Column(String)
    turno = Column(String)
    
    def __init__(self, nome, cargo, turno): # Aspa corrigida aqui!
        self.nome = nome
        self.cargo = cargo
        self.turno = turno

class HistoricoCuidado(Base):
    __tablename__ = "historico_cuidados"
    id_cuidado = Column(Integer, primary_key=True, index=True)
    id_planta = Column(Integer, ForeignKey("plantas_individuais.id_planta"))
    data_cuidado = Column(Date)
    tipo_cuidado = Column(String)
    funcionario_responsavel = Column(Integer, ForeignKey("funcionarios.id_funcionario"))

    def __init__(self, id_planta, tipo_cuidado, funcionario_responsavel):
        self.id_planta = id_planta
        self.tipo_cuidado = tipo_cuidado
        self.funcionario_responsavel = funcionario_responsavel

class SensorAmbiente(Base): 
    __tablename__ = "sensores_ambiente"
    id_sensor = Column(Integer, primary_key=True, index=True) 
    setor = Column(String)
    temperatura = Column(Float)
    umidade = Column(Float)
    data_leitura = Column(Date)

    def __init__(self, setor, temperatura, umidade, data_leitura=None):
        self.setor = setor
        self.temperatura = temperatura
        self.umidade = umidade
        self.data_leitura = data_leitura