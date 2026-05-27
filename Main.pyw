""" Função principal, responsável por interpretar e configurar o quando executar uma tarefa """

from dotenv import load_dotenv

load_dotenv(r"MaXtro.env")

from componentes.GerenciadorTarefas import montarTarefas
# Alteração 1: Mudança para o BackgroundScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from os import system
from datetime import datetime
from componentes.Executivo import executar
import sys

# Alteração 2: Importações necessárias para o pystray
import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as item

if sys.platform == "win32":
    import ctypes

    kernel32 = ctypes.windll.kernel32
    # Desativa o QuickEdit Mode (0x0040) no terminal atual
    # noinspection PyUnresolvedReferences
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0x0080 | 0x0008)

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

        print("\nO MaXtro está rodando em segundo plano. Verifique a bandeja do sistema.\n")

    # Alteração 3: Função para gerar um ícone temporário (caso não tenha uma imagem)
    def criar_icone(self):
        # Cria uma imagem 64x64 simples com as letras "MX"
        image = Image.new('RGB', (64, 64), color=(41, 53, 65))
        d = ImageDraw.Draw(image)
        d.text((15, 25), "MX", fill=(255, 255, 255))
        return image

    # Alteração 4: Função para encerrar o programa corretamente pelo menu
    def parar_maxtro(self, icon, item):
        print("Encerrando agendador e saindo...")
        if self.scheduler:
            self.scheduler.shutdown()
        icon.stop()

    def iniciar(self):
        system('cls')

        # Inicializa e inicia o agendador em BACKGROUND (não bloqueia mais o código aqui)
        self.scheduler = BackgroundScheduler(timezone=timezone)
        self.constroiProcessos()
        self.scheduler.start()

        # Configura o menu interativo do Tray Icon
        menu = pystray.Menu(
            item('Sair', self.parar_maxtro)
        )

        # Cria a instância do ícone (Nome interno, Imagem, Texto ao passar o mouse, Menu)
        self.icon = pystray.Icon("MaXtro", self.criar_icone(), "MaXtro Agendador", menu)

        # Roda o ícone (Este comando bloqueia a thread principal e mantém o app vivo)
        self.icon.run()


if __name__ == "__main__":
    OQ = Orquestra()
    OQ.iniciar()