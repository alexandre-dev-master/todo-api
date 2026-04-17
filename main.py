from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from database import engine, Base
from routes import task_routes, auth_routes
from utils.responses import api_response
from fastapi.exceptions import HTTPException
# Importações estruturais para o core da aplicação

app = FastAPI()

# =========================
# DATABASE INTEGRITY
# =========================
Base.metadata.create_all(bind=engine)
# Garante a persistência do schema no SQLite durante o startup

# =========================
# EXCEPTION HANDLER (HTTP)
# =========================
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=api_response(
            success=False,
            message=exc.detail,
            data=None
        )
    )
    # Intercepta exceções controladas para normalização do envelope de saída

# =========================
# GLOBAL ERROR CATCH-ALL
# =========================
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=api_response(
            success=False,
            message="Internal Server Error: consulte os logs para mais detalhes.",
            data=None
        )
    )
    # Middleware de última instância para evitar vazamento de stacktrace em produção

# =========================
# ROUTE REGISTRATION
# =========================
app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])
# Injeção das rotas de negócio com versionamento implícito via prefixo
app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
# Módulo de segurança e gerenciamento de identidade (Identity Provider)