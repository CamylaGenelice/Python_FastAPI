from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get('/')
async def autenticacao():
    """Rota de autenticação, teste de explicação da documentação."""
    return {"message": "Rota de autenticação", "autenticado": False}