class Exemplar:
    def __init__(self, idExemplar, ISBN, estado, localizacao="", livro=None):
        self.idExemplar = idExemplar
        self.ISBN = ISBN
        self.estado = estado
        self.localizacao = localizacao
        self.livro = livro

    def indicarEstado(self):
        return self.estado

    def pode_emprestar(self):
        return self.indicarEstado()

    def para_dicionario(self):
        return {
            "idExemplar": self.idExemplar,
            "ISBN": self.ISBN,
            }

@classmethod
def de_dicionario(cls, dados_exemplar):
    return cls(
        idExemplar=dados_exemplar["idExemplar"],
        ISBN=dados_exemplar["ISBN"],
        estado=dados_exemplar["estado"]
    )