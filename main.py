# uvicorn main:app --reload para rodar o servidor
# app é a variavel do fastAPI que vai ser criada

from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
app = FastAPI()
    
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    
    
    
    
# importações de rotas precisa serem feitas depois da criação do app para evitar erros de importação circular    

from src.routes.auth_routes import auth_router as auth_routes
from src.routes.recovery_routes import recovery_router as recovery_router
from src.routes.ordens_routes import ordens_router as ordens_routes

app.include_router(auth_routes)
app.include_router(ordens_routes)
app.include_router(recovery_router)