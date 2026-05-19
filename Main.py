from componentes.GerenciadorTarefas import montarTarefas
from componentes.Executivo import executarPython
from apscheduler.schedulers.blocking import BlockingScheduler


from os import system


system('cls')


scheduler = BlockingScheduler()


tarefas  =  montarTarefas()


indices = {}

for tarefa in tarefas:

    resultado = None

    match(tarefa['tipo']):

        case('python'):

            if tarefa['trigger'] == 'interval':
                scheduler.add_job(
                    executarPython,
                    'interval',

                    minutes=tarefa['interval_minutes'],

                    args=[tarefa],

                    id=tarefa['id'],

                    max_instances=1
                )

                indices[tarefa['id']] = (f'A cada {tarefa['interval_minutes']}' +
                                         (' minutos' if tarefa['interval_minutes'] > 1 else ' minuto'))

            else:
                print('Trigger não definido')


print("iniciando MaXtro\n")

for ind in indices:

    print(f'{ind} -> {indices[ind]}')

scheduler.start()






