from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Modelo.SQL import SessionLocal
from Controladores.planta_controlador import PlantaControlador

router = APIRouter(prefix="/plantas", tags=["Plantas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def cadastrar(id_especie: int, setor: str, status: str = "Saudável", db: Session = Depends(get_db)):
    return PlantaControlador(db).cadastrar(id_especie, setor, status)

@router.get("/setor/{setor}")
def buscar_setor(setor: str, db: Session = Depends(get_db)):
    return PlantaControlador(db).listar_por_setor(setor)

@router.put("/{id}/status")
def editar_status(id: int, novo_status: str, db: Session = Depends(get_db)):
    return PlantaControlador(db).editar_status(id, novo_status)