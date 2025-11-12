# uvicorn main:app --reload para rodar o servidor
# app é a variavel do fastAPI que vai ser criada

from fastapi import FastAPI

app = FastAPI()
    
# importações de rotas precisa serem feitas depois da criação do app para evitar erros de importação circular    

from src.routes.auth_routes import auth_router as auth_routes
from src.routes.ordens_routes import ordens_router as ordens_routes

app.include_router(auth_routes)
app.include_router(ordens_routes)