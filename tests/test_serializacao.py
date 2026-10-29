import unittest
from src.modelos.leitor import Leitor

def test_serializacao_leitor():
    leitor = Leitor(1, "Ana Silva", "ana@email.com")

    dados = leitor.para_dicionario()
    leitor_recuperado = Leitor.de_dicionario(dados)

    assert isinstance(leitor_recuperado, Leitor)
    assert leitor_recuperado.idLeitor == leitor.idLeitor
    assert leitor_recuperado.nome == leitor.nome

    

