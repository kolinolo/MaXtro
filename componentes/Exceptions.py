
# utilitários:
class NotJsonException(Exception):
    pass


# gereciadorTarefas:


class TarefaInvalida(Exception):
    def __init__(self, mensagem):

        self.mensagem = mensagem
