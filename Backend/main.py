from fastapi import FastAPI
from rotas import especie_rota, funcionario_rota, plantas_rota, sensor_rota
from modelo.Tabelas import Base  
from backend.BancoDeDados import engine  

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Jardim API")

app.include_router(especie_rota.router)
app.include_router(funcionario_rota.router)
app.include_router(plantas_rota.router)
app.include_router(sensor_rota.router)