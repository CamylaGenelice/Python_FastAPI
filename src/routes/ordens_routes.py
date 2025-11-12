#fastAPI vai trabalhar com funções async
from fastapi import APIRouter

ordens_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@ordens_router.get('/')
async def pedidos ():
    """Rota de pedidos, teste de explicação da documentação."""
    return {"message": "Lista de pedidos"}

@ordens_router.post('/')
async def criar_pedido():
    return {"message": "Pedido criado com sucesso"}