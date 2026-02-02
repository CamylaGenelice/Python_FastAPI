from jose import jwt, JWTError
import time
from datetime import datetime, timedelta, timezone

secret_key = "minha_chave_secreta" 
algorithm = "HS256" 
expire_minutes = 1

def teste_token(dados: dict):
   
   payload = dados.copy()
   payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)

   return jwt.encode(payload,secret_key,algorithm)

def teste_criacao_token():
   
   dados = {'id_user':12,'role':'admin'}
   token = teste_token(dados=dados)
   decoded = jwt.decode(token, secret_key, algorithms=[algorithm])

   assert decoded['id_user'] == 12
   assert decoded['role'] == 'admin'

def teste_expiracao():
   dados = {'id_user':123}
   token = teste_token(dados=dados)
   decoded = jwt.decode(token, secret_key, algorithm)

   assert 'exp' in decoded

   time.sleep(30)

   try:
      jwt.decode(token=token, secret_key= secret_key, algorithms=[algorithm])

      assert False, 'Token deveria estar expirado'

   except Exception as e:
      assert True