import re

def validar_email(email):
    
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    
    if not re.fullmatch(padrao,email):
        return False
    return True

def validar_nome(nome):
    
    padrao = [A-Za-zÀ-ÖØ-öø-ÿ]
    
    if not re.fullmatch(padrao, nome):
        return False
    return True
