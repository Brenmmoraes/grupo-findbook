"""Persistência dos leitores do FindBook numa base de dados SQLite."""

import sqlite3
from contextlib import closing


def criar_tabela(caminho="dados/findbook.db"):
    """Cria a tabela de leitores, caso ainda não exista."""
    with closing(sqlite3.connect(caminho)) as ligacao:
        with ligacao:
            ligacao.execute(
                """
                CREATE TABLE IF NOT EXISTS leitores (
                    idLeitor INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    email TEXT
                )
                """
            )


def adicionar_leitor(objeto, caminho="dados/findbook.db"):
    """Guarda um Leitor e devolve True se criou um registo, False se o ID existe."""
    dados = objeto.para_dicionario()
    with closing(sqlite3.connect(caminho)) as ligacao:
        with ligacao:
            cursor = ligacao.execute(
                """
                INSERT INTO leitores (idLeitor, nome, email)
                VALUES (?, ?, ?)
                ON CONFLICT(idLeitor) DO NOTHING
                """,
                (dados["idLeitor"], dados["nome"], dados["email"]),
            )
            return cursor.rowcount == 1


def listar_leitores(caminho="dados/findbook.db"):
    """Devolve todos os leitores como tuplos, ordenados por ID."""
    with closing(sqlite3.connect(caminho)) as ligacao:
        with ligacao:
            cursor = ligacao.execute(
                "SELECT idLeitor, nome, email FROM leitores ORDER BY idLeitor"
            )
            return cursor.fetchall()
