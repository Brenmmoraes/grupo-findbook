"""Testes de integração da persistência SQLite e da demonstração."""

from contextlib import closing
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest

from src.base_dados import adicionar_leitor, criar_tabela, listar_leitores
from src.modelos.leitor import Leitor


class TestBaseDados(unittest.TestCase):
    def setUp(self):
        self.pasta_temporaria = TemporaryDirectory()
        self.addCleanup(self.pasta_temporaria.cleanup)
        self.caminho = Path(self.pasta_temporaria.name) / "findbook.db"
        criar_tabela(self.caminho)

    def test_esquema_e_criacao_repetida_preservam_registos(self):
        adicionar_leitor(Leitor(1, "Ana", "ana@exemplo.pt"), self.caminho)

        criar_tabela(self.caminho)

        with closing(sqlite3.connect(self.caminho)) as ligacao:
            colunas = ligacao.execute("PRAGMA table_info(leitores)").fetchall()
        self.assertEqual(
            [(coluna[1], coluna[2], coluna[3], coluna[5]) for coluna in colunas],
            [("idLeitor", "INTEGER", 0, 1), ("nome", "TEXT", 1, 0),
             ("email", "TEXT", 0, 0)],
        )
        self.assertEqual(
            listar_leitores(self.caminho), [(1, "Ana", "ana@exemplo.pt")]
        )

    def test_tabela_vazia(self):
        self.assertEqual(listar_leitores(self.caminho), [])

    def test_dois_objetos_persistem_e_sao_listados_por_id(self):
        adicionar_leitor(Leitor(2, "Rui", "rui@exemplo.pt"), self.caminho)
        adicionar_leitor(Leitor(1, "Ana", "ana@exemplo.pt"), self.caminho)

        self.assertEqual(
            listar_leitores(self.caminho),
            [(1, "Ana", "ana@exemplo.pt"), (2, "Rui", "rui@exemplo.pt")],
        )
        # Uma nova ligação confirma que os INSERT foram confirmados no disco.
        with closing(sqlite3.connect(self.caminho)) as ligacao:
            quantidade = ligacao.execute("SELECT COUNT(*) FROM leitores").fetchone()[0]
        self.assertEqual(quantidade, 2)

    def test_aspas_e_sql_sao_guardados_como_texto(self):
        nome = "D'Ávila'); DROP TABLE leitores; --"
        email = "ana'@exemplo.pt"
        adicionar_leitor(Leitor(1, nome, email), self.caminho)
        adicionar_leitor(Leitor(2, "Rui"), self.caminho)

        self.assertEqual(
            listar_leitores(self.caminho), [(1, nome, email), (2, "Rui", "")]
        )

    def test_id_repetido_preserva_o_leitor_existente(self):
        adicionar_leitor(Leitor(1, "Ana", "ana@exemplo.pt"), self.caminho)

        adicionar_leitor(Leitor(1, "Outro nome", "outro@exemplo.pt"), self.caminho)

        self.assertEqual(
            listar_leitores(self.caminho), [(1, "Ana", "ana@exemplo.pt")]
        )

    def test_nome_nulo_e_rejeitado_sem_impedir_insercoes_seguintes(self):
        # A classe Leitor já valida o nome; este objeto testa a restrição da BD.
        objeto_invalido = SimpleNamespace(
            para_dicionario=lambda: {"idLeitor": 1, "nome": None, "email": ""}
        )
        with self.assertRaises(sqlite3.IntegrityError):
            adicionar_leitor(objeto_invalido, self.caminho)

        self.assertEqual(listar_leitores(self.caminho), [])
        adicionar_leitor(Leitor(1, "Ana"), self.caminho)
        self.assertEqual(listar_leitores(self.caminho), [(1, "Ana", "")])


class TestDemonstracaoSQLite(unittest.TestCase):
    def test_execucao_repetida_fora_do_projeto(self):
        origem = Path(__file__).resolve().parents[1]
        with TemporaryDirectory() as pasta_temporaria:
            raiz = Path(pasta_temporaria)
            projeto = raiz / "projeto"
            projeto.mkdir()
            shutil.copy2(origem / "demonstrar_sqlite.py", projeto)
            shutil.copytree(origem / "src", projeto / "src")
            pasta_externa = raiz / "outra_pasta"
            pasta_externa.mkdir()
            ambiente = os.environ.copy()
            ambiente["PYTHONUTF8"] = "1"
            ambiente["PYTHONDONTWRITEBYTECODE"] = "1"

            for _ in range(2):
                resultado = subprocess.run(
                    [sys.executable, "-B", str(projeto / "demonstrar_sqlite.py")],
                    cwd=pasta_externa,
                    env=ambiente,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    timeout=30,
                    check=True,
                )
                self.assertIn("1 - Ana - ana@exemplo.pt", resultado.stdout)
                self.assertIn("2 - Rui - rui@exemplo.pt", resultado.stdout)
                self.assertIn(
                    str((projeto / "dados" / "findbook.db").resolve()),
                    resultado.stdout,
                )

            self.assertFalse((pasta_externa / "dados").exists())
            self.assertEqual(
                listar_leitores(projeto / "dados" / "findbook.db"),
                [(1, "Ana", "ana@exemplo.pt"), (2, "Rui", "rui@exemplo.pt")],
            )


if __name__ == "__main__":
    unittest.main()
