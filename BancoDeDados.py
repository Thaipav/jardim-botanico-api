from SQL import engine, Base
import tabelas 

print("Criando o banco de dados e as tabelas...")

Base.metadata.create_all(bind=engine)
print("Sucesso! O arquivo 'jardim.db' foi gerado.")