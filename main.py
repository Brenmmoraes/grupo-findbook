
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

leitor1 = Leitor(1, "Ana Silva", "ana@email.com")

dados = leitor1.para_dicionario()
print(dados)

leitor2 = Leitor.de_dicionario(dados)
print(leitor2.nome)

leitores = [
    Leitor(1, "Ana Silva", "ana@email.com"),
    Leitor(2, "João Santos", "joao@email.com")
]

dados = [leitor.para_dicionario() for leitor in leitores]

with open("leitores.json", "w", encoding="utf-8") as ficheiro:
    json.dump(dados, ficheiro, ensure_ascii=False, indent=4)

with open("leitores.json", "r", encoding="utf-8") as ficheiro:
    dados_lidos = json.load(ficheiro)

leitores_recuperados = [
    Leitor.de_dicionario(dados) for dados in dados_lidos
]

for leitor in leitores_recuperados:
    print(leitor.nome)
