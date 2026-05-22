import subprocess
from datetime import datetime

from componentes.utilitarios import vermelho, verde, inTimeRange, azul, inDay


def executar(tarefa):
    """ Define os parâmetros e executa a função """

    inicio = datetime.now()
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




    fim = datetime.now()

    retorno = {
        'returncode': resultado.returncode,
        'stdout': resultado.stdout,
        'stderr': resultado.stderr,
        'inicio': inicio,
        'fim': fim,
        'sucesso': resultado.returncode == 0
    }



    if retorno['returncode'] == 1:
        vermelho(f"Erro na execução de {tarefa['id']}")
        vermelho(f"stderr {retorno['stderr']}")
        vermelho(f"returncode {retorno['returncode']}")

    else:
        verde(f"{tarefa['id']} Executado com sucesso {fim}")
        verde(f"returncode {retorno['returncode']}")
        print(retorno['stdout'])

    return





