import React, { useState } from 'react';
import api from './services/api';
import { useNavigate, Link } from 'react-router-dom';

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Enviando exatamente o que o seu Python espera no schemas.py
      // Remova o '/users/' e use apenas '/register'
      await api.post('/register', { 
        email: email, 
        password: password 
      });
      
      alert("Conta criada com sucesso! Redirecionando para o login...");
      navigate('/'); // Volta para a tela de login
    } catch (error) {
      console.error("Erro no cadastro:", error.response?.data);
      // Pega a mensagem de erro vinda do FastAPI (ex: "Email já cadastrado")
      const errorDetail = error.response?.data?.detail || "Erro ao criar conta.";
      alert(errorDetail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-white font-sans p-4">
      <div className="bg-slate-900 p-8 rounded-2xl shadow-2xl border border-slate-800 w-full max-w-md">
        
        <div className="mb-8">
          <h1 className="text-3xl font-black text-blue-500">Criar Conta</h1>
          <p className="text-slate-400 mt-2">Cadastre-se para gerenciar suas tarefas.</p>
        </div>
        
        <form onSubmit={handleRegister} className="space-y-5">
          <div>
            <label className="block text-xs font-bold uppercase text-slate-500 mb-2">E-mail</label>
            <input 
              type="email" 
              required
              placeholder="seu@email.com"
              className="w-full bg-slate-800 border border-slate-700 p-3 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all text-slate-200"
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase text-slate-500 mb-2">Senha</label>
            <input 
              type="password" 
              required
              placeholder="••••••••"
              className="w-full bg-slate-800 border border-slate-700 p-3 rounded-xl focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all text-slate-200"
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button 
            type="submit"
            disabled={loading}
            className={`w-full font-bold py-4 rounded-xl mt-4 transition-all shadow-lg ${
              loading 
                ? 'bg-slate-700 cursor-not-allowed text-slate-400' 
                : 'bg-blue-600 hover:bg-blue-500 text-white shadow-blue-900/20'
            }`}
          >
            {loading ? 'CADASTRANDO...' : 'CRIAR MINHA CONTA'}
          </button>
        </form>
        
        <div className="mt-8 text-center border-t border-slate-800 pt-6">
          <p className="text-sm text-slate-500">
            Já tem uma conta?{' '}
            <Link 
              to="/" 
              className="text-blue-500 hover:text-blue-400 font-bold transition-colors underline underline-offset-4"
            >
              Fazer Login
            </Link>
          </p>
        </div>

      </div>
    </div>
  );
}

export default Register;