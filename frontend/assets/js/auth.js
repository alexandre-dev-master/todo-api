    /**
     * SERVIÇO DE AUTENTICAÇÃO - CHAOS BOARD
     * Este módulo gerencia o fluxo de identidade do usuário, incluindo login,
     * registro e persistência de sessão via JWT.
     */

    /**
     * Realiza a autenticação do usuário junto à API.
     * @async
     * @returns {Promise<void>}
     */
    async function realizarLogin() {
    // 1. Você precisa pegar os valores dos campos (estava faltando!)
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const erroMsg = document.getElementById('login-erro');

    try {
        // 2. Você PRECISA definir o params aqui para o body lá embaixo funcionar
        const params = new URLSearchParams();
        params.append('username', email);
        params.append('password', password);

        const response = await fetch(`${BASE_API}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: params // Agora o JS sabe o que é 'params'
        });

        const result = await handleResponse(response);
                
        if (result.access_token) {
            localStorage.setItem(STORAGE_KEY, result.access_token);
            console.log("Token guardado com sucesso!");
            
            document.getElementById('login-modal').classList.add('hidden');
            loadTasksFromBackend(); 
        }

    } catch (err) {
        console.error("Erro no login:", err);
        if (erroMsg) {
            erroMsg.innerText = err.message;
            erroMsg.classList.remove('hidden');
        }
    }
    }

    /**
     * Registra um novo usuário no sistema.
     * @async
     * @returns {Promise<void>}
     */
    async function realizarCadastro() {
        const email = document.getElementById('reg-email').value;
        const password = document.getElementById('reg-password').value;
        const erroMsg = document.getElementById('reg-erro');

        // Validação de entrada básica (Client-side)
        if (!email || !password) {
            erroMsg.innerText = "Campos obrigatórios ausentes.";
            erroMsg.classList.remove('hidden');
            return;
        }

        try {
            const response = await fetch(`${BASE_API}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    email: email, 
                    password: password 
                })
            });

            await handleResponse(response);
            
            // Feedback de sucesso e redirecionamento de fluxo
            alert("REGISTRO_CONCLUÍDO. Prossiga com o login.");
            alternarModais();
            
            // Reset de campos para segurança
            document.getElementById('reg-email').value = "";
            document.getElementById('reg-password').value = "";

        } catch (err) {
            erroMsg.innerText = err.message || "Erro ao processar registro.";
            erroMsg.classList.remove('hidden');
        }
    }

    /**
     * Alterna a visibilidade entre os formulários de Login e Registro.
     */
    function alternarModais() {
        const loginModal = document.getElementById('login-modal');
        const registerModal = document.getElementById('register-modal');
        
        loginModal.classList.toggle('hidden');
        registerModal.classList.toggle('hidden');
    }

    /**
     * Encerra a sessão do usuário e limpa os dados locais.
     */
    function logout() {
        localStorage.removeItem(STORAGE_KEY);
        // Reload garante que todos os estados do app sejam resetados
        location.reload();
    }