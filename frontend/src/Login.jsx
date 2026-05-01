import React, { useState } from 'react';
import api from './services/api';
import { useNavigate } from 'react-router-dom'; // Importante para mudar de página
import { Link } from 'react-router-dom';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await api.post('/login', formData);
      const token = response.data.access_token;
      localStorage.setItem('access_token', token);
      
      alert("Sucesso! Você está autenticado.");
      navigate('/dashboard'); // Redireciona para o Dashboard após o OK
    } catch (error) {
      console.error("Erro no login:", error.response?.data || error.message);
      alert("Erro ao conectar com o Backend.");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center text-white font-sans">
      <div className="bg-slate-900 p-8 rounded-2xl shadow-2xl border border-slate-800 w-96">
        <h1 className="text-3xl font-black mb-2 text-blue-500">Notes</h1>
        <p className="text-slate-400 mb-6 text-sm">Foco no Backend, estilo no Frontend.</p>
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase text-slate-500 mb-1">Usuário</label>
            <input 
              type="text" 
              className="w-full bg-slate-800 border border-slate-700 p-3 rounded-lg focus:outline-none focus:border-blue-500 transition-all"
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-xs font-bold uppercase text-slate-500 mb-1">Senha</label>
            <input 
              type="password" 
              className="w-full bg-slate-800 border border-slate-700 p-3 rounded-lg focus:outline-none focus:border-blue-500 transition-all"
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-lg mt-4 transition-colors">
            ACESSAR SISTEMA
          </button>
        </form>
        <div className="mt-6 text-center">
          <p className="text-sm text-slate-500">
            Ainda não tem uma conta?{' '}
            <Link 
              to="/register" 
              className="text-blue-500 hover:text-blue-400 font-bold transition-colors underline underline-offset-4"
            >
              Cadastre-se aqui
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;