from datetime import datetime, timedelta, timezone 
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "sua-chave-secreta-aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """
    Gera o hash de uma senha utilizando o algoritmo bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    """
    Compara uma senha em texto plano com um hash armazenado.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """
    Gera um token JWT com tempo de expiracao configurado.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)