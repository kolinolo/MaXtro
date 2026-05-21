import os, json
from datetime import datetime
from componentes.printTool import configColorizar
from componentes.Exceptions import NotJsonException


dias = {

    'mon':0,
    'tue':1,
    'wed':2,
    'thu':3,
    'fri':4,
    'sat':5,
    'sun':6,

}


def diretorio(caminho, cwd = True) -> str:

    """ converte o caminho para padrão linux ou windows e coloca o CWD como prefixo """

    if os.name == "nt":
        caminho = caminho.replace("/", "\\")

        if cwd:
            caminho = f'{os.getcwd()}\\{caminho}'

    else:
        caminho = caminho.replace("\\","/")
        if cwd:
            caminho = fr'{os.getcwd()}/{caminho}'

    return caminho


def carregaJSON(caminho):


    if not caminho.endswith(".json"):
        raise NotJsonException()

    with open(caminho, "rb") as file:
        return json.load(file)


def inTimeRange(tarefa:dict)-> bool:

    if 'time_range' not in tarefa:
        return True

    inicial = tarefa['time_range'].split(' - ')[0]
    final = tarefa['time_range'].split(' - ')[1]

    agora = datetime.now()
    agora = agora.strftime("%H:%M")

    if (agora >= inicial) and (agora <= final):
        return True


    else:
        print(f"{tarefa['id']} Fora do periodo de execução")
        return False

def inDay(tarefa:dict)-> bool:

    if 'day_of_week' not in tarefa:
        return True

    if '-' in tarefa['day_of_week']:
        inicial = tarefa['day_of_week'].split('-')[0]
        final = tarefa['day_of_week'].split('-')[1]

    else:
        inicial = tarefa['day_of_week']
        final = tarefa['day_of_week']




    inicial = dias[inicial]
    final = dias[final]




    agora = datetime.now()
    agora = agora.weekday()

    if (agora >= inicial) and (agora <= final):
        return True

    else:

        return False





verde = configColorizar('verde',autoPrint=True).colorizar
vermelho = configColorizar('vermelho',autoPrint=True).colorizar
azul = configColorizar('azul',autoPrint=True).colorizar


