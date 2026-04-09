from fastapi import FastAPI
# importa o FastAPI, usado para criar APIs

app = FastAPI()
# cria a aplicação (sua API)

tasks = [
    {"id": 1, "title": "Estudar Python", "done": True},
    {"id": 2, "title": "Treinar API", "done": False}

]
# lista de tarefas em memória (simula um banco de dados)

print("task created")
#testar git

@app.get("/")
# define uma rota GET na raiz "/"

def home():
# função que será executada quando acessar "/"
    
    return {"message": "ToDo API funcionando!"}
    # retorna um JSON como resposta

@app.get("/tasks")
# define uma rota GET em "/tasks"

def get_tasks():
# função executada ao acessar "/tasks"

    return tasks
    # retorna a lista de tarefas

@app.post("/tasks")
# define rota POST para criar nova tarefa

def create_task(task: dict):
# recebe um dicionário enviado pelo usuário
# "task: dict" = tipo esperado (dicionário)

    new_task = {
        "id": len(tasks) + 1,
        # cria id automático baseado no tamanho da lista

        "title": task["title"],
        # pega o título enviado pelo usuário

        "done": False
        # toda tarefa começa como não concluída
    }

    tasks.append(new_task)
    # adiciona a nova tarefa na lista

    return new_task
    # retorna a tarefa criada

@app.delete("/tasks/{task_id}")
# define rota DELETE com parâmetro na URL

def delete_task(task_id: int):
# recebe o id da tarefa como número inteiro

    for task in tasks:
    # percorre cada tarefa da lista
    # treina: loop e busca

        if task["id"] == task_id:
        # verifica se o id da tarefa é igual ao recebido

            tasks.remove(task)
            # remove a tarefa da lista

            return {"message": "Tarefa removida"}
            # retorna mensagem de sucesso

    return {"error": "Tarefa não encontrada"}
    # retorna erro se não achar a tarefa

@app.put("/tasks/{task_id}")
# define rota PUT para atualizar tarefa

def update_task(task_id: int, updated_data: dict):
# recebe o id da tarefa e os novos dados enviados pelo usuário
# "updated_data: dict" = corpo da requisição

    for task in tasks:
    # percorre todas as tarefas da lista

        if task["id"] == task_id:
        # verifica se encontrou a tarefa com esse id

            task["title"] = updated_data.get("title", task["title"])
            # atualiza o título se vier no request
            # se não vier, mantém o valor atual

            task["done"] = updated_data.get("done", task["done"])
            # atualiza o status se vier
            # se não vier, mantém o atual

            return task
            # retorna a tarefa atualizada

    return {"error": "Tarefa não encontrada"}
    # retorna erro se não achar a tarefa