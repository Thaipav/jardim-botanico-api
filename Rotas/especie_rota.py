from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modelo.SQL import SessionLocal 
from controladores.especie_controlador import EspecieControlador

router = APIRouter(prefix="/especies", tags=["Espécies"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def cadastrar(nome: str, frequencia_rega: int, luminosidade: str, categoria: str, origem: str, db: Session = Depends(get_db)):
    return EspecieControlador(db).cadastrar(nome, frequencia_rega, luminosidade, categoria, origem)

@router.get("/")
def listar(db: Session = Depends(get_db)):
    return EspecieControlador(db).listar_tudo()

@router.put("/{id}")
def editar(id: int, nome: str, freq: int, db: Session = Depends(get_db)): 
    return EspecieControlador(db).editar(id, nome, freq)

@router.delete("/{id}")
def excluir(id: int, db: Session = Depends(get_db)):
    return EspecieControlador(db).excluir(id)