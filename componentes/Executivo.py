import subprocess
from datetime import datetime, timezone
from componentes.utilitarios import vermelho, verde, inTimeRange, azul, inDay, diretorio
import DbLabs
from zoneinfo import ZoneInfo
import os

bp = DbLabs.buscaPostgres()

tz = ZoneInfo('America/Sao_Paulo')

def newLog(retorno):

    tarefa = retorno['tarefa']


    os.makedirs(diretorio(f"/Logs/{tarefa['id']}"), exist_ok=True)

    caminho = diretorio(f"/Logs/{tarefa['id']}/{retorno['logID']}.txt")

    with open(caminho, "x") as file:

        fileText = f"""
{tarefa['id']}
{retorno['inicio']}
{retorno['fim']}
==============================
\n
{retorno['stdout']}
        """

        file.write(fileText)




def executar(tarefa):
    """ Define os parâmetros e executa a função """

    inicio = datetime.now(tz)
    execInfo = []
    parametros = {}


    if not inTimeRange(tarefa) or not inDay(tarefa):
        azul(f'skip {tarefa["id"]}')
        return

    if tarefa['tipo'] == 'python':


        execInfo =[tarefa['python_path'],
         tarefa['script']]

        parametros = {

        'cwd' : tarefa['working_dir'],
        'capture_output' : True,
        'text' : True,
        'errors' : 'replace',
        'encoding' : 'UTF-8',


        }

    elif tarefa['tipo'] == 'powershell':

        execInfo =[

            "powershell",
            "-ExecutionPolicy", "Bypass",
            "-File", tarefa['script']
        ]


        parametros = {
        'cwd' : tarefa['working_dir'],
        'capture_output' : True,
        'text' : True,
        'encoding' : 'UTF-8',

        }

    print(f"Executando  {tarefa['id']} ({tarefa['tipo']})")
    resultado = subprocess.run(execInfo,**parametros)




    fim = datetime.now(tz)

    retorno = {
        'returncode': resultado.returncode,
        'stdout': resultado.stdout,
        'stderr': resultado.stderr,
        'inicio': inicio.replace(microsecond=0),
        'fim': fim.replace(microsecond=0),
        'sucesso': resultado.returncode == 0,
        'tarefa': tarefa,
        'logID': inicio.strftime('%Y-%m-%d %H%M')
    }



    if retorno['returncode'] == 1:
        vermelho(f"Erro na execução de {tarefa['id']}")
        vermelho(f"stderr {retorno['stderr']}")
        vermelho(f"returncode {retorno['returncode']}")

    else:
        verde(f"{tarefa['id']} Executado com sucesso {fim}")
        verde(f"returncode {retorno['returncode']}")
        print(retorno['stdout'])


    try:

        sql = f""" insert into mx_exec values (
            
                            {bp.lastID('mx_exec') + 1},
                            '{tarefa['id']}',
                           '{tarefa['tipo']}',
                            {retorno['returncode']},
                            {retorno['stderr'] if retorno['stderr'] != "" else 0},
                            {retorno['sucesso']},
                            '{retorno['inicio']}',
                            '{retorno['fim']}',
                            '{retorno['logID']}',
                            '{retorno['fim']}'
                            );
"""

        bp.executaComando(sql)
        newLog(retorno)



    except Exception as e:

        print(f"exceção ao logar {e}")



    return





