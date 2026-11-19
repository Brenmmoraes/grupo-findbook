"""API Flask dos leitores do FindBook, com persistência SQLite."""

from pathlib import Path
import re
import sqlite3

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from src.base_dados import adicionar_leitor, criar_tabela, listar_leitores
from src.modelos.leitor import Leitor


def validar_leitor(dados):
    """Valida o pedido antes de construir o modelo já existente."""
    if not isinstance(dados, dict):
        raise ValueError("Envia um objeto JSON com idLeitor, nome e email.")

    if not all(campo in dados for campo in ("idLeitor", "nome", "email")):
        raise ValueError("Os campos idLeitor, nome e email são obrigatórios.")

    id_leitor = dados["idLeitor"]
    # bool é uma subclasse de int em Python, mas não é um ID válido.
    if type(id_leitor) is not int or not 1 <= id_leitor <= 2**63 - 1:
        raise ValueError("idLeitor deve ser um inteiro positivo até 9223372036854775807.")

    nome = dados["nome"]
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("O nome do leitor não pode estar vazio.")

    email = dados["email"]
    if not isinstance(email, str) or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()):
        raise ValueError("Indica um email válido, por exemplo carla@exemplo.pt.")

    return Leitor(id_leitor, nome.strip(), email.strip())


def create_app(config=None):
    """Cria a aplicação; os testes podem indicar uma base de dados temporária."""
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.config["DATABASE"] = Path(__file__).resolve().parent / "dados" / "findbook.db"
    if config:
        app.config.update(config)

    caminho = Path(app.config["DATABASE"]).resolve()
    caminho.parent.mkdir(parents=True, exist_ok=True)
    app.config["DATABASE"] = caminho
    criar_tabela(caminho)

    @app.get("/")
    def inicio():
        return jsonify({"aplicacao": "FindBook", "rotas": ["GET /leitores", "POST /leitores"]})

    @app.get("/leitores")
    def consultar_leitores():
        # A função SQLite devolve tuplos, não instâncias de Leitor.
        registos = listar_leitores(app.config["DATABASE"])
        return jsonify([
            {"idLeitor": id_leitor, "nome": nome, "email": email}
            for id_leitor, nome, email in registos
        ]), 200

    @app.post("/leitores")
    def criar_leitor():
        # silent=True permite responder 400 também a JSON malformado ou ausente.
        dados = request.get_json(silent=True)
        try:
            leitor = validar_leitor(dados)
        except ValueError as erro:
            return jsonify({"erro": str(erro)}), 400

        criado = adicionar_leitor(leitor, app.config["DATABASE"])
        if not criado:
            return jsonify({"erro": "Já existe um leitor com este idLeitor."}), 409
        return jsonify(leitor.para_dicionario()), 201

    @app.errorhandler(sqlite3.OperationalError)
    def base_indisponivel(erro):
        app.logger.warning("Não foi possível aceder à base de dados: %s", erro)
        return jsonify({"erro": "Base de dados temporariamente indisponível. Tenta novamente."}), 503

    @app.errorhandler(HTTPException)
    def erro_http(erro):
        # Preserva cabeçalhos HTTP, incluindo Allow no erro 405.
        resposta = erro.get_response()
        mensagens = {
            404: "Rota não encontrada.",
            405: "Método HTTP não permitido nesta rota.",
        }
        resposta.data = app.json.dumps({"erro": mensagens.get(erro.code, erro.description)})
        resposta.content_type = "application/json"
        return resposta

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
