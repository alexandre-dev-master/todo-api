from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import get_db
from models import User
# Importações para validação de tokens e consulta de persistência

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
# Configuração do esquema de autenticação via Bearer Token

SECRET_KEY = "sua_chave_secreta_aqui"
ALGORITHM = "HS256"
# Constantes criptográficas para decodificação do JWT

# =========================
# VALIDAR ACESSO (JWT)
# =========================
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou expiradas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Definição da exceção para falhas de integridade do token

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Extração do subject (username) do payload decodificado
    except JWTError:
        raise credentials_exception
    # Tratamento de erro para assinaturas inválidas ou tokens corrompidos

    user = db.query(User).filter(User.username == username).first()
    # Recuperação da entidade User para acessar atributos de perfil e cargo

    if user is None:
        raise credentials_exception
    # Garantia de que o usuário detentor do token ainda existe na base

    return {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }
    # Retorno do payload de identidade para consumo nos Services e Routes