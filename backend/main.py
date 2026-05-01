"""
ENTRY POINT - BACKEND API
Este é o arquivo central que orquestra o servidor FastAPI.
Integra rotas de autenticação, gestão de tarefas e configuração de segurança (CORS).
"""
#SPA (Single Page Application) com autenticação JWT, consumindo API assíncrona em FastAPI 
# e persistência em banco de dados SQL

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import task_routes, auth_routes
from database import engine, Base

# --- PERSISTÊNCIA DE DADOS ---
# O comando abaixo verifica os modelos definidos e cria as tabelas no SQLite
# automaticamente se elas ainda não existirem. Essencial para o primeiro "boot".
Base.metadata.create_all(bind=engine)

# --- INICIALIZAÇÃO DA API ---
app = FastAPI(
    title="Chaos Board API", 
    version="1.0.0",
    # O parâmetro abaixo mantém o cadeado do Swagger aberto após o login (melhora o teste)
    swagger_ui_parameters={"persistAuthorization": True}
)

# --- MIDDLEWARE DE SEGURANÇA (CORS) ---
# Necessário para que o  Frontend consiga consumir esta API
# sem ser bloqueado pela política de mesma origem do navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True, # Isso permite que o navegador envie o Token com segurança
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INJEÇÃO DE ROTAS (ROUTERS) ---
# Separar as rotas em arquivos diferentes mantém o código escalável e limpo.
app.include_router(auth_routes.router) # Endpoints de /login e /register
app.include_router(task_routes.router) # Endpoints de /tasks

@app.get("/")
def health_check():
    """
    Endpoint de verificação de integridade (Health Check).
    Útil para monitoramento e para o Docker saber se o container está vivo.
    """
    return {
        "status": "SISTEMA_ONLINE", 
        "version": "1.0.0",
        "message": "Chaos Board API operando normalmente."
    }