from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.model.model import Produto

class QueriesProduto:

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

    def criar_pizza(self, pizza: Produto):
        return self._salvar(pizza)
    
    def atualizar_nome_pizza(self, pizza: Produto):
        return self._salvar(pizza)