from fastapi import APIRouter, Depends, HTTPException
from src.model.model import Usuario
from src.dependencies.depends import pegar_sessao
import bcrypt
from src.schemas.schemas import UsuarioSchema, LoginSchema, AtualizarSenhaSchema
from sqlalchemy.orm import Session
from src.services.service import validar_email, validar_nome, validar_senha


auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id):
    token = f"667jh#sdufkDQR*03{id}"
    return token

def autenticar_usuario(email, senha, session):
    try:
        
        usuario = session.query(Usuario).filter(Usuario.email == email).first()
        
        if not usuario:
            return False
        elif not bcrypt.checkpw(senha.encode('utf-8'), usuario.senha):
            return False
        return usuario
    except Exception as e:
        print('Erro: ',e)


@auth_router.get('/')
async def autenticacao():
    """Rota de autenticação, teste de explicação da documentação."""
    return {"message": "Rota de autenticação", "autenticado": False}

# é importante definir o tipo dos parâmetros
# criando uma sessão e passando para o sessionmaker o banco de dados

@auth_router.post('/cadastro')
async def cadastro(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    try:
        print(f"DEBUG: Iniciando cadastro para email: {usuario_schema.email}")
        print(f"DEBUG: Dados recebidos - nome: {usuario_schema.nome}, email: {usuario_schema.email}")
        
        # Validação do nome
        print(f"DEBUG: Validando nome: {usuario_schema.nome}")
        if not validar_nome(usuario_schema.nome):
            print(f"DEBUG: Validação do nome falhou para: {usuario_schema.nome}")
            raise HTTPException(status_code=400, detail='Nome deve conter apenas letras')
        print(f"DEBUG: Nome validado com sucesso")
        
        # Validação do email
        print(f"DEBUG: Validando email: {usuario_schema.email}")
        if not validar_email(usuario_schema.email):
            print(f"DEBUG: Validação do email falhou para: {usuario_schema.email}")
            raise HTTPException(status_code=400, detail='Email inválido')
        print(f"DEBUG: Email validado com sucesso")

        # Validação da senha
        print(f'DEBUG: Verificando o tamanho da senha')
        if not validar_senha(usuario_schema.senha):
            print('DEBUG: Senha não segue o padrão')
            raise HTTPException(status_code=404, detail='Senha precisa ter um número, caractere especial, letra maiscula, sem espaços')
        
        # Verificar se email já existe
        print(f"DEBUG: Verificando se email já existe no banco: {usuario_schema.email}")
        usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first() 
        
        if usuario:
            print(f"DEBUG: Email já cadastrado: {usuario_schema.email}")
            raise HTTPException(status_code=400, detail='E-mail já está em uso')
        
        print(f"DEBUG: Email não encontrado no banco, pode prosseguir")
        
        # Criptografar senha
        print(f"DEBUG: Criptografando senha")
        senha = usuario_schema.senha.encode("utf-8")
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha, salt)
        print(f"DEBUG: Senha criptografada com sucesso")
        
        # Criar novo usuário
        print(f"DEBUG: Criando objeto Usuario")
        novo_usuario = Usuario(
            nome=usuario_schema.nome,
            email=usuario_schema.email,
            senha=senha_hash.decode('utf-8'),
            ativo=getattr(usuario_schema, 'ativo', True),
            admin=getattr(usuario_schema, 'admin', False)
        )
        print(f"DEBUG: Usuario criado: {novo_usuario.nome}, {novo_usuario.email}")
        
        # Adicionar ao banco
        print(f"DEBUG: Adicionando usuário à sessão")
        session.add(novo_usuario)
        print(f"DEBUG: Commitando no banco")
        session.commit()
        print(f"DEBUG: Commit realizado com sucesso, ID: {novo_usuario.id}")
        
        return HTTPException(status_code=200, detail='Cadastro realizado com sucesso!')
   
    except HTTPException as he:
        print(f"DEBUG: HTTPException capturada: {he.detail}, status: {he.status_code}")
        raise he
    except Exception as e:
        print(f'DEBUG: Exceção genérica no cadastro. Tipo: {type(e).__name__}, Mensagem: {str(e)}')
        print(f'DEBUG: Traceback completo:')
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail='Erro no servidor')
    
    
@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
        
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
    

