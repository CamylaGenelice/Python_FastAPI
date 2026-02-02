from src.model.model import ItemPedido
#from src.schemas.schemas import Item
from repository.queries import QueriesRepository

class ItensService:

    def __init__(self, repository:QueriesRepository):
        
        self.repository = repository
    
    def criar_item_do_pedido(self,pedido,sabor,quantidade, preco):

        try:
            item = ItemPedido(pedido,sabor,quantidade,preco)

            return self.repository.criar_item_pedido(item)
        
        except Exception as e:

            print(f'Erro ao criar o item do pedido no service',{e})