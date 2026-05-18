from componentes.GerenciadorTarefas import montarTarefas
from componentes.Executivo import executarPython

from apscheduler.schedulers.blocking import BlockingScheduler


scheduler = BlockingScheduler()



tarefas  =  montarTarefas()



for tarefa in tarefas:

    resultado = None

    match(tarefa['tipo']):

        case('python'):

            scheduler.add_job(
                executarPython,
                'interval',

                minutes=tarefa['interval_minutes'],

                args=[tarefa],

                id=tarefa['id'],

                max_instances=1
            )



print("iniciando MaXtro")
scheduler.start()






