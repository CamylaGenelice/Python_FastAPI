from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base

from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv('DB_USER')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_password = os.getenv('DB_PASSWORD')

DATABAS_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABAS_URL, echo=True)

# cria a base do seu banco de dados
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id = Column('id', Integer,primary_key=True, autoincrement=True),
    nome = Column('nome', String, nullable= False),
    email = Column('email',String, nullable= False),
    senha = Column('senha', String, nullable= False),
    admin = Column('admin', Boolean, default= False),
    ativo = Column('ativo', Boolean, default=True)

    # essa função vai ser chamada sempre que eu criar um novo usuario
    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome,
        self.email = email,
        self.senha = senha,
        self.ativo = ativo,
        self.admin = admin