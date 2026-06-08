from fastapi import HTTPException
from Controladores.base import Base 
from Modelo.Tabelas import SensorAmbiente

class SensorControlador(Base):

    def cadastrar_leitura(self, setor: str, temperatura: float, umidade: float, data_leitura: int):
        
        # 9. VALIDAÇÃO: Verifica se a umidade é positiva
        if umidade < 0:
            raise HTTPException(
                status_code=400, 
                detail="A umidade deve apresentar apenas valores positivos."
            )

        # 10. LÓGICA DE NEGÓCIO: Verifica se o clima é bom para cactos
        if temperatura > 25 and umidade < 30:
            diagnostico = "SIM! O ambiente está perfeito para cactos (quente e seco)."
        else:
            diagnostico = "NÃO. O ambiente não está ideal para cactos no momento."

        nova_leitura = SensorAmbiente(
            setor=setor, 
            temperatura=temperatura, 
            umidade=umidade, 
            data_leitura=data_leitura
        )
        
        self._db.add(nova_leitura)
        self._db.commit()
        self._db.refresh(nova_leitura)
        
        return {
            "id_sensor": nova_leitura.id_sensor,
            "setor": nova_leitura.setor,
            "diagnostico_cacto": diagnostico,
            "dados": nova_leitura
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
                "data": s.data_leitura
            })
        return lista_final
    
    def editar(self, id_sensor: int, novo_setor: str, nova_temp: float, nova_umid: float, nova_data: int):

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
        sensor.data_leitura = nova_data
        
        self._db.commit()
        self._db.refresh(sensor)
        return sensor

    def excluir(self, id_sensor: int):
        leitura = self._db.query(SensorAmbiente).filter(SensorAmbiente.id_sensor == id_sensor).first()
        
        if not leitura:
            raise HTTPException(status_code=404, detail="Leitura do sensor não encontrada para exclusão.")
        
        self._db.delete(leitura)
        self._db.commit()
        
        return {"detail": f"Leitura do sensor {id_sensor} removida com sucesso."}