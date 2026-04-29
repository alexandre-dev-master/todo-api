/**
 * CONFIGURAÇÃO GLOBAL DA API - CHAOS BOARD
 * Este arquivo centraliza a comunicação com o servidor Backend.
 */

// URL base do servidor FastAPI. Mude aqui para o IP do servidor no deploy.
const BASE_API = "http://127.0.0.1:8000";

// Chave utilizada para identificar o Token JWT no armazenamento local.
const STORAGE_KEY = "meu_token_jwt";

/**
 * Filtro global de respostas da API.
 * Gerencia a conversão de JSON e trata erros de autenticação (401).
 * @async
 * @param {Response} response - Objeto de resposta do Fetch API.
 * @throws {Error} Lança um erro com a mensagem vinda do servidor ou padrão.
 * @returns {Promise<any>} Dados convertidos do corpo da resposta.
 */
async function handleResponse(response) {
    // Se o servidor retornar 401 (Unauthorized), o token expirou ou é inválido
    if (response.status === 401) {
        localStorage.removeItem(STORAGE_KEY);
        document.getElementById('login-modal').classList.remove('hidden');
        throw new Error("Sessão expirada. Por favor, realize o login novamente.");
    }
    
    const data = await response.json();
    
    // Se a resposta não estiver no range 200-299, captura o erro do FastAPI (detail)
    if (!response.ok) {
        throw new Error(data.detail || "Ocorreu um erro inesperado no servidor.");
    }
    
    return data;
}