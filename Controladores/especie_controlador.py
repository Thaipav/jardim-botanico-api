from fastapi import HTTPException
from Controladores.base import Base
from Modelo.Tabelas import Especie

class EspecieControlador(Base):

    def cadastrar(self, nome: str, freq: int, luz: str, cat: str, orig: str):
        # Requisito 1: Não permite sem nome
        if not nome:
            raise HTTPException(status_code=400, detail="O nome da espécie é obrigatório.")
        # Requisito 2: Frequência de rega não pode ser negativa
        if freq < 0:
            raise HTTPException(status_code=400, detail="A rega não pode ser negativa!")
        # Requisito 3: Rega excessiva em cactos
        if "Cacto" in nome and freq > 1:
            raise HTTPException(status_code=400, detail="Cactos devem ser regados no máximo uma vez por semana.")
        
        nova = Especie(nome=nome, freq=freq, luz=luz, cat=cat, orig=orig)
        self._db.add(nova)
        self._db.commit()
        self._db.refresh(nova)
        return nova 
 
    def listar_tudo(self):
        especies = self._db.query(Especie).all()
        return [{"id": e.id_especie, "nome": e.nome} for e in especies]

    def editar(self, id_especie: int, nome: str, freq: int):
        alvo = self._db.query(Especie).filter(Especie.id_especie == id_especie).first()
        if not alvo:
            raise HTTPException(status_code=404, detail="Espécie não encontrada para editar.")
        alvo.nome = nome
        alvo.frequencia_rega = freq
        
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
        