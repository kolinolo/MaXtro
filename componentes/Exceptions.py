
# utilitários:
class NotJsonException(Exception):
    pass


# gereciadorTarefas:


class TarefaInvalida(Exception):
    def __init__(self, mensagem):

        self.mensagem = mensagem


class ErroExecutandoPython(Exception):

    def __init__(self, mensagem,resultado):

        self.mensagem = mensagem
        self.infos = resultado


class IntervaloMalDefinido(Exception):
    def __init__(self, mensagem):
        self.mensagem = mensagem
