from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from auth import hash_password, verify_password, create_access_token
from utils.responses import api_response

# =========================
# REGISTRO
# =========================
def create_user_service(user: UserCreate, db: Session):
    hashed = hash_password(user.password)
    new_user = User(username=user.username, password=hashed)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return api_response(
        success=True,
        message="User registered successfully",
        data={"username": new_user.username}
    )

# =========================
# LOGIN
# =========================
# services/auth_service.py

def login_user_service(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password):
        return None # O controller vai tratar isso

   
    token = create_access_token({
        "sub": user.username, 
        "role": user.role  # Colocamos usuário e role no token
    }) 
    # 🆕 AGORA PASSAMOS O USERNAME E A ROLE PARA O TOKEN

    return token