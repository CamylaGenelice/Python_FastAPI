from jose import jwt, JWTError
from fastapi import HTTPException, status
from datetime import timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv('SECRET_KEY_TOKEN')
algorithm = os.getenv('ALGORITHM')
expire_minutes = int(os.getenv('EXPIRE_MINUTES'))

def criar_token(dados: dict):
    try:
        payload = dados.copy() #cria uma copia dos dados que foram enviados
        payload['exp'] = timezone.utc + timedelta(minutes=expire_minutes)
        return jwt.encode(payload, secret_key, algorithm=algorithm)
    
    except Exception as e:
        print(f'Erro ao criar token {e}')
        raise e

def validar_token(token: str) -> dict:

    try:
        payload = jwt.decode(token=token, secret_key=secret_key, algorithms=[algorithm])

        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException (
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail='TOKEN inválido'
            )
        return payload
    
    except JWTError:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )

