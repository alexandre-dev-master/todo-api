# =========================
# EXCEÇÃO CUSTOMIZADA
# =========================
class TaskNotFoundException(Exception):
    # erro usado quando tarefa não existe

    def __init__(self, message="Task not found"):
        # mensagem padrão

        self.message = message
        super().__init__(self.message)
        # inicializa Exception com mensagem