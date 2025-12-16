from fastapi import APIRouter, Depends, HTTPException
from src.model.model import Usuario
from src.dependencies.depends import pegar_sessao
import bcrypt
from src.schemas.schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from src.services.service import validar_email, validar_nome


auth_router = APIRouter(prefix="/auth", tags=["auth"])


def criar_token(id):
    token = f"667jh#sdufkDQR*03{id}"
    return token

def autenticar_usuario(email, senha, session):
    try:
        
        usuario = session.query(Usuario).filter(Usuario.email == email).first()
        
        if not usuario:
            return False
        elif not bcrypt.checkpw(senha, Usuario.senha):
            return False
        return Usuario
    except Exception as e:
        print('Erro: ',e)



@auth_router.get('/')
async def autenticacao():
    """Rota de autenticação, teste de explicação da documentação."""
    return {"message": "Rota de autenticação", "autenticado": False}

# é importante definir o tipo dos parâmetros
@auth_router.post('/cadastro')

async def cadastro(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    
    # criando uma sessão e passando para o sessionmaker o banco de dados
    try:
        if not validar_nome(UsuarioSchema.nome):
            
            return HTTPException(status_code=404, detail='Nome deve conter apenas letras')
        
        if not validar_email(UsuarioSchema.email):
            
            return HTTPException(status_code=404, detail='Email inválido')
            
        usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    
        if usuario:
            raise HTTPException(status_code=404, detail='E-mail já está em uso')
        else:
            senha = usuario_schema.senha.encode("utf-8")
            salt = bcrypt.gensalt()
            senha_hash = bcrypt.hashpw(senha,salt)
            
            novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_hash, usuario_schema.admin, usuario_schema.ativo)
            session.add(novo_usuario)
            session.commit() # salvando as alterações no banco de dados
            return HTTPException(status_code=200, detail='Cadastro realizado com sucesso')
   
    except Exception as e:
        print('Ocorreu um erro no cadastro ',e)
        raise HTTPException(status_code=500, detail='Erro no servidor')
    
    
    
@auth_router.post('/login')
async def login(login_schema: LoginSchema, session = Depends(pegar_sessao)):
        
    if not validar_email(LoginSchema.email):
            
        return HTTPException(status_code=404, detail='Email inválido')
    
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario não encontrado ou credenciais inválidas')
    else:
        access_token = criar_token(usuario.id)
        # Headers = {Access_Token: Bearer token}
        return {
            "access_token": access_token,
            "token_type": "Bearer"
            }