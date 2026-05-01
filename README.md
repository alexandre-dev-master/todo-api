#  Notes - Full Stack Task Manager

O **Notes** é uma aplicação completa de gerenciamento de tarefas (To-Do List) desenvolvida para demonstrar a integração entre um backend moderno em **FastAPI** (Python) e um frontend dinâmico em **React**.

## Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web de alta performance.
- **SQLAlchemy**: ORM para manipulação de banco de dados.
- **JWT (JSON Web Tokens)**: Autenticação segura de usuários.
- **SQLite**: Banco de dados relacional para desenvolvimento local.

### Frontend
- **React (Vite)**: Biblioteca para interfaces reativas.
- **Tailwind CSS**: Estilização baseada em utilitários com suporte a Dark Mode.
- **Axios**: Cliente HTTP para comunicação com a API.
- **React Router**: Gerenciamento de navegação e proteção de rotas privadas.

## Funcionalidades

- [x] **Autenticação de Usuários**: Sistema de Login e Registro com criptografia de senhas.
- [x] **Segurança por Token**: Acesso protegido às rotas via JWT (Bearer Token).
- [x] **CRUD Completo de Tarefas**: Criar, visualizar, editar e remover tarefas.
- [x] **Persistência de Dados**: As tarefas são salvas individualmente por usuário no banco de dados.
- [x] **Interface Moderna**: Design inspirado em painéis de produtividade, totalmente responsivo.

## Como Executar o Projeto

### 
1. Clonar o repositório
```bash
git clone [https://github.com/alexandre-dev-master/todo-api.git](https://github.com/alexandre-dev-master/todo-api.git)
cd todo-api

2. Configurar o Backend (Python)
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows: venv\Scripts\activate
# No Linux/Mac: source venv/bin/activate

# Instalar as dependências
pip install -r requirements.txt

# Iniciar o servidor
uvicorn main:app --reload

3. Configurar o Frontend (React)
# Instalar as dependências do Node
npm install

# Iniciar a aplicação
npm run dev


