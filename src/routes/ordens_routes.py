#fastAPI vai trabalhar com funções async
from fastapi import APIRouter, Depends, HTTPException
from src.schemas.schemas import  PedidoSchema
from sqlalchemy.orm import Session
from src.dependencies.depends import pegar_sessao
from src.model.model import Pedido



ordens_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@ordens_router.get('/')
async def pedidos ():
    """Rota de pedidos, teste de explicação da documentação."""
    return {"message": "Lista de pedidos"}

@ordens_router.post('/')
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    
    return HTTPException(status_code=200,detail= f"Pedido criado com sucesso, n: {novo_pedido}")

