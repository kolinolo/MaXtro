import os

from componentes.utilitarios import diretorio,carregaJSON, verde, vermelho
from componentes.Exceptions import NotJsonException, TarefaInvalida, IntervaloMalDefinido


def verificaTipo(js):

    parFaltante = []
    exigido = []

    match js['tipo']:

        case 'python':

            exigido = ['id','enabled','python_path','working_dir','script']



        case 'powershell':

            exigido = ['id', 'enabled', 'working_dir','script']

        case _:
            print(f'Tipo de execução não configurada {js['tipo']}')


    for par in exigido:

        if par not in js:
            parFaltante.append(par)

        if len(parFaltante) > 0:
            raise TarefaInvalida(f'parâmetros {js['tipo']} não configurado(s): {parFaltante}')

    interval =  'interval_minutes' in js
    startTime = 'start_time' in js

    if not( interval or startTime):

        raise TarefaInvalida('Horário ou intervalo de execução não definido, tarefa sera ignorada')

    elif interval and startTime:
        raise TarefaInvalida('Horário e intervalo de execução definidos ao mesmo tempo')


    if 'time_range'  in js:
        if len(js['time_range']) != 13:
            raise IntervaloMalDefinido(f"intervalo de {js['id']} mal definido ({js['time_range']})")







def montarTarefas() -> list:
    tarefasValidas = []

    tarefas = os.listdir(diretorio('tarefas'))

    for t in tarefas:
        try:

            js = carregaJSON(diretorio(fr"tarefas\{t}"))

            verificaTipo(js)

            if 'interval_minutes' in js:
                js['trigger'] = 'interval'

            elif 'start_time' in js:
                js['trigger'] = 'start_time'

            if js['enabled']:
                tarefasValidas.append(js)

        except  NotJsonException:

            vermelho(f"{t} Não é um arquivo Json, tarefa sera ignorada")

        except TarefaInvalida or IntervaloMalDefinido as e:
            vermelho(f"{t} -> {e.mensagem}")








    return tarefasValidas




