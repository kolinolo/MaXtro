from componentes.GerenciadorTarefas import montarTarefas
from componentes.Executivo import executarPython




tarefas  =  montarTarefas()



for tarefa in tarefas:

    resultado = None

    match(tarefa['tipo']):

        case('python'):

            resultado = executarPython(tarefa)

    print(resultado)





