from pydantic import BaseModel

class PedidoSchema(BaseModel):
    
    usuario: int
    preco: int
    
    class Config: 
        from_attributes = True
        

class NomePizzaSchema(BaseModel):

    nome: str

    class Config:
        from_attributes = True

class AtualizarNomePizzaSchema(BaseModel):

    id: int
    nome: str

    class Config:
        from_attributes = True