from fastapi import HTTPException
from Controladores.base import Base 
from Modelo.Tabelas import PlantaIndividual
from datetime import date

class PlantaControlador(Base):

    def cadastrar(self, id_especie: int, setor_jardim: str, status_saude: str = "Saudável", altura_cm: float = 0.0, data_plantio: date = None):
        # Requisito 5: Se a planta receber status "Doente", gera alerta para o usuário
        alerta_usuario = None
        if status_saude.lower() == "doente":
            alerta_usuario = f"ATENÇÃO: A planta do setor {setor_jardim} foi registrada como DOENTE!"
            print(alerta_usuario) 

        nova_planta = PlantaIndividual(
            id_especie=id_especie, 
            setor_jardim=setor_jardim, 
            status_saude=status_saude,
            altura_cm=altura_cm,
            data_plantio=data_plantio if data_plantio else date.today()
        )
        
        # Requisito 6: Armazena a data do último cuidado
        nova_planta.data_ultimo_cuidado = date.today() 

        self._db.add(nova_planta)
        self._db.commit()
        self._db.refresh(nova_planta)
        
        return {
            "mensagem": "Planta cadastrada com sucesso!",
            "alerta": alerta_usuario, 
            "dados_da_planta": {
                "id_planta": nova_planta.id_planta,
                "id_especie": nova_planta.id_especie,
                "setor": nova_planta.setor_jardim,
                "status": nova_planta.status_saude,
                "altura": nova_planta.altura_cm if nova_planta.altura_cm else 0.0,
                "data_plantio": nova_planta.data_plantio.strftime('%d/%m/%Y'),
                "ultimo_cuidado": nova_planta.data_ultimo_cuidado.strftime('%d/%m/%Y')
            }
        }
    
    def listar_por_setor(self, setor_jardim: str):
        # Requisito 7: Listar plantas por setor do jardim
        plantas = self._db.query(PlantaIndividual).filter(PlantaIndividual.setor_jardim == setor_jardim).all()
       
        return [{
            "id_planta": p.id_planta,
            "id_especie": p.id_especie,
            "setor": p.setor_jardim,
            "status": p.status_saude,
            "altura": p.altura_cm if p.altura_cm else 0.0,
            "data_plantio": p.data_plantio.strftime('%d/%m/%Y') if p.data_plantio else "Sem data",
            "ultimo_cuidado": p.data_ultimo_cuidado.strftime('%d/%m/%Y') if p.data_ultimo_cuidado else "Sem registro"
        } for p in plantas]
    
    def editar_status(self, id_planta: int, novo_status: str):
        # Requisito 8: Permite a edição do status de saúde da planta, atualizando a data do último cuidado
        planta = self._db.query(PlantaIndividual).filter(PlantaIndividual.id_planta == id_planta).first()
        
        if not planta:
            raise HTTPException(status_code=404, detail="Planta não encontrada para editar.")
        
        planta.status_saude = novo_status
        planta.data_ultimo_cuidado = date.today() 
        
        self._db.commit()
        self._db.refresh(planta)

        alerta = None
        if novo_status.lower() == "doente":
            alerta = f"ALERTA: Status alterado! Planta do setor {planta.setor_jardim} está DOENTE!"

        return {
            "mensagem": "Status atualizado com sucesso!",
            "alerta": alerta,
            "planta": {
                "id_planta": planta.id_planta,
                "id_especie": planta.id_especie,
                "setor": planta.setor_jardim,
                "status": planta.status_saude,
                "altura": planta.altura_cm if planta.altura_cm else 0.0,
                "data_plantio": planta.data_plantio.strftime('%d/%m/%Y') if planta.data_plantio else "Sem data",
                "ultimo_cuidado": planta.data_ultimo_cuidado.strftime('%d/%m/%Y') if planta.data_ultimo_cuidado else "Sem registro"
            }
        }
    
    def excluir(self, id_planta: int):
        planta = self._db.query(PlantaIndividual).filter(PlantaIndividual.id_planta == id_planta).first()
        
        if not planta:
            raise HTTPException(status_code=404, detail="Planta não encontrada para exclusão.")
        
        self._db.delete(planta)
        self._db.commit()
        
        return {"detail": f"Planta {id_planta} removida com sucesso."}