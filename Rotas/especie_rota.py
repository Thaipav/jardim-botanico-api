from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Modelo.SQL import SessionLocal 
from Controladores.especie_controlador import EspecieControlador

router = APIRouter(prefix="/especies", tags=["Espécies"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def cadastrar(nome: str, freq: int, luz: str, cat: str, orig: str, db: Session = Depends(get_db)):
    return EspecieControlador(db).cadastrar(nome, freq, luz, cat, orig)

@router.get("/")
def listar(db: Session = Depends(get_db)):
    return EspecieControlador(db).listar_tudo()

@router.delete("/{id}")
def excluir(id: int, db: Session = Depends(get_db)):
    return EspecieControlador(db).excluir(id)