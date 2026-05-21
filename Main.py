from componentes.GerenciadorTarefas import montarTarefas
from componentes.Executivo import executarPython, executaPowerShell


from apscheduler.schedulers.blocking import BlockingScheduler
from os import system
from dotenv import load_dotenv


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

            if tarefa['tipo'] == 'python':
                scheduler.add_job(
                    executarPython,
                    'interval',

                    minutes=tarefa['interval_minutes'],

                    args=[tarefa],

                    id=tarefa['id'],

                    max_instances=1
                )

            elif tarefa['tipo'] == 'powershell':

                scheduler.add_job(
                    executaPowerShell,
                    'interval',

                    minutes=tarefa['interval_minutes'],

                    args=[tarefa],

                    id=tarefa['id'],

                    max_instances=1
                )


            indices[tarefa['id']] = (f'A cada {tarefa['interval_minutes']}' +
                                     (' minutos' if tarefa['interval_minutes'] > 1 else ' minuto'))

        case _:
            print('Trigger não definido')


print("iniciando MaXtro\n")

for ind in indices:

    print(f'{ind} -> {indices[ind]}')

print("\n\n")
scheduler.start()






