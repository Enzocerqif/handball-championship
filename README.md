# Sistema de Campeonatos de Handebol SQLite

Este projeto foi criado para testar e gerenciar dados relacionados a campeonatos de handebol utilizando SQLite como banco de dados e Python para execução e manipulação do esquema SQL. O código define as tabelas e as relações entre equipes, jogadores, estádios, partidas e campeonatos, além de inserir e consultar dados de exemplo.

## Funcionalidades

- Criação de tabelas para armazenar dados de campeonatos de handebol, incluindo equipes, jogadores, estádios, partidas e campeonatos.
- Inserção de dados fictícios para testar o esquema.
- Consultas simples utilizando SQLite para manipulação e visualização dos dados.
  
## Estrutura do Banco de Dados

O esquema SQL define as seguintes tabelas:

- `teams`: Armazena dados das equipes, incluindo nome, estádio, capitão e campeonato.
- `players`: Contém informações sobre os jogadores, incluindo nome, data de nascimento, gênero, altura e equipe.
- `stadiums`: Informações sobre os estádios onde as partidas acontecem.
- `matches`: Registra as partidas, incluindo data, times participantes, estádio e o resultado.
- `championships`: Armazena os campeonatos, com ano e descrição.

## Tecnologias Utilizadas

- **SQLite**: Banco de dados leve para armazenar e manipular dados.
- **Python**: Linguagem de programação usada para executar as operações no banco de dados.
