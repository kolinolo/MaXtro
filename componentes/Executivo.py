import subprocess
from datetime import datetime

from componentes.utilitarios import vermelho, verde


def executarPython(tarefa):

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