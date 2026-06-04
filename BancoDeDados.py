from Modelo.SQL import engine, Base
import Modelo as Tabelas  

print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("Banco de dados pronto!")