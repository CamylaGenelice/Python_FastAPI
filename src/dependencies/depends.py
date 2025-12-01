from src.model.model import engine
from sqlalchemy.orm import sessionmaker

def pegar_sessao():
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session # retorna mas nao fecha a sessão
    finally:    
        session.close()