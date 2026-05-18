import os, json

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

verde = configColorizar('verde',autoPrint=True).colorizar
vermelho = configColorizar('vermelho',autoPrint=True).colorizar