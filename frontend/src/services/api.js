import axios from 'axios';

// Cria uma "instância" do Axios. 
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000' 
});

// Esse interceptor é AUTOMÁTICO: 
// Ele checa se você tem um token e coloca no cabeçalho antes de enviar pro Python.
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;