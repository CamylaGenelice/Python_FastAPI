from pydantic import BaseModel
from datetime import datetime
from typing import Optional
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
    preco: int
    
    class Config: 
        from_attributes = True
        
class LoginSchema(BaseModel):
    email: str
    senha: str
    
    class Config:
        from_attributes = True


class AtualizarSenhaSchema(BaseModel):

    email: str
    codigo: str
    nova_senha: str
    class Config:
        from_attributes = True
    
class SolicitarRecuperacaoSchema(BaseModel):
    email: str

    class Config:
        from_attributes = True

class VerificarCodigoSchema(BaseModel):
    email: str
    codigo: str

    class Config:
        from_attributes = True

class SuccesMessageSchema(BaseModel):
    message: str
    class Config:
        from_attributes = True

