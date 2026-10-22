

class Emprestimo:
    def __init__(self, idEmprestimo, leitor, exemplar):
        self.idEmprestimo = idEmprestimo
        self.leitor = leitor
        self.exemplar = exemplar

        self.idLeitor = leitor.idLeitor
        self.idExemplar = exemplar.idExemplar

        self.isbn = exemplar.livro.isbn if exemplar.livro else ""

        self.dataInicio = None
        self.dataDevolucaoPrevista = None
        self.dataDevolucaoEfetiva = None

    def pode_realizar(self):
        return self.exemplar.pode_emprestar()
