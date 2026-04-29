from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate  # <--- FALTAVA ISSO!
from auth import hash_password, verify_password, create_access_token

# =========================
# REGISTRO
# =========================
def create_user_service(user: UserCreate, db: Session):
    hashed = hash_password(user.password)
    
    # Usando 'password' pq é o que está no seu models.py
    new_user = User(email=user.email, password=hashed) 

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Removi o api_response aqui para não dar erro de "not defined" 
    # se você ainda não criou essa função. Retornar o objeto é mais seguro.
    return new_user

# =========================
# LOGIN
# =========================
def login_user_service(email_fornecido: str, password: str, db: Session):
    # Mudado de User.username para User.email (conforme seu models.py)
    user = db.query(User).filter(User.email == email_fornecido).first()

    # Verificando contra user.password (conforme seu models.py)
    if not user or not verify_password(password, user.password):
        return None 

    token_data = {
        "sub": user.email, 
        "role": getattr(user, 'role', 'user')
    }
    
    token = create_access_token(token_data) 
    return token