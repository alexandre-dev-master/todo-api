import React, { useEffect, useState } from 'react';
import api from './services/api';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => { fetchTasks(); }, []);

  const fetchTasks = async () => {
    try {
      const response = await api.get('/tasks/');
      const lista = response.data.data || response.data;
      setTasks(Array.isArray(lista) ? lista : []);
    } catch (err) { console.error(err); } 
    finally { setLoading(false); }
  };

  const addTask = async (e) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;
    try {
      await api.post('/tasks/', { title: newTaskTitle, description: "", is_done: false });
      setNewTaskTitle('');
      fetchTasks();
    } catch (err) { console.error(err); }
  };

  const toggleTask = async (task) => {
  // 1. Atualiza na tela primeiro (Otimista)
  const novasTasks = tasks.map(t => 
    t.id === task.id ? { ...t, is_done: !t.is_done } : t
  );
  setTasks(novasTasks);

  try {
    // 2. Tenta avisar o Python
    // Verifique se a rota é /tasks/{id} ou se seu Python exige a barra no final /tasks/{id}/
    await api.put(`/tasks/${task.id}/`, { 
      title: task.title, 
      description: task.description || "", 
      is_done: !task.is_done 
    });
  } catch (err) {
    console.error("Erro ao sincronizar com o banco:", err);
    // Se der erro, volta ao estado anterior
    fetchTasks();
    alert("O servidor não salvou a alteração.");
  }
};

  const deleteTask = async (id) => {
    if (!confirm("Excluir tarefa?")) return;
    try {
      await api.delete(`/tasks/${id}`);
      setTasks(tasks.filter(t => t.id !== id));
    } catch (err) { console.error(err); }
  };

  const editTask = async (task) => {
    const newTitle = prompt("Novo nome:", task.title);
    if (newTitle && newTitle !== task.title) {
      try {
        await api.put(`/tasks/${task.id}`, { ...task, title: newTitle });
        fetchTasks();
      } catch (err) { console.error(err); }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8 font-sans">
      <div className="max-w-2xl mx-auto">
        
        <div className="flex justify-between items-center mb-8 border-b border-slate-800 pb-4">
          <h1 className="text-3xl font-black text-blue-500">Notes</h1>
          <button onClick={handleLogout} className="bg-red-900/20 hover:bg-red-600 text-red-500 hover:text-white px-4 py-2 rounded-lg text-sm font-bold border border-red-900/50 transition-all">
            SAIR
          </button>
        </div>

        <form onSubmit={addTask} className="flex gap-2 mb-8">
          <input 
            type="text" 
            placeholder="Nova tarefa..." 
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            className="flex-1 bg-slate-900 border border-slate-800 p-3 rounded-xl focus:border-blue-500 outline-none"
          />
          <button type="submit" className="bg-blue-600 hover:bg-blue-500 px-6 py-3 rounded-xl font-bold transition-all">
            ADICIONAR
          </button>
        </form>

        {loading ? (
          <p className="text-center text-slate-500">Carregando...</p>
        ) : (
          <div className="space-y-3">
            {tasks.map(task => (
              <div key={task.id} className="flex items-center bg-slate-900 p-4 rounded-xl border border-slate-800 transition-all">
                
                {/* Deletar (X) */}
                <button onClick={() => deleteTask(task.id)} className="text-slate-600 hover:text-red-500 mr-4 font-bold text-xl">
                  ✕
                </button>

                {/* CHECKBOX CUSTOMIZADO COM "V" VERDE */}
                <button 
                  onClick={() => toggleTask(task)}
                  className={`w-6 h-6 rounded-md border-2 mr-4 flex items-center justify-center transition-all ${
                    task.is_done 
                      ? 'bg-green-500 border-green-500' 
                      : 'bg-transparent border-slate-700 hover:border-slate-500'
                  }`}
                >
                  {task.is_done && (
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={4}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                  )}
                </button>

                <span 
                  onClick={() => editTask(task)}
                  className={`flex-1 cursor-pointer text-lg ${task.is_done ? 'line-through text-slate-600' : 'text-slate-200'}`}
                >
                  {task.title}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;