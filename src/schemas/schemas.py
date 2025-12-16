from pydantic import BaseModel
from typing import Optional

# classe para garantir a integridade dos valores que vao ser passados dentro do banco
class UsuarioSchema(BaseModel):
    
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]
    
    class Config: #
        from_attributes = True
        
class PedidoSchema(BaseModel):
    
    usuario: int
    preco: float
    item: str
    
    
    class Config: 
        from_attributes = True
        
class LoginSchema(BaseModel):
    email: str
    senha: str
    
    class Config:
        from_attributes = True