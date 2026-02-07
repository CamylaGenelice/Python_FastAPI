
from repository.queries import QueriesRepository
from src.schemas.schemas import NomePizzaSchema, AtualizarNomePizzaSchema

class ProdutoPizza:

    def __init__(self, repository: QueriesRepository):
        self.repository = repository

    
    def criar_pizza(self, dados: NomePizzaSchema):

        return self.repository.criar_pizza(nome=dados.nome)
 
    def atualizar_nome(self, dados: AtualizarNomePizzaSchema):

        nome = AtualizarNomePizzaSchema(
            id=dados.id,
            nome=dados.nome
        )

        return self.repository.atualizar_nome_pizza(nome)