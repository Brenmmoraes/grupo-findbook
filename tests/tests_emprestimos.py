import unittest
# Importa a sua função do módulo src
from src.emprestimos import resumo_emprestimo

class TestProjeto(unittest.TestCase):

    def test_caso_valido(self):
        """Caso 1: Um caso completamente válido"""
        resultado = resumo_emprestimo("João", 10, "confirmado")
        self.assertEqual(resultado, ("João", True, True))

    def test_nome_com_espacos(self):
        """Caso 2: Um caso em que nome contém apenas espaços"""
        resultado = resumo_emprestimo("   ", 15, "pendente")
        self.assertEqual(resultado, ("Sem identificação", True, True))

    def test_dias_fora_do_intervalo(self):
        """Caso 3: Um caso com dias fora do intervalo válido"""
        resultado = resumo_emprestimo("Maria", 35, "confirmado")
        self.assertEqual(resultado, ("Maria", False, True))

    def test_estado_nao_aceite(self):
        """Caso 4: Um caso com estado não aceite"""
        resultado = resumo_emprestimo("Carlos", 20, "recusado")
        self.assertEqual(resultado, ("Carlos", True, False))

    def test_tipo_dias_invalido(self):
        """Caso Extra: Garante que valores booleanos ou None não contam como dias válidos"""
        resultado_bool = resumo_emprestimo("Ana", True, "confirmado")
        resultado_none = resumo_emprestimo("Ana", None, "confirmado")
        
        self.assertEqual(resultado_bool, ("Ana", False, True))
        self.assertEqual(resultado_none, ("Ana", False, True))

if __name__ == "__main__":
    unittest.main()
