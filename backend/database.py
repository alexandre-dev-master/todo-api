# importa função que cria a conexão com o banco
from sqlalchemy import create_engine

# importa ferramentas pra trabalhar com sessões e modelos (POO)
from sqlalchemy.orm import sessionmaker, declarative_base


# 🔗 URL do banco de dados
# sqlite:///./todo.db → cria um arquivo chamado todo.db na pasta do projeto
DATABASE_URL = "sqlite:///./todo.db"


# ⚙️ ENGINE = conexão com o banco
# é o "motor" que permite o Python falar com o banco
engine = create_engine(
    DATABASE_URL,

    # necessário pro SQLite funcionar corretamente com FastAPI
    connect_args={"check_same_thread": False}
)


# 🧠 SESSION = comunicação com o banco
# cada requisição da API usa uma sessão pra acessar dados
SessionLocal = sessionmaker(

    # não salva automaticamente (você controla quando salvar)
    autocommit=False,

    # não sincroniza automaticamente (melhor performance)
    autoflush=False,

    # conecta essa sessão ao engine (banco)
    bind=engine
)


# 🧱 BASE = base para criar modelos (POO)
# daqui você vai criar classes que viram tabelas no banco
Base = declarative_base()


# =========================
# CONEXÃO PADRÃO COM BANCO (DEPENDENCY FASTAPI)
# =========================
def get_db():
    # cria uma nova sessão com o banco

    db = SessionLocal()

    try:
        # entrega a conexão para a rota usar
        yield db

    finally:
        # garante que a conexão sempre será fechada
        db.close()