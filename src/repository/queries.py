from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.model.model import Usuario,Pedido,ItemPedido


'''
self.session.rollback(): Esta é a linha mais importante. Ela diz ao banco de dados: "Esqueça tudo o que eu tentei fazer nesta transação, pois algo deu errado". Sem isso, sua próxima tentativa de usar a session pode falhar com um erro de "transação inativa".
'''
class QueriesRepository:

    def __init__(self, session: Session):
        self.session = session

    def _salvar(self, objeto):
        try:
            self.session.add(objeto)
            self.session.commit()
            self.session.refresh(objeto)
            return objeto
        
        except SQLAlchemyError as e:

            self.session.rollback()
            print(f'Erro: ',{e})
            raise e


    def buscar_email(self, email: str) -> Usuario:
        try:
            return(
                self.session.query(Usuario).filter(Usuario.email == email).first()
            )
        except SQLAlchemyError as e:

            self.session.rollback()
            print(f'Erro ao buscar email',{e})
            raise e
    
    def criar_usuario(self, usuario:Usuario) -> Usuario:
       return self._salvar(usuario)
    
    def criar_pedido(self, pedido:Pedido) -> Pedido:
        return self._salvar(pedido)
    
    def criar_item_pedido(self, item_pedido: ItemPedido) -> ItemPedido:
       return self._salvar(item_pedido)
    
    

