"""Testes da API FindBook com bases SQLite temporárias e dados fictícios."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
from threading import Barrier
import unittest
from unittest.mock import patch

from app import create_app


class TestAPILeitores(unittest.TestCase):
    def setUp(self):
        self.pasta = TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.caminho = Path(self.pasta.name) / "dados" / "findbook.db"
        self.app = create_app({"TESTING": True, "DATABASE": self.caminho})
        self.cliente = self.app.test_client()
        self.leitor = {
            "idLeitor": 3,
            "nome": "Carla",
            "email": "carla@exemplo.pt",
        }

    def test_get_vazio_cria_pasta_e_tabela(self):
        resposta = self.cliente.get("/leitores")
        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(resposta.is_json)
        self.assertEqual(resposta.get_json(), [])
        self.assertTrue(self.caminho.is_file())
        with closing(sqlite3.connect(self.caminho)) as ligacao:
            self.assertEqual(
                ligacao.execute("SELECT COUNT(*) FROM leitores").fetchone()[0], 0
            )

    def test_post_devolve_201_e_get_le_a_mesma_base(self):
        resposta = self.cliente.post("/leitores", json=self.leitor)
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.get_json(), self.leitor)
        resposta_get = self.cliente.get("/leitores")
        self.assertEqual(resposta_get.status_code, 200)
        self.assertEqual(resposta_get.get_json(), [self.leitor])
        with closing(sqlite3.connect(self.caminho)) as ligacao:
            self.assertEqual(
                ligacao.execute("SELECT idLeitor, nome, email FROM leitores").fetchall(),
                [(3, "Carla", "carla@exemplo.pt")],
            )

    def test_listagem_converte_tuplos_e_ordena_por_id(self):
        outro = {"idLeitor": 1, "nome": "Ana", "email": "ana@exemplo.pt"}
        self.cliente.post("/leitores", json=self.leitor)
        self.cliente.post("/leitores", json=outro)
        self.assertEqual(self.cliente.get("/leitores").get_json(), [outro, self.leitor])

    def test_nome_e_normalizado_e_acentos_sao_preservados(self):
        dados = {"idLeitor": 5, "nome": "  João D'Ávila  ", "email": "joao@exemplo.pt"}
        esperado = {**dados, "nome": "João D'Ávila"}
        resposta = self.cliente.post("/leitores", json=dados)
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.get_json(), esperado)
        self.assertEqual(self.cliente.get("/leitores").get_json(), [esperado])

    def test_id_repetido_devolve_409_sem_substituir_dados(self):
        self.assertEqual(self.cliente.post("/leitores", json=self.leitor).status_code, 201)
        alterado = {**self.leitor, "nome": "Outro nome", "email": "outro@exemplo.pt"}
        resposta = self.cliente.post("/leitores", json=alterado)
        self.assertEqual(resposta.status_code, 409)
        self.assertTrue(resposta.is_json)
        self.assertEqual(self.cliente.get("/leitores").get_json(), [self.leitor])

    def test_campos_em_falta_sao_400_sem_inserir(self):
        for campo in self.leitor:
            with self.subTest(campo=campo):
                dados = {chave: valor for chave, valor in self.leitor.items() if chave != campo}
                resposta = self.cliente.post("/leitores", json=dados)
                self.assertEqual(resposta.status_code, 400)
                self.assertTrue(resposta.is_json)
        self.assertEqual(self.cliente.get("/leitores").get_json(), [])

    def test_ids_invalidos_sao_400_sem_inserir(self):
        for valor in (None, True, False, "3", 3.0, 0, -1, 2**63, [], {}):
            with self.subTest(idLeitor=valor):
                resposta = self.cliente.post("/leitores", json={**self.leitor, "idLeitor": valor})
                self.assertEqual(resposta.status_code, 400)
                self.assertTrue(resposta.is_json)
        self.assertEqual(self.cliente.get("/leitores").get_json(), [])

    def test_maior_id_sqlite_permitido(self):
        dados = {**self.leitor, "idLeitor": 2**63 - 1}
        resposta = self.cliente.post("/leitores", json=dados)
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(self.cliente.get("/leitores").get_json(), [dados])

    def test_nomes_invalidos_sao_400_sem_inserir(self):
        for valor in (None, "", "   ", 123, False, [], {}):
            with self.subTest(nome=valor):
                resposta = self.cliente.post("/leitores", json={**self.leitor, "nome": valor})
                self.assertEqual(resposta.status_code, 400)
                self.assertTrue(resposta.is_json)
        self.assertEqual(self.cliente.get("/leitores").get_json(), [])

    def test_emails_invalidos_sao_400_sem_inserir(self):
        for valor in (None, "", "   ", "sem-arroba.pt", "ana@", "@exemplo.pt", "ana@exemplo", "ana silva@exemplo.pt", 123, [], {}):
            with self.subTest(email=valor):
                resposta = self.cliente.post("/leitores", json={**self.leitor, "email": valor})
                self.assertEqual(resposta.status_code, 400)
                self.assertTrue(resposta.is_json)
        self.assertEqual(self.cliente.get("/leitores").get_json(), [])

    def test_corpo_json_tem_de_ser_objeto(self):
        for corpo in ("null", "[]", '"texto"', "123", "true", "{}", '{"idLeitor":'):
            with self.subTest(corpo=corpo):
                resposta = self.cliente.post("/leitores", data=corpo, content_type="application/json")
                self.assertEqual(resposta.status_code, 400)
                self.assertTrue(resposta.is_json)
        self.assertEqual(self.cliente.get("/leitores").get_json(), [])

    def test_pedido_sem_json_e_sem_corpo_sao_400(self):
        for argumentos in ({}, {"data": "texto", "content_type": "text/plain"}, {"data": "idLeitor=3&nome=Carla&email=carla@exemplo.pt"}):
            with self.subTest(argumentos=argumentos):
                resposta = self.cliente.post("/leitores", **argumentos)
                self.assertEqual(resposta.status_code, 400)
                self.assertTrue(resposta.is_json)

    def test_rotas_200_404_e_405(self):
        self.assertEqual(self.cliente.get("/").status_code, 200)
        inexistente = self.cliente.get("/nao-existe")
        self.assertEqual(inexistente.status_code, 404)
        self.assertTrue(inexistente.is_json)
        proibido = self.cliente.post("/")
        self.assertEqual(proibido.status_code, 405)
        self.assertTrue(proibido.is_json)
        self.assertIn("GET", proibido.headers.get("Allow", ""))
        self.assertEqual(self.cliente.delete("/leitores").status_code, 405)

    def test_registo_persiste_apos_recriar_aplicacao(self):
        self.cliente.post("/leitores", json=self.leitor)
        outra_app = create_app({"TESTING": True, "DATABASE": self.caminho})
        resposta = outra_app.test_client().get("/leitores")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json(), [self.leitor])

    def test_configuracoes_usam_bases_separadas(self):
        self.cliente.post("/leitores", json=self.leitor)
        caminho_outro = Path(self.pasta.name) / "outra" / "findbook.db"
        outra_app = create_app({"TESTING": True, "DATABASE": caminho_outro})
        self.assertEqual(outra_app.test_client().get("/leitores").get_json(), [])
        self.assertEqual(self.cliente.get("/leitores").get_json(), [self.leitor])

    def test_concorrencia_id_igual_cria_apenas_um_registo(self):
        inicio = Barrier(2)

        def inserir():
            with self.app.test_client() as cliente:
                inicio.wait(timeout=10)
                return cliente.post("/leitores", json=self.leitor).status_code

        with ThreadPoolExecutor(max_workers=2) as executor:
            pedidos = [executor.submit(inserir) for _ in range(2)]
            codigos = sorted(pedido.result(timeout=15) for pedido in pedidos)
        self.assertEqual(codigos, [201, 409])
        self.assertEqual(self.cliente.get("/leitores").get_json(), [self.leitor])

    def test_indisponibilidade_sqlite_na_consulta_e_tratada(self):
        with patch("app.listar_leitores", side_effect=sqlite3.OperationalError("database is locked")):
            resposta = self.cliente.get("/leitores")
        self.assertEqual(resposta.status_code, 503)
        self.assertTrue(resposta.is_json)
        self.assertNotIn("database is locked", resposta.get_data(as_text=True))

    def test_indisponibilidade_sqlite_na_insercao_e_tratada(self):
        with patch("app.adicionar_leitor", side_effect=sqlite3.OperationalError("database is locked")):
            resposta = self.cliente.post("/leitores", json=self.leitor)
        self.assertEqual(resposta.status_code, 503)
        self.assertTrue(resposta.is_json)
        self.assertEqual(self.cliente.get("/leitores").get_json(), [])


if __name__ == "__main__":
    unittest.main()
