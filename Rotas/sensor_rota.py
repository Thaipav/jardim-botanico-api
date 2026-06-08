from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Modelo.SQL import SessionLocal
from Controladores.sensor_controlador import SensorControlador
from datetime import date

router = APIRouter(prefix="/sensores", tags=["Sensores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def cadastrar(setor: str, temperatura: float, umidade: float, data_leitura: date = None, db: Session = Depends(get_db)):
    return SensorControlador(db).cadastrar_leitura(setor, temperatura, umidade, data_leitura)

@router.get("/")
def listar_todas(db: Session = Depends(get_db)):
    return SensorControlador(db).listar_leituras()

@router.put("/{id}")
def editar_leitura(id: int, setor: str, temperatura: float, umidade: float, data_leitura: date = None, db: Session = Depends(get_db)):
    return SensorControlador(db).editar(id, setor, temperatura, umidade, data_leitura)

@router.delete("/{id}")
def deletar_leitura(id: int, db: Session = Depends(get_db)):
    return SensorControlador(db).excluir(id)