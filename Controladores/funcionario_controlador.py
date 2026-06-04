from fastapi import HTTPException
from Controladores.base import Base 
from Modelo.Tabelas import Funcionario

class FuncionarioControlador(Base):

    def cadastrar(self, nome: str, setor: str, turno: str):
        # Requisito 9: Cadastro de funcionários
        if not nome: 
            raise HTTPException(status_code=400, detail= "O nome precisa ser informado para cadastrar um funcionário.")
        
        novo = Funcionario(nome=nome, setor=setor, turno=turno)
        self._db.add(novo)
        self._db.commit()
        self._db.refresh(novo)
        return novo
    
    def listar_todos(self): 
        funcionarios_db = self._db.query(Funcionario).all()
        lista_final = []
        for f in funcionarios_db:
            lista_final.append({
                "id": f.id_funcionario,
                "nome": f.nome,
                "setor": f.setor,
                "turno": f.turno
            })
        return lista_final

    def editar(self, id_funcionario: int, novo_setor: str, novo_turno: str):
        funcionario = self._db.query(Funcionario).filter(Funcionario.id_funcionario == id_funcionario).first()
        
        if not funcionario:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado.")
        
        funcionario.setor = novo_setor
        funcionario.turno = novo_turno
        
        self._db.commit()
        self._db.refresh(funcionario)
        return funcionario

    def excluir(self, id_funcionario: int):
        funcionario = self._db.query(Funcionario).filter(Funcionario.id_funcionario == id_funcionario).first()
        
        if not funcionario:
            raise HTTPException(status_code=404, detail="Funcionário não encontrado para exclusão.")
        
        self._db.delete(funcionario)
        self._db.commit()
        return {"detail": f"Funcionário {id_funcionario} removido com sucesso."}