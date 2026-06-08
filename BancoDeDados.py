from Modelo.Tabelas import Base
from Modelo.SQL import engine

print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Banco de dados pronto!")






