import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone 
from jose import jwt
from passlib.context import CryptContext

# 1. Carregamos o arquivo .env
load_dotenv()

# 2. Buscamos as variáveis do sistema (sem expor a senha no código) 🔑
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # 3. O jwt usa as variáveis que vieram do .env
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)