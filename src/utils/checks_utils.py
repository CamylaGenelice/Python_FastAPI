import re
import random

def validar_email(email: str) -> bool:
    try:

        padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        
        if not re.fullmatch(padrao,email):
            print('email inválido')
            return False
       
        return True
    
    except Exception as e:
        print(f"DEBUG validar_email: Erro ao validar email '{email}': {e}")
        return False


def validar_nome(nome: str) -> bool:
    try:

        padrao = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$'
        
        if not re.fullmatch(padrao, nome):
            print('nome inválido')
            return False
       
        return True
    
    except Exception as e:
        print(f'DEBUG validar_nome: Nome inválido:{nome}')

def validar_senha(senha: str) -> bool:

    try:
        padrao = re.compile(r'^[A-Za-z0-9!@#$%^&*(),.?":{}|<>_-]+$')

        if len(senha) < 7:
            #print('Tamanho da senha é menor do que o esperado')
            return False
        
        if not padrao.match(senha):
            return False
        
        return True
    
        
    except Exception as e:
        print('Erro na validação da senha: ',e)
        return False
    

def gera_numero() -> int:
    numero = random.randint(100000, 999999) # garante 6 dígitos
    print(numero)
    return numero