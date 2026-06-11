from fastapi import HTTPException
from controladores.base import Base
from modelo.Tabelas import Especie

class EspecieControlador(Base):

    def cadastrar(self, nome: str, frequencia_rega: int, luminosidade: str, categoria: str, origem: str, tipo_solo: str = "solo humífero "):
        if not nome:
            raise HTTPException(status_code=400, detail="O nome da espécie é obrigatório.")
        # Requisito 1: Frequência de rega não pode ser negativa
        if frequencia_rega < 0:
            raise HTTPException(status_code=400, detail="A rega não pode ser negativa!")
        
        # Requisito 2: Rega excessiva em cactos não é permitida
        if "cacto" in nome.lower() and frequencia_rega > 1:
            raise HTTPException(status_code=400, detail="Cactos devem ser regados no máximo uma vez por semana.")
        
        nova = Especie(nome=nome, frequencia_rega=frequencia_rega, luminosidade=luminosidade, categoria=categoria, origem=origem, tipo_solo=tipo_solo)
        self._db.add(nova)
        self._db.commit()
        self._db.refresh(nova)
        return nova 

    def listar_tudo(self):
        especies = self._db.query(Especie).all()
        
        return [{
            "id": e.id_especie, 
            "nome": e.nome, 
            "rega": e.frequencia_rega, 
            "solo": e.tipo_solo
        } for e in especies]

    def editar(self, id_especie: int, nome: str, frequencia_rega: int):
        alvo = self._db.query(Especie).filter(Especie.id_especie == id_especie).first()
        if not alvo:
            raise HTTPException(status_code=404, detail="Espécie não encontrada para editar.")
        
        if "cacto" in nome.lower() and frequencia_rega > 1:
            raise HTTPException(status_code=400, detail="Cactos devem ser regados no máximo uma vez por semana (mesmo na edição).")

        alvo.nome = nome
        alvo.frequencia_rega = frequencia_rega

        self._db.commit()
        self._db.refresh(alvo)
        return alvo
    
    def excluir(self, id_especie: int):
        alvo = self._db.query(Especie).filter(Especie.id_especie == id_especie).first()
        if not alvo:
            raise HTTPException(status_code=404, detail="Espécie não encontrada para excluir.")
        
        self._db.delete(alvo)
        self._db.commit()
        return {"detail": "Espécie excluída com sucesso."}