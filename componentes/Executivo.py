import subprocess
from datetime import datetime

from componentes.utilitarios import vermelho, verde, inTimeRange


def executarPython(tarefa):

    if not inTimeRange(tarefa):
        print(f'Tarefa fora do range de execução {tarefa["id"]}')

        return

    inicio = datetime.now()

    print(f'Executando {tarefa['id']}')
    resultado = subprocess.run(
        [tarefa['python_path'], tarefa['script']],

        cwd=tarefa['working_dir'],

        capture_output=True,
        text=True,
        errors='replace',
        encoding='utf-8'
    )

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

    return



def executaPowerShell(tarefa):

    if not inTimeRange(tarefa):
        print(f'Tarefa fora do range de execução {tarefa["id"]}')

        return

    inicio = datetime.now()

    print(f"Executando  {tarefa['id']} ({tarefa['tipo']})")

    resultado = subprocess.run(

        [
            "powershell",
            "-ExecutionPolicy", "Bypass",
            "-File", tarefa['script']
        ],

        cwd=tarefa['working_dir'],
        capture_output=True,
        text=True,
        encoding='cp1252'

    )

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