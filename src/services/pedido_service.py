from src.model.model import Pedido
from src.schemas.schemas import PedidoSchema
from repository.queries import QueriesRepository

class PedidoService:

    def __init__(self, repository: QueriesRepository):
        self.repository = repository

    def criar_pedido(self,pedido_schema:PedidoSchema) -> Pedido:
        try:
            pedido = Pedido(
                usuario=pedido_schema.usuario,
                status=pedido_schema.preco,
                itens=pedido_schema.item
                )

            return self.repository.criar_pedido(pedido)
        
        except Exception as e:
            print(f'Erro ao criar pedido service',{e})