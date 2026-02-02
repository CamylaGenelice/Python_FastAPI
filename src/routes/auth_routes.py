from fastapi import APIRouter, Depends, HTTPException
from fastapi import Response
from repository.queries import QueriesRepository
from src.services.usuario_service import UsuarioService
from src.dependencies.depends import pegar_sessao

from src.schemas.schemas import UsuarioSchema, LoginSchema, AtualizarSenhaSchema
from sqlalchemy.orm import Session



auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id):
    token = f"667jh#sdufkDQR*03{id}"
    return token


@auth_router.get('/')
async def autenticacao():
    """Rota de autenticação, teste de explicação da documentação."""
    return {"message": "Rota de autenticação", "autenticado": False}

# é importante definir o tipo dos parâmetros
# criando uma sessão e passando para o sessionmaker o banco de dados

@auth_router.post('/cadastro')
async def cadastro(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    try:
       repo = QueriesRepository(session)
       service = UsuarioService(repo)
       usuario =  service.criar_usuario(usuario_schema)

       return Response(
           content='Usuario criado com sucesso!',
           status_code=200
       )

    
    except Exception as e:
        print(f'DEBUG: Exceção genérica no cadastro. Tipo: {type(e).__name__}, Mensagem: {str(e)}')
        print(f'DEBUG: Traceback completo:')
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail='Erro no servidor')
    
    
@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
        
    try:
        # Queries é o meu construtor e ele tem argumentos que é necessario para que assim possa ser criado o objeto ( instancia) da classe
         
        repo = QueriesRepository(session) #Crie um objeto responsável por acessar o banco usando essa session”
        service = UsuarioService(repo)
        
        '''AQUI VAI RETORNAR O TOKEN DO USUARIO'''
        headers = service
        return Response(
            content='Login realizado com sucesso',
            status_code=200,
            headers= headers
            )
    
    
    except Exception as e:
        
        print('Erro ao fazer login')
        raise HTTPException(status_code=500, detail='Erro interno no servidor')
    

