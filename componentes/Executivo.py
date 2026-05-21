import subprocess
from datetime import datetime

from componentes.utilitarios import vermelho, verde, inTimeRange, azul, inDay


def executar(tarefa):
    """ Define os parâmetros e executa a função """

    inicio = datetime.now()
    execInfo = []
    parametros = {}


    if not inTimeRange(tarefa) or not inDay(tarefa):
        azul(f'Tarefa fora do range de execução {tarefa["id"]}')
        return

    if tarefa['tipo'] == 'python':


        execInfo =[tarefa['python_path'],
         tarefa['script']]

        parametros = {

        'cwd' : tarefa['working_dir'],
        'capture_output' : True,
        'text' : True,
        'errors' : 'replace',
        'encoding' : 'utf-8'

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
        'encoding' : 'cp1252'
        }


    resultado = subprocess.run(execInfo,**parametros)

    print(f"Executando  {tarefa['id']} ({tarefa['tipo']})")


    fim = datetime.now()

    retorno = {
        'returncode': resultado.returncode,
        'stdout': resultado.stdout,
        'stderr': resultado.stderr,
        'inicio': inicio,
        'fim': fim,
        'sucesso': resultado.returncode == 0
    }

    if retorno['returncode'] != 0:
        vermelho(f"Erro na execução de {tarefa['id']}")

    else:
        verde(f"{tarefa['id']} Executado com sucesso {fim}")

        print(retorno['stdout'])

    return





