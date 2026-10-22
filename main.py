
from src.modelos import Leitor, Livro, Exemplar, Emprestimo


leitor = Leitor(1, "João", "joao@email.com")

livro1 = Livro("9781234567890", "Harry Potter")
livro2 = Livro("9781234567891", "O Senhor dos Anéis")

exemplar1 = Exemplar("E001", True, "Estante A", livro1)
exemplar2 = Exemplar("E002", False, "Estante B", livro2)

emprestimo1 = Emprestimo(1, leitor, exemplar1)
emprestimo2 = Emprestimo(2, leitor, exemplar2)

print("Leitor:", leitor.nome)

print("\nLivro:", livro1.titulo)
print("Disponível para empréstimo:", emprestimo1.pode_realizar())

print("\nLivro:", livro2.titulo)
print("Disponível para empréstimo:", emprestimo2.pode_realizar())
