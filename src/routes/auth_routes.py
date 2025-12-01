from fastapi import APIRouter, Depends, HTTPException
from src.model.model import Usuario
from src.dependencies.depends import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get('/')
async def autenticacao():
    """Rota de autenticação, teste de explicação da documentação."""
    return {"message": "Rota de autenticação", "autenticado": False}

# é importante definir o tipo dos parâmetros
@auth_router.post('/cadastro')

async def cadastro(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    
    # criando uma sessão e passando para o sessionmaker o banco de dados
    
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    
    if usuario:
        raise HTTPException(status_code=404, detail='E-mail já está em uso')
    else:
        senha_hash = bcrypt_context.hash(usuario_schema.senha)
        
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_hash, usuario_schema.admin, usuario_schema.ativo)
        session.add(novo_usuario)
        session.commit() # salvando as alterações no banco de dados
        return HTTPException(status_code=200, detail='Cadastro realizado com sucesso')