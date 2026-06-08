from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from Modelo.SQL import Base
from datetime import date

class Especie(Base):
    __tablename__ = "especies"
    id_especie = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False) 
    frequencia_rega = Column(Integer)
    luminosidade = Column(String(255))          
    categoria = Column(String(255))            
    origem = Column(String(255))
    tipo_solo = Column(String(255)) 

    def __init__(self, nome, frequencia_rega, luminosidade, categoria, origem, tipo_solo="Geral"):
        self.nome = nome
        self.frequencia_rega = frequencia_rega
        self.luminosidade = luminosidade
        self.categoria = categoria
        self.origem = origem
        self.tipo_solo = tipo_solo

class PlantaIndividual(Base):
    __tablename__ = "plantas_individuais"
    id_planta = Column(Integer, primary_key=True, index=True)
    id_especie = Column(Integer, ForeignKey("especies.id_especie"), nullable=False)
    data_plantio = Column(Date)
    status_saude = Column(String(255))        
    setor_jardim = Column(String(255))       
    altura_cm = Column(Float)
    data_ultimo_cuidado = Column(Date, nullable=True)

    def __init__(self, id_especie, setor_jardim, status_saude="Saudável", altura_cm=0.0, data_plantio=None):
        self.id_especie = id_especie
        self.setor_jardim = setor_jardim
        self.status_saude = status_saude
        self.altura_cm = altura_cm
        self.data_plantio = data_plantio if data_plantio else date.today()
        self.data_ultimo_cuidado = date.today()

class Funcionario(Base):
    __tablename__ = "funcionarios"
    id_funcionario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False) 
    setor = Column(String(255))                 
    turno = Column(String(255))                 
    
    def __init__(self, nome, setor, turno): 
        self.nome = nome
        self.setor = setor
        self.turno = turno

class SensorAmbiente(Base):
    __tablename__ = "sensores_ambiente"
    id_sensor = Column(Integer, primary_key=True, index=True)
    setor = Column(String(255))
    temperatura = Column(Float)
    umidade = Column(Float)
    data_leitura = Column(Date)

    def __init__(self, setor, temperatura, umidade, data_leitura=None):
        self.setor = setor
        self.temperatura = temperatura
        self.umidade = umidade
        self.data_leitura = data_leitura if data_leitura else date.today()