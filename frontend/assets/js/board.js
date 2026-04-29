/**
 * GERENCIADOR DO QUADRO (BOARD)
 * Responsável por buscar, renderizar e manipular os cards de tarefas na UI.
 */

/**
 * Solicita ao backend a lista de tarefas vinculadas ao usuário logado.
 * @async
 * @returns {Promise<void>}
 */
async function loadTasksFromBackend() {
    const token = localStorage.getItem(STORAGE_KEY);
    if (!token) return;

    try {
        const response = await fetch(`${BASE_API}/tasks/`, {
            method: 'GET',
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        const result = await handleResponse(response);
        
        // Limpa o container do board para evitar duplicatas ao recarregar
        const board = document.getElementById('board');
        board.innerHTML = "";
        
        // Renderiza cada tarefa retornada pelo banco de dados
        // Assume-se que result.data é um Array de objetos
        result.data.forEach(task => renderCard(task.title));
        
        // Atualização visual do indicador de status do sistema
        const statusTag = document.getElementById('status-tag');
        if (statusTag) {
            statusTag.innerText = "SISTEMA_ONLINE";
            statusTag.classList.replace('bg-blue-900', 'bg-green-900');
        }

    } catch (err) {
        console.error("[Board Error]:", err.message);
    }
}

/**
 * Cria e injeta o elemento HTML de um card no DOM.
 * @param {string} title - O título ou descrição da tarefa.
 */
function renderCard(title) {
    const board = document.getElementById('board');
    const card = document.createElement('div');
    
    // Classes do Tailwind para o design Dark/Cyberpunk
    card.className = "bg-slate-800 p-4 rounded-xl border border-slate-700 hover:border-blue-500 transition-all cursor-pointer group";
    
    card.innerHTML = `
        <div class="flex items-center justify-between">
            <span class="text-slate-100 font-mono text-sm">${title.toUpperCase()}</span>
            <div class="h-2 w-2 rounded-full bg-slate-600 group-hover:bg-blue-500"></div>
        </div>
    `;
    
    board.appendChild(card);
}