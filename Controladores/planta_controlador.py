from fastapi import HTTPException
from Controladores.base import Base 
from Modelo.Tabelas import PlantaIndividual
from datetime import date

class PlantaControlador(Base):

    def cadastrar(self, id_especie: int, setor: str, status: str = "Saudável"):
        # Requisito 10: Alertar se estiver 'Doente'
        if status.lower() == "doente":
            print(f"ALERTA: A planta do setor {setor} esta doente!")

        nova_planta = PlantaIndividual(id_especie=id_especie, setor=setor, status=status)
        self._db.add(nova_planta)
        self._db.commit()
        self._db.refresh(nova_planta)
        return nova_planta
    
    def listar_por_setor(self, setor: str):
        # Requisito 8: Listar plantas por setor
        plantas = self._db.query(PlantaIndividual).filter(PlantaIndividual.setor_jardim == setor).all()
        return [p for p in plantas]
    
    def editar_status(self, id_planta: int, novo_status: str):
        # Requisito 6: Edição de dados
        planta = self._db.query(PlantaIndividual).filter(PlantaIndividual.id_planta == id_planta).first()
        if not planta:
            raise HTTPException(status_code=404, detail="Planta não encontrada para editar.")
        
        planta.status_saude = novo_status
        planta.data_ultimo_cuidado = date.today() #Requisito 12:  armazenar data do último cuidado.
        self._db.commit()
        return planta
    
    def excluir(self, id_planta: int):
        planta = self._db.query(PlantaIndividual).filter(PlantaIndividual.id_planta == id_planta).first()
        if not planta:
            raise HTTPException(status_code=404, detail="Planta não encontrada para exclusão.")
        
        self._db.delete(planta)
        self._db.commit()
        return {"detail": f"Planta {id_planta} removida com sucesso."}

    
