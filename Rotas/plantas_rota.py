from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Modelo.SQL import SessionLocal 
from Controladores.planta_controlador import PlantaControlador
from datetime import date 

router = APIRouter(prefix="/plantas", tags=["Plantas Individuais"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def cadastrar(id_especie: int, setor_jardim: str, altura_cm: float = 0.0, status_saude: str = "Saudável", data_plantio: date = None, db: Session = Depends(get_db)):
    return PlantaControlador(db).cadastrar(id_especie, setor_jardim, status_saude, altura_cm, data_plantio)

@router.get("/{setor_jardim}")
def listar(setor_jardim: str, db: Session = Depends(get_db)):
    return PlantaControlador(db).listar_por_setor(setor_jardim)

@router.put("/{id}/status")
def editar_status(id: int, novo_status: str, db: Session = Depends(get_db)):
    return PlantaControlador(db).editar_status(id, novo_status)

@router.delete("/{id}")
def excluir(id: int, db: Session = Depends(get_db)):
    return PlantaControlador(db).excluir(id)