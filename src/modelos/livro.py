
class Livro:
    def __init__(self, isbn, titulo, autor="", genero="", edicao="", ano=0):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.edicao = edicao
        self.ano = ano
        self.exemplaresDisponiveis = 0
