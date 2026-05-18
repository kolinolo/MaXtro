import subprocess
from datetime import datetime

def executarPython(tarefa):

    inicio = datetime.now()

    print(f'Executando {tarefa['id']}')
    resultado = subprocess.run(
        [tarefa['python_path'], tarefa['script']],

        cwd=tarefa['working_dir'],

        capture_output=True,
        text=True,

        encoding='utf-8'
    )

    fim = datetime.now()

    return {
        'returncode': resultado.returncode,
        'stdout': resultado.stdout,
        'stderr': resultado.stderr,
        'inicio': inicio,
        'fim': fim,
        'sucesso': resultado.returncode == 0
    }