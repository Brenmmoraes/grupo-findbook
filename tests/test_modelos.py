
import unittest
from src.modelos import Leitor, Livro, Exemplar, Emprestimo


class TestEmprestimo(unittest.TestCase):

    def test_exemplar_disponivel(self):
        leitor = Leitor(1, "João")
        livro = Livro("9781234567890", "Harry Potter")
        exemplar = Exemplar(
            idExemplar="E001", ISBN=livro.isbn, estado=True,
            localizacao="Estante A", livro=livro,
        )
        emprestimo = Emprestimo(1, leitor, exemplar)

        self.assertIs(emprestimo.pode_realizar(), True)

    def test_exemplar_indisponivel(self):
        leitor = Leitor(1, "João")
        livro = Livro("9781234567891", "O Senhor dos Anéis")
        exemplar = Exemplar(
            idExemplar="E002", ISBN=livro.isbn, estado=False,
            localizacao="Estante B", livro=livro,
        )
        emprestimo = Emprestimo(2, leitor, exemplar)

        self.assertIs(emprestimo.pode_realizar(), False)


if __name__ == "__main__":
    unittest.main()
