from src.model.model import Usuario
from src.schemas.schemas import UsuarioSchema, LoginSchema
from repository.queries import QueriesRepository
from src.utils.checks_utils import validar_email, validar_nome, validar_senha
from src.security.auth_jwt import criar_token,validar_token
import bcrypt


class UsuarioService:

    def __init__(self, repository:QueriesRepository):
        
        self.repository = repository
    
    def criar_usuario(self, dados: UsuarioSchema) -> Usuario:

        if not validar_nome(dados.nome):

            raise Exception('Nome inválido')
        
        if not validar_email(dados.email):

            raise Exception('Email inválido')
        
        if not validar_senha(dados.senha):

            raise Exception ('Senha não segue os padrões')
        
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(dados.senha,salt)
        
        usuario_existe = self.repository.buscar_email(dados.email)

        if usuario_existe:
            raise Exception ('Este email já está em uso')
        
        novo_usuario = Usuario(
            nome=dados.nome,
            email=dados.email,
            senha=senha_hash,
            ativo=dados.ativo,
            admin=dados.admin
            )

        return self.repository.criar_usuario(novo_usuario)
    
    def login(self, dados: LoginSchema):
        try:
            usuario = self.repository.buscar_email(dados.email)

            if not usuario:
                raise Exception('Email ou senha inválidos')
            if not bcrypt.checkpw(
                dados.senha.encode('utf-8'),
                usuario.senha
            ):
                raise Exception('Email ou senha inválidos')
            
            payload = {
                'sub':str(usuario.id),
                'admin': usuario.admin
                 }
            token = criar_token(dados=payload)
            return token
            
        
        except Exception as e:
            print('Erro no login service ', e)
            raise e
