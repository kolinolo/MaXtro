import os

from componentes.utilitarios import diretorio,carregaJSON, verde, vermelho
from componentes.Exceptions import NotJsonException, TarefaInvalida



def verificaTipo(js):

    match js['tipo']:

        case 'python':

            parFaltante = []

            for par in ['id','enabled','python_path','working_dir','script']:

                if par not in js:
                    parFaltante.append(par)

                if len(parFaltante) > 0:
                    raise TarefaInvalida(f'parâmetros Python não configurados: {parFaltante}')


    interval =  'interval_minutes' in js
    startTime = 'start_time' in js

    if not( interval or startTime):

        raise TarefaInvalida('Horário ou intervalo de execução não definido, tarefa sera ignorada')

    elif interval and startTime:
        raise TarefaInvalida('Horário e intervalo de execução definidos ao mesmo tempo')

    return True





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

        except TarefaInvalida as e :
            vermelho(f"{t} -> {e.mensagem}")








    return tarefasValidas




