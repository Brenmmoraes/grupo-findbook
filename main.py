
import json
from src.modelos import Leitor, Livro, Exemplar, Emprestimo


# Criar leitor
leitor = Leitor(1, "João", "joao@email.com")

# Criar livros
livro1 = Livro("9781234567890", "Harry Potter")
livro2 = Livro("9781234567891", "O Senhor dos Anéis")

# Criar exemplares
exemplar1 = Exemplar("E001", True, "Estante A", livro1)
exemplar2 = Exemplar("E002", False, "Estante B", livro2)

#empréstimos
emprestimo1 = Emprestimo(1, leitor, exemplar1)
emprestimo2 = Emprestimo(2, leitor, exemplar2)


# Disponibilidade dos livros
print("=== FIND BOOK ===")

print("\nLeitor:", leitor.nome)

print("\nLivro:", livro1.titulo)
print("Disponível para empréstimo:", emprestimo1.pode_realizar())

print("\nLivro:", livro2.titulo)
print("Disponível para empréstimo:", emprestimo2.pode_realizar())


# Serializar os leitores
print("\n=== SERIALIZAÇÃO DE LEITORES ===")

leitores = [
    Leitor(1, "Ana Silva", "ana@email.com"),
    Leitor(2, "João Santos", "joao@email.com")
]

dados = [leitor.para_dicionario() for leitor in leitores]

with open("leitores.json", "w", encoding="utf-8") as ficheiro:
    json.dump(dados, ficheiro, ensure_ascii=False, indent=4)

print("Leitores guardados em leitores.json")


# Desserializar os leitores
with open("leitores.json", "r", encoding="utf-8") as ficheiro:
    dados_lidos = json.load(ficheiro)

leitores_recuperados = [
    Leitor.de_dicionario(dados) for dados in dados_lidos
]

print("\nLeitores recuperados:")

for leitor in leitores_recuperados:
    print(leitor.idLeitor, "-", leitor.nome, "-", leitor.email)