

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

class DiaMalDefinido (Exception):

    def __init__(self, atual):
        self.atual = atual
        self.mensagem = f"""Dia da semana mal definido {atual},
        
-Possíveis dias :mon','tue','wed','thu','fri','sat','sun'
-Intervalos deve seguir o padrão 'inicio-fim' (sem espaços)"""
