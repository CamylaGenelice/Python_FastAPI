from src.model.model import engine, Usuario
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.security.auth_jwt import validar_token

#objeto da classe
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def pegar_sessao():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session # retorna mas nao fecha a sessão
    finally:    
        session.close()

# -> Usuario: Isso é um Type Hint (Dica de Tipo). Indica que, no final de tudo, esta função vai devolver um objeto do tipo Usuario
def usuario_autenticado(token:str = Depends(oauth2_scheme), session: Session = Depends(pegar_sessao)
) -> Usuario:
    
    payload = validar_token(token)
    usuario = session.query(Usuario).filter(Usuario.id == payload['sub']).first()

    if not usuario:
        raise HTTPException( 
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuario não encontrado'
        )
    return usuario
