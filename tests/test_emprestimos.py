import unittest

def pode_agendar_sessao(data_no_periodo, existe_conflito): 
    return not existe_conflito

class TesteAgendamento(unittest.TestCase): 

    def teste_rejeitar_sessao_com_conflito(self):

        self.assertFalse(
            pode_agendar_sessao(data_no_periodo = True, existe_conflito = True)
        )

    def teste_aceita_sessao_sem_conflito(self):
        self.assertTrue(
            pode
        )