
import unittest
from src.modelos import Leitor, Livro, Exemplar, Emprestimo


class TestEmprestimo(unittest.TestCase):

    def test_exemplar_disponivel(self):
        leitor = Leitor(1, "João")
        livro = Livro("9781234567890", "Harry Potter")
        exemplar = Exemplar("E001", True, "Estante A", livro)
        emprestimo = Emprestimo(1, leitor, exemplar)

        self.assertTrue(emprestimo.pode_realizar())

    def test_exemplar_indisponivel(self):
        leitor = Leitor(1, "João")
        livro = Livro("9781234567891", "O Senhor dos Anéis")
        exemplar = Exemplar("E002", False, "Estante B", livro)
        emprestimo = Emprestimo(2, leitor, exemplar)

        self.assertFalse(emprestimo.pode_realizar())


if __name__ == "__main__":
    unittest.main()
