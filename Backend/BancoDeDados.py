from modelo.Tabelas import Base
from modelo.SQL import engine

print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Banco de dados pronto!")






