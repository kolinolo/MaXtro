
""" Função principal, responsável por interpretar e configurar o quando executar uma tarefa """

from componentes.GerenciadorTarefas import montarTarefas
from componentes.Executivo import executar
from apscheduler.schedulers.blocking import BlockingScheduler
from os import system
from dotenv import load_dotenv
from datetime import datetime

import sys

if sys.platform == "win32":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    # Desativa o QuickEdit Mode (0x0040) no terminal atual
    # noinspection PyUnresolvedReferences
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0x0080 | 0x0008)




timezone='America/Sao_Paulo'



load_dotenv(r"MaXtro.env")


system('cls')


scheduler = BlockingScheduler()


tarefas  =  montarTarefas()


indices = {}

for tarefa in tarefas:

    resultado = None

    match(tarefa['trigger']):

        case('interval'):

            scheduler.add_job(
                executar,
                'interval',

                minutes=tarefa['interval_minutes'],

                args=[tarefa],

                id=tarefa['id'],

                max_instances=1
            )

            indices[tarefa['id']] = (f'A cada {tarefa['interval_minutes']}' +
                                     (' minutos' if tarefa['interval_minutes'] > 1 else ' minuto'))


        case('cron'):

            num = -1
            for horario in tarefa['start_time']:

                num = num + 1

                horas = horario.split(':')[0]
                minutos = horario.split(':')[1]

                scheduler.add_job(
                    executar,
                    'cron',

                    hour=horas,
                    minute=minutos,

                    args=[tarefa],

                    id=f"{tarefa['id']}{num}",

                    max_instances=1,

                    timezone= 'America/Sao_Paulo'
                )
            indices[tarefa['id']] = tarefa['start_time']





        case _:
            print('Trigger não definido')


print(f"iniciando MaXtro {datetime.now()}\n")


for ind in indices:

    print(f'{ind} -> {indices[ind]}')

print("\n\n")
scheduler.start()






