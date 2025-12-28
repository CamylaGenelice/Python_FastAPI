from src.services.service import validar_email, validar_senha
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from src.model.model import Usuario
from src.dependencies.depends import pegar_sessao
import bcrypt
from src.schemas.schemas import UsuarioSchema, AtualizarSenhaSchema

update_router = APIRouter(prefix="/update", tags=["update"])

@update_router.post('/vericar_email')
async def verificacao_email(email:str,usuario_schema: UsuarioSchema,session: Session = Depends(pegar_sessao)):

    try:

        usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()

        if not usuario:
            raise HTTPException(status_code=404, detail='Usuario não encontrado')
        

    except HTTPException as he:
        print(f"DEBUG: HTTPException capturada: {he.detail}, status: {he.status_code}")
        raise he
    except Exception as e:
        print(f'DEBUG: Exceção genérica no cadastro. Tipo: {type(e).__name__}, Mensagem: {str(e)}')
        print(f'DEBUG: Traceback completo:')
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail='Erro no servidor')
    
@update_router.put('/atualizar_senha')
async def atualizar_senha(dados_senha: AtualizarSenhaSchema, session: Session = Depends(pegar_sessao)):

    try:
       print('DEBUG: Iniciando atualização de senha')

       if not validar_email(dados_senha.email):
           raise HTTPException(
               status_code=400,
               detail= 'Email inválido'
           )
       
       if not validar_senha(dados_senha.nova_senha):
           raise HTTPException(
               status_code=400,
               detail='A nova senha precisa ter: mínimo 8 caracteres, uma letra maiúscula, uma minúscula, um número, um caractere especial e não pode conter espaços'
           )
       usuario = session.query(Usuario).filter(
            Usuario.email == dados_senha.email
        ).first()
       
       if not usuario:
           raise HTTPException(
               status_code=400,
               detail='Usuario não encontrado'
           )
       print('dsdds')
       senha_nova = dados_senha.nova_senha.encode('utf-8')
       salt = bcrypt.gensalt()
       senha_hash = bcrypt.hashpw(senha_nova,salt)    

       usuario.senha = senha_hash.decode('utf-8')
       session.commit()

       return HTTPException(
            status_code=200,
            detail='senha atualizada com sucesso'
            )
        
    except HTTPException as he:
        print('DEBUG: HTTPException em atualizar_senha')
        raise he
    
    except Exception as e:
         print(f'DEBUG: Erro inesperado em atualizar_senha: {type(e).__name__}: {str(e)}')

         import traceback
         traceback.print_exc()
         raise HTTPException(
            status_code=500, 
            detail='Erro interno ao atualizar senha'
        )
