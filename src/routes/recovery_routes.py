from src.services.service import validar_email, validar_senha
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import bcrypt
from src.schemas.schemas import (SolicitarRecuperacaoSchema, VerificarCodigoSchema, AtualizarSenhaSchema, SuccesMessageSchema)
from src.dependencies.depends import pegar_sessao
from src.model.model import Usuario
from src.services.email_service import email_service

recovery_router = APIRouter(prefix="/recuperacao_de_senha", tags=["recovery"])

def gerar_codigo_recuperacao():

    import secrets
    import string

    caracteres = string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(6))

def enviar_email_recuperacao_background(email: str, nome: str, codigo: str):

    assunto = 'Recuperação de Senha'
    corpo = email_service.criar_email_recuperacao(nome, codigo)
    email_service.enviar_email(email, assunto, corpo)

@recovery_router.post(
        '/solicitar-recuperacao', response_model=SuccesMessageSchema,
        summary='Solicitar código de recuperação'
)

async def solicitar_recuperacao(dados: SolicitarRecuperacaoSchema, background_tasks: BackgroundTasks, session: Session = Depends(pegar_sessao)):
    try: 
        if not validar_email(dados.email):
            raise HTTPException(status_code=400, detail='Email inválido')
        
        usuario = session.query(Usuario).filter(
            Usuario.email == dados.email, Usuario.ativo == True
        ).first()
        if not usuario:
            return { "message": "Se o email existir em nosso sistema, enviaremos um código de recuperação"}
        
        codigo = gerar_codigo_recuperacao()
        expiracao = datetime.now() + timedelta(minutes=10)

        usuario.codigo_recuperacao = codigo
        usuario.codigo_expiracao = expiracao
        usuario.tentativas_codigo = 0

        session.commit()

        background_tasks.add_task(
            enviar_email_recuperacao_background,
            usuario.email,
            usuario.nome,
            codigo
        )
        return {
            "message": "Código de recuperação enviado para seu email"
            
        }

    except Exception as e:
        print(f"Erro ao solicitar recuperação: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")
    

@recovery_router.post(
    '/verificar-codigo',
    response_model=SuccesMessageSchema,
    summary='Verificar código de recuperação')
async def verificar_codigo(
    
    dados: VerificarCodigoSchema,
    session: Session = Depends(pegar_sessao)
):
    try:
        usuario = session.query(Usuario).filter(
            Usuario.email == dados.email,
            Usuario.ativo == True
        ).first()

        if not usuario:
            raise HTTPException(status_code=400, detail='Usuario não encontrado')
        if not usuario.codigo_recuperacao or not usuario.codigo_expiracao:
            raise HTTPException(status_code=400, detail='Nenhum código de recuperação pendente')

        # Verificar expiração
        if datetime.now() > usuario.codigo_expiracao:
            raise HTTPException(
                status_code=400, 
                detail="Código expirado. Solicite um novo."
            )
        
        # Verificar tentativas (máximo 3)
        if usuario.tentativas_codigo >= 3:
            raise HTTPException(
                status_code=400, 
                detail="Máximo de tentativas excedido. Solicite um novo código."
            )
         # Verificar código

        if usuario.codigo_recuperacao != dados.codigo:

            usuario.tentativas_codigo += 1
            session.commit()

            tentativas_restantes = 3 - usuario.tentativas_codigo

            raise HTTPException(status_code=400, detail='Código invalido')
        usuario.tentativas_codigo = 0
        session.commit()

        return {'message': 'Código verificado com sucesso!'}

    except Exception as e:
        print(f"Erro ao verificar código: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")
    
@recovery_router.post('/redefinir_senha')
async def redefinir_senha(
    dados: AtualizarSenhaSchema,
    session: Session =  Depends(pegar_sessao)
):
    try:

        if not validar_senha(dados.nova_senha):
            raise HTTPException(status_code=400, detail='A senha nova não atende os requisitos de segurança.')
        
        usuario = session.query(Usuario).filter(Usuario.email == usuario.email,
        Usuario.ativo == True).first()

        if not usuario:
            raise HTTPException(status_code=404, detail='Usuario não encontrado')
        
        # Verificar código
        if not usuario.codigo_recuperacao != dados.codigo:
            raise HTTPException(status_code=404, detail='Código invalido')
        
        # Verifica expiração
        if datetime.now() > usuario.codigo_expiracao:
            raise HTTPException(status_code=400, detail='Código expirado')

        
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(dados.nova_senha.encode('utf-8'), salt)

        usuario.senha = senha_hash.decode('utf-8')
        usuario.codigo_recuperacao = None
        usuario.codigo_expiracao = None
        usuario.tentativas_codigo = 0

        session.commit()

        return {
            "message": "Senha redefinida com sucesso"
            
        }

    except Exception as e:
       print(f"Erro ao redefinir senha: {e}")
       raise HTTPException(status_code=500, detail="Erro interno") 