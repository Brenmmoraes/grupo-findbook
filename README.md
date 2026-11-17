# FindBook

Projeto desenvolvido em Python para a gestão de empréstimos de livros de uma biblioteca.

## Elementos do grupo

- Formando A: Brenda
- Formando B: Joao
- Formando C: Bruno

## Atividade 1 - SQLite

A atividade reutiliza a classe `Leitor` e acrescenta persistência em SQLite,
sem alterar o `main.py` nem as classes originais. Não é necessário instalar
bibliotecas: `sqlite3`, `contextlib` e `pathlib` fazem parte do Python.

Na pasta do projeto, executar:

```console
python demonstrar_sqlite.py
```

O programa cria automaticamente `dados/findbook.db`, prepara a tabela `leitores`,
guarda os objetos `Leitor(1, "Ana", "ana@exemplo.pt")` e
`Leitor(2, "Rui", "rui@exemplo.pt")` e apresenta todos os registos no terminal:

```text
Leitores guardados:
1 - Ana - ana@exemplo.pt
2 - Rui - rui@exemplo.pt
```

Também apresenta o caminho absoluto da pasta e do ficheiro da base de dados.
Pode ser executado de outra pasta: a base de dados fica sempre na pasta `dados/`
do projeto. É possível repetir a execução: um `idLeitor` já existente mantém os
seus dados, sem duplicar registos nem apagar a base.

### Como funciona

O módulo `src/base_dados.py` disponibiliza três funções, com o parâmetro
`caminho` (por omissão, `"dados/findbook.db"`):

- `criar_tabela(caminho)`: usa `CREATE TABLE IF NOT EXISTS`.
- `adicionar_leitor(objeto, caminho)`: obtém os campos com `para_dicionario()` e
  executa um `INSERT INTO` com parâmetros `?`. O conflito de um ID já existente
  é ignorado com `ON CONFLICT(idLeitor) DO NOTHING`.
- `listar_leitores(caminho)`: usa `SELECT` e `fetchall()` e devolve tuplos
  `(idLeitor, nome, email)`, ordenados pelo ID.

As ligações são fechadas com `closing()` e as transações são geridas com
`with ligacao:`. Para outro caminho, a pasta que contém o ficheiro deve existir.

| Coluna | Definição SQL |
| --- | --- |
| idLeitor | INTEGER PRIMARY KEY |
| nome | TEXT NOT NULL |
| email | TEXT |

### Visualização e evidências no VS Code

1. Abrir a pasta do projeto no VS Code e executar a demonstração.
2. No Explorador, expandir `dados/` para mostrar `findbook.db`.
3. Instalar a extensão **SQLite Viewer**, de **qwtel**, caso ainda não exista.
4. Abrir `dados/findbook.db` e selecionar a tabela `leitores`. Se necessário,
   usar **Reopen Editor With... / SQLite Viewer**.
5. Confirmar os registos de Ana e Rui. Guardar capturas do terminal com a
   listagem e do VS Code com a pasta `dados/` e a tabela aberta.

Para apresentar o trabalho, mostrar também o código de `src/base_dados.py` e
`demonstrar_sqlite.py`. Se os IDs 1 e 2 já existirem, serão mostrados os dados
anteriormente guardados nesses IDs.

### Testes da integração SQLite

```console
python -m unittest discover -s tests -p test_base_dados.py -v
```

Os testes usam bases de dados temporárias e não modificam `dados/findbook.db`.
