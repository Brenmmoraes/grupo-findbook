class Exemplar:
    def __init__(self, idExemplar, estado, localizacao="", livro=None):
        self.idExemplar = idExemplar
        self.estado = estado
        self.localizacao = localizacao
        self.livro = livro

    def indicarEstado(self):
        return self.estado

    def pode_emprestar(self):
        return self.indicarEstado()
