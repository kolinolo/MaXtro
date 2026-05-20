import os, json
from datetime import datetime
from componentes.printTool import configColorizar
from componentes.Exceptions import NotJsonException


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

    if (agora > inicial) and (agora < final):
        return True


    else:
        print(f"{tarefa['id']} Fora do periodo de execução")
        return False




verde = configColorizar('verde',autoPrint=True).colorizar
vermelho = configColorizar('vermelho',autoPrint=True).colorizar


