"""Demonstra a gravação e consulta de objetos Leitor com SQLite."""

from pathlib import Path

from src.base_dados import adicionar_leitor, criar_tabela, listar_leitores
from src.modelos.leitor import Leitor


def main():
    # Usa a pasta do projeto, mesmo quando executado de outra localização.
    pasta_dados = Path(__file__).resolve().parent / "dados"
    pasta_dados.mkdir(exist_ok=True)
    caminho = pasta_dados / "findbook.db"

    criar_tabela(caminho)

    leitores = [
        Leitor(1, "Ana", "ana@exemplo.pt"),
        Leitor(2, "Rui", "rui@exemplo.pt"),
    ]
    for leitor in leitores:
        adicionar_leitor(leitor, caminho)

    print("=== FIND BOOK - SQLITE ===")
    print(f"Pasta da base de dados: {pasta_dados}")
    print(f"Ficheiro da base de dados: {caminho}")
    print("\nLeitores guardados:")
    for id_leitor, nome, email in listar_leitores(caminho):
        print(f"{id_leitor} - {nome} - {email}")


if __name__ == "__main__":
    main()
