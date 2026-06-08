from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Modelo.SQL import SessionLocal
from Controladores.funcionario_controlador import FuncionarioControlador

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def cadastrar(nome: str, setor: str, turno: str, db: Session = Depends(get_db)):
    return FuncionarioControlador(db).cadastrar(nome, setor, turno)

@router.get("/")
def listar(db: Session = Depends(get_db)):
    return FuncionarioControlador(db).listar_todos()

@router.put("/{id}")
def editar(id: int, setor: str, turno: str, db: Session = Depends(get_db)):
    return FuncionarioControlador(db).editar(id, setor, turno)

@router.delete("/{id}")
def excluir(id: int, db: Session = Depends(get_db)):
    return FuncionarioControlador(db).excluir(id)