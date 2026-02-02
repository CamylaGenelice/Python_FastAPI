#fastAPI vai trabalhar com funções async
from fastapi import Response
from fastapi import APIRouter, Depends, HTTPException
from src.schemas.schemas import  PedidoSchema
from sqlalchemy.orm import Session
from src.dependencies.depends import pegar_sessao
from src.repository.queries import QueriesRepository
from src.services.pedido_service import PedidoService



ordens_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@ordens_router.get('/')
async def pedidos ():
    """Rota de pedidos, teste de explicação da documentação."""
    return {"message": "Lista de pedidos"}

@ordens_router.post('/')
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    
    try:
        repo = QueriesRepository(session)
        service = PedidoService(repo)
        pedido = service.criar_pedido(pedido_schema)

        headers = {'Pedido-ID':str(pedido.id)}
        return Response (
            content='Pedido criado com sucesso',
            status_code=200,
            headers=headers
        )
        
        #return service.criar_pedido(pedido_schema)
    
    
    except Exception as e:
        print(f'DEBUG: Exceção genérica no cadastro de PEDIDOS. Tipo: {type(e).__name__}, Mensagem: {str(e)}')
        print(f'DEBUG: Traceback completo:')
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail='Erro no servidor')

