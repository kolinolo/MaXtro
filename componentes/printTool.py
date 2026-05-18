def deColorLen(texto):
    if texto[0] == '\x1b':
        texto = texto[5:-5]

    return len(texto)




class configCentralizar:

    def __init__(self, MX: int, borda: str):
        self.MX = MX
        self.borda = borda

    def centralizar(self, texto: str, ):
        tamanhoTexto = deColorLen(texto)
        fix = 0
        if tamanhoTexto % 2 != 0: fix = 1

        espacos = int((self.MX - tamanhoTexto) / 2)
        if len(self.borda) > 1:
            print(f"{(self.borda * espacos)[:espacos]} {texto} {(self.borda * espacos)[espacos - fix:]}")

        else:
            print(f"{self.borda * espacos} {texto} {self.borda * (espacos + fix)}")


class configColorizar:
    def __init__(self, cor: str, autoPrint: bool = False):
        if cor not in ['rosa', 'azul', 'verde', 'amarelo', 'vermelho', 'clear']:
            raise CorInexistente

        self.cor = cor
        self.autoPrint = autoPrint

    def colorizar(self, texto):
        cores = {'rosa': '\033[95m', 'azul': '\033[94m', 'verde': '\033[92m', 'amarelo': '\033[93m',
                 'vermelho': '\033[91m',
                 'clear': '\033[0m', }

        if self.cor not in cores:
            raise CorInexistente(f"Cor {self.cor} invalida")

        if self.autoPrint:
            print(f"{cores[self.cor]}{texto}{cores["clear"]}")

        else:
            return f"{cores[self.cor]}{texto}{cores["clear"]}"


class CorInexistente(Exception):
    pass

