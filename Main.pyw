""" Função principal, responsável por interpretar e configurar o quando executar uma tarefa """

from dotenv import load_dotenv

load_dotenv(r".env")

from componentes.GerenciadorTarefas import montarTarefas

from apscheduler.schedulers.blocking import BlockingScheduler
from os import system
from datetime import datetime
from componentes.Executivo import executar
import sys

# Alteração 2: Importações necessárias para o pystray
#import pystray
#from PIL import Image, ImageDraw
#from pystray import MenuItem as item
#
#if sys.platform == "win32":
#    import ctypes
#
#    kernel32 = ctypes.windll.kernel32
#    # Desativa o QuickEdit Mode (0x0040) no terminal atual
#    # noinspection PyUnresolvedReferences
#    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0x0080 | 0x0008)

timezone = 'America/Sao_Paulo'


class Orquestra:

    def __init__(self):
        self.scheduler = None
        self.icon = None  # Referência para o ícone do tray

    def constroiProcessos(self):
        tarefas = montarTarefas()
        indices = {}

        for tarefa in tarefas:
            match (tarefa['trigger']):
                case ('interval'):
                    self.scheduler.add_job(
                        executar,
                        'interval',
                        minutes=tarefa['interval_minutes'],
                        args=[tarefa],
                        id=tarefa['id'],
                        max_instances=1
                    )
                    indices[tarefa['id']] = (f"A cada {tarefa['interval_minutes']}" +
                                             (" minutos" if tarefa['interval_minutes'] > 1 else " minuto"))

                case ('cron'):
                    num = -1
                    for horario in tarefa['start_time']:
                        num = num + 1
                        horas, minutos = horario.split(':')

                        self.scheduler.add_job(
                            executar,
                            'cron',
                            hour=horas,
                            minute=minutos,
                            args=[tarefa],
                            id=f"{tarefa['id']}{num}",
                            max_instances=1,
                            timezone=timezone
                        )
                    indices[tarefa['id']] = tarefa['start_time']

                case _:
                    print('Trigger não definido')

        print(f"Iniciando MaXtro {datetime.now()}\n")

        for ind in indices:
            print(f'{ind} -> {indices[ind]}')

        print("\nO MaXtro está rodando\n")



    def iniciar(self):

        self.scheduler = BlockingScheduler(timezone=timezone)
        self.constroiProcessos()
        self.scheduler.start()




if __name__ == "__main__":
    OQ = Orquestra()
    OQ.iniciar()