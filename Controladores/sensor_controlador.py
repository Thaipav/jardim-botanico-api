from fastapi import HTTPException
from Controladores.base import Base 
from Modelo.Tabelas import SensorAmbiente
from datetime import date

class SensorControlador(Base):

    def cadastrar_leitura(self, setor: str, temperatura: float, umidade: float, data_leitura: date = None):
        
        # Requisito 9: VALIDAÇÃO: Verifica se a umidade é positiva
        if umidade < 0:
            raise HTTPException(
                status_code=400, 
                detail="A umidade deve apresentar apenas valores positivos."
            )

        # Requisito 10: Verifica se o clima é bom para cactos
        if temperatura > 25 and umidade < 30:
            diagnostico = "O ambiente está perfeito para cactos (quente e seco)."
        else:
            diagnostico = "O ambiente não está ideal para cactos no momento, coloque o sensor em um local mais apropriado, ou insira a planta aduqada a esse ambiente."

        nova_leitura = SensorAmbiente(
            setor=setor, 
            temperatura=temperatura, 
            umidade=umidade, 
            data_leitura=data_leitura if data_leitura else date.today()
        )
        
        self._db.add(nova_leitura)
        self._db.commit()
        self._db.refresh(nova_leitura)
        
        return {
            "id_sensor": nova_leitura.id_sensor,
            "setor": nova_leitura.setor,
            "diagnostico_cacto": diagnostico,
            "dados": {
                "id": nova_leitura.id_sensor,
                "setor": nova_leitura.setor,
                "temp": nova_leitura.temperatura,
                "umid": nova_leitura.umidade,
                "data": nova_leitura.data_leitura.strftime('%d/%m/%Y') if nova_leitura.data_leitura else "Sem data"
            }
        }

    def listar_leituras(self):
        leituras_db = self._db.query(SensorAmbiente).all()
        lista_final = []
        
        for s in leituras_db:
            lista_final.append({
                "id": s.id_sensor,
                "setor": s.setor,
                "temp": s.temperatura,
                "umid": s.umidade,
                "data": s.data_leitura.strftime('%d/%m/%Y') if s.data_leitura else "Sem data"
            })
        return lista_final
    
    def editar(self, id_sensor: int, novo_setor: str, nova_temp: float, nova_umid: float, nova_data: date = None):

        sensor = self._db.query(SensorAmbiente).filter(SensorAmbiente.id_sensor == id_sensor).first()
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Leitura do sensor não encontrada.")
        
        if nova_umid < 0:
            raise HTTPException(
                status_code=400, 
                detail="A umidade deve apresentar apenas valores positivos."
            )
        
        sensor.setor = novo_setor
        sensor.temperatura = nova_temp
        sensor.umidade = nova_umid
        sensor.data_leitura = nova_data if nova_data else date.today()
        
        self._db.commit()
        self._db.refresh(sensor)
        
        return {
            "mensagem": "Leitura do sensor atualizada com sucesso!",
            "dados": {
                "id": sensor.id_sensor,
                "setor": sensor.setor,
                "temp": sensor.temperatura,
                "umid": sensor.umidade,
                "data": sensor.data_leitura.strftime('%d/%m/%Y') if sensor.data_leitura else "Sem data"
            }
        }

    def excluir(self, id_sensor: int):
        leitura = self._db.query(SensorAmbiente).filter(SensorAmbiente.id_sensor == id_sensor).first()
        
        if not leitura:
            raise HTTPException(status_code=404, detail="Leitura do sensor não encontrada para exclusão.")
        
        self._db.delete(leitura)
        self._db.commit()
        
        return {"detail": f"Leitura do sensor {id_sensor} removida com sucesso."}