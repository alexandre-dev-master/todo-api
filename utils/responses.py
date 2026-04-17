# =========================
# HELPER GLOBAL DE RESPOSTA
# =========================
from typing import Any, Optional

def api_response(success: bool, message: str, data: Any = None, meta: Optional[dict] = None):
    # Função que garante que toda resposta da API tenha a mesma cara
    # Isso evita repetir dicionários manuais nos services
    
    return {
        "success": success,
        "message": message,
        "data": data,
        "meta": meta
    }