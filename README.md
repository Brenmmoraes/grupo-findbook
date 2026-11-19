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

## Atividade 2 - API Flask

A API disponibiliza os leitores através de pedidos HTTP e reutiliza a classe
`Leitor` e as funções SQLite da Atividade 1. O ponto de entrada é `app.py`;
`main.py` e `demonstrar_sqlite.py` continuam disponíveis.

### Preparar o ambiente

Abrir a raiz do projeto no VS Code e escolher um terminal **Git Bash**.
Executar um comando de cada vez. Se a pasta `.venv/` ainda não existir, criar:

```bash
python -m venv .venv
```

Ativar o ambiente e verificar se Flask já está instalado:

```bash
source .venv/Scripts/activate
```

```bash
python -m pip show flask
```

Se o comando anterior indicar que Flask não foi encontrado, instalar as
dependências do projeto:

```bash
python -m pip install -r requirements.txt
```

O módulo `sqlite3` faz parte do Python e não precisa de instalação.
Para incluir os leitores fictícios Ana e Rui, executar uma vez:

```bash
python demonstrar_sqlite.py
```

Iniciar o servidor e manter este terminal aberto:

```bash
python -m flask --app app:app run --debug
```

A API fica em `http://127.0.0.1:5000`. A opção `--debug` destina-se apenas
ao desenvolvimento local. Para parar, usar `Ctrl+C` no terminal.

### Pedidos e respostas

| Pedido | Resposta esperada |
| --- | --- |
| `GET /` | `200`, informação da API |
| `GET /leitores` | `200`, lista JSON dos leitores, ou `[]` se estiver vazia |
| `POST /leitores` com um novo ID e dados válidos | `201`, leitor criado |
| `POST /leitores` com um ID já existente | `409`, conflito sem alterar o leitor |
| `POST /leitores` com dados inválidos | `400`, mensagem de erro em JSON |
| `GET /nao-existe` | `404`, rota inexistente |
| `POST /` | `405`, método não permitido |

Em `POST /leitores`, escolher **Body → JSON** e enviar os três campos:

```json
{
  "idLeitor": 3,
  "nome": "Carla",
  "email": "carla@exemplo.pt"
}
```

O cabeçalho é `Content-Type: application/json`. O ID tem de ser um inteiro
positivo dentro do intervalo do SQLite; valores booleanos não são IDs válidos.
O nome tem de ser texto não vazio. O email é obrigatório e passa por uma
validação simples do formato. Espaços no início e no fim do nome e do email
são removidos. JSON malformado, um corpo que não seja um objeto, campos em
falta e tipos incorretos recebem `400`.

Exemplo que deve receber `400`, sem inserir um registo:

```json
{
  "idLeitor": 4,
  "nome": "",
  "email": "sem_nome@exemplo.pt"
}
```

### Testar no Bruno

1. No Bruno, escolher **Open Collection** e abrir a pasta `bruno/` deste
   projeto, onde está `bruno.json`.
2. Selecionar o ambiente **Local**. A variável `baseUrl` aponta para
   `http://127.0.0.1:5000`. As variáveis `nomeLeitor` e `emailLeitor`
   definem o leitor a criar; podem ser alteradas para outros dados fictícios.
3. Com o servidor em execução, enviar os pedidos pela ordem numérica:
   consultar, criar o leitor, confirmar a listagem, repetir o ID, enviar nome
   vazio, visitar uma rota inexistente e enviar POST para a raiz.
4. Confirmar o JSON, o código HTTP e os resultados na área **Tests** de cada
   resposta. A coleção inclui testes para os códigos `200`, `201`, `409`,
   `400`, `404` e `405`.

Para demonstrar, executar a coleção completa no **Runner**, por ordem e sem
ativar a execução em paralelo. O pedido 01 consulta os leitores e escolhe
automaticamente um ID livre numa variável temporária. O pedido 02 usa esse ID
para obter `201`; o pedido 04 repete-o para obter `409`. **Run Again** escolhe
outro ID livre e mantém os registos anteriores.

Para criar outra pessoa, abrir **Environments → Local**, alterar `nomeLeitor`
e `emailLeitor`, guardar e executar novamente a coleção completa. Exemplos:
Mariana com `mariana@exemplo.pt`, ou Pedro com `pedro@exemplo.pt`.

Se forem enviados pedidos individualmente, executar 01 antes de 02. Depois
da criação, executar 03 para confirmar e 04 para mostrar o conflito. Repetir
apenas 02 com o mesmo ID continua a devolver `409`, como é esperado.

### Confirmar no SQLite Viewer e recolher evidências

Depois do POST com `201`, voltar ao VS Code e abrir `dados/findbook.db` com
SQLite Viewer. Atualizar a visualização e selecionar `leitores`. Confirmar
o ID, o nome e o email recebidos na resposta, juntamente com os leitores
anteriores. A API e `demonstrar_sqlite.py` usam o mesmo ficheiro dentro da
pasta do projeto, mesmo quando são iniciados a partir de outra localização.

Guardar capturas de `app.py`, das respostas GET `200`, POST `201` e erro `400`,
da tabela no SQLite Viewer e de `requirements.txt` e `.gitignore`.
Acrescentar a resposta `409` para mostrar o tratamento de IDs repetidos.

### Testes automáticos

Na raiz do projeto, com o ambiente ativo:

```bash
python -m unittest discover -s tests -v
```

Os testes da API usam bases temporárias. Os pedidos enviados no Bruno usam a
base real do projeto e mantêm os leitores criados entre execuções.

### Explicação oral

“Acrescentei `app.py` ao FindBook e reutilizei a classe `Leitor` e o módulo
SQLite. O GET consulta os tuplos da base e transforma cada um num dicionário
com `idLeitor`, `nome` e `email`. O POST lê e valida o JSON, cria um único
objeto `Leitor` e chama a inserção. A inserção indica se criou uma linha:
respondo `201` quando criou e `409` quando o ID já existia. Os dados inválidos
recebem `400`. A informação fica guardada em `dados/findbook.db` e posso
confirmá-la no GET e no SQLite Viewer.”

### Preparar a entrega no GitHub

Incluir `app.py`, o código em `src/`, os demonstradores, os testes, a coleção
`bruno/`, este README, `.gitignore` e `requirements.txt`. O ficheiro de
dependências corresponde ao ambiente usado para testar a atividade. Se forem
alteradas as dependências, atualizar a partir do ambiente virtual ativo:

```bash
python -m pip freeze > requirements.txt
```

Não incluir `.venv/`, caches, ficheiros `.env` com segredos ou bases com dados
pessoais. O `.gitignore` exclui os ficheiros SQLite; a base pode ser recriada
com `python demonstrar_sqlite.py` e os exemplos usam apenas dados fictícios.
Antes de publicar, verificar os ficheiros selecionados no controlo de versões.

Referências: [API oficial do Flask](https://flask.palletsprojects.com/en/stable/api/),
[testes com Flask](https://flask.palletsprojects.com/en/stable/testing/) e
[guia oficial do Bruno](https://docs.usebruno.com/introduction/quick-start).
