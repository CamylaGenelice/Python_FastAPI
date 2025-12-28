from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv('DB_USER')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_password = os.getenv('DB_PASSWORD')

DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    admin = Column(Boolean, default=False)
    ativo = Column(Boolean, default=True)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    __tablename__ = 'pedido'
    
    STATUS_PEDIDOS = (
        ('PENDENTE', 'PENDENTE'),
        ('EM_PREPARO', 'EM_PREPARO'),
        ('ENVIADO', 'ENVIADO'),
        ('ENTREGUE', 'ENTREGUE'),
        ('CANCELADO', 'CANCELADO'),
    )
        
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(ChoiceType(choices=STATUS_PEDIDOS))
    usuario = Column(Integer, ForeignKey('usuario.id'))
    preco = Column(Float, nullable=False)
    itens = Column(String)
    
    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status


class ItemPedido(Base):
    __tablename__ = 'itens_pedido'      
     
    id = Column(Integer, primary_key=True, autoincrement=True) 
    quantidade = Column(Integer, nullable=False)
    sabor = Column(String, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    pedido = Column(Integer, ForeignKey('pedido.id'))
    
    def __init__(self, pedido, sabor, quantidade, preco_unitario):
        self.pedido = pedido
        self.sabor = sabor
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
