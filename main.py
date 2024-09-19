import sqlite3
import random
import sys
import io

# Redirecionar a saída padrão para aceitar UTF-8
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Conexão com o banco de dados em memória
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Esquema SQL
schema = """
CREATE TABLE teams (
  id_team INTEGER PRIMARY KEY NOT NULL,
  team_name TEXT CHECK (length(team_name) <= 50) NOT NULL,
  id_home_stadium INTEGER NOT NULL,
  id_captain INTEGER NOT NULL,
  id_championship INTEGER NOT NULL
);

CREATE TABLE players (
  id_player INTEGER PRIMARY KEY NOT NULL,
  player_name TEXT CHECK (length(player_name) <= 50) NOT NULL,
  date_of_birth DATE NOT NULL,
  gender TEXT CHECK(gender IN ('M', 'F')) NOT NULL,
  height REAL CHECK(height <= 999) NOT NULL,
  id_team INTEGER NOT NULL,
  FOREIGN KEY (id_team) REFERENCES teams(id_team)
);

CREATE TABLE stadiums (
  id_stadium INTEGER PRIMARY KEY NOT NULL,
  stadium_name TEXT CHECK (length(stadium_name) <= 50) NOT NULL,
  address TEXT CHECK (length(address) <= 100) NOT NULL
);

CREATE TABLE matches (
  id_match INTEGER PRIMARY KEY NOT NULL,
  match_date DATE NOT NULL,
  id_stadium INTEGER NOT NULL,
  id_home_team INTEGER NOT NULL,
  id_away_team INTEGER NOT NULL,
  home_goals INTEGER CHECK(home_goals <= 50),
  away_goals INTEGER CHECK(away_goals <= 50),
  id_championship INTEGER NOT NULL
);

CREATE TABLE championships (
  id_championship INTEGER PRIMARY KEY NOT NULL,
  year INTEGER CHECK(year >= 1000 AND year <= 9999) NOT NULL,
  description TEXT CHECK (length(description) <= 100)
);
"""

# Executa o esquema SQL
cursor.executescript(schema)

# Inserir dados do campeonato
cursor.execute("INSERT INTO championships (id_championship, year, description) VALUES (1, 2024, 'Campeonato de Handebol')")
championship_id = 1

# Inserir dados dos estádios
cursor.execute("INSERT INTO stadiums (id_stadium, stadium_name, address) VALUES (1, 'Estádio Nacional', 'Rua 123, Cidade XYZ')")
stadium_id = 1

# Inserir dados dos times
teams = [
    (1, 'Time A', stadium_id, 1, championship_id),
    (2, 'Time B', stadium_id, 2, championship_id),
    (3, 'Time C', stadium_id, 3, championship_id),
    (4, 'Time D', stadium_id, 4, championship_id)
]

cursor.executemany("INSERT INTO teams (id_team, team_name, id_home_stadium, id_captain, id_championship) VALUES (?, ?, ?, ?, ?)", teams)

# Inserir dados dos jogadores
players = [
    # Jogadores do Time A
    (1, 'Neymar Júnior', '1992-02-05', 'M', 175, 1),
    (2, 'Cristiano Ronaldo', '1985-02-05', 'M', 187, 1),
    (3, 'Lionel Messi', '1987-06-24', 'M', 170, 1),
    (4, 'Vinícius Júnior', '2000-07-12', 'M', 176, 1),
    
    # Jogadores do Time B
    (5, 'Marta Vieira', '1986-02-19', 'F', 170, 2),
    (6, 'Formiga', '1978-03-03', 'F', 165, 2),
    (7, 'Alex Morgan', '1989-07-02', 'F', 170, 2),
    (8, 'Debinha', '1990-05-05', 'F', 165, 2),
    
    # Jogadores do Time C
    (9, 'Kaká', '1982-04-22', 'M', 186, 3),
    (10, 'Ronaldinho Gaúcho', '1980-03-21', 'M', 180, 3),
    (11, 'Ronaldo Fenômeno', '1976-09-18', 'M', 183, 3),
    (12, 'Romario', '1966-01-29', 'M', 170, 3),
    
    # Jogadores do Time D 
    (13, 'Michael Jordan', '1963-02-17', 'M', 198, 4),
    (14, 'LeBron James', '1984-12-30', 'M', 206, 4),
    (15, 'Stephen Curry', '1988-03-14', 'M', 191, 4),
    (16, 'Kevin Durant', '1988-09-29', 'M', 206, 4)
]

cursor.executemany("INSERT INTO players (id_player, player_name, date_of_birth, gender, height, id_team) VALUES (?, ?, ?, ?, ?, ?)", players)

# Inserir dados das partidas
matches = [
    (1, '2024-05-01', stadium_id, 1, 2, None, None, championship_id),  # Partida entre Time A e Time B
    (2, '2024-05-02', stadium_id, 3, 4, None, None, championship_id)   # Partida entre Time C e Time D
]

cursor.executemany("INSERT INTO matches (id_match, match_date, id_stadium, id_home_team, id_away_team, home_goals, away_goals, id_championship) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", matches)

# Simulação de resultados das partidas
for match_id in range(1, 3):
    home_goals = random.randint(0, 5)  # Gols do time da casa
    away_goals = random.randint(0, 5)  # Gols do time visitante
    cursor.execute("UPDATE matches SET home_goals = ?, away_goals = ? WHERE id_match = ?", (home_goals, away_goals, match_id))

# Consultar e mostrar os resultados das partidas
cursor.execute("""
SELECT m.id_match, m.match_date, t1.team_name AS home_team, t2.team_name AS away_team, s.stadium_name, m.home_goals, m.away_goals
FROM matches m
JOIN teams t1 ON m.id_home_team = t1.id_team
JOIN teams t2 ON m.id_away_team = t2.id_team
JOIN stadiums s ON m.id_stadium = s.id_stadium
WHERE m.id_championship = ?
""", (championship_id,))

print("\nResultados das Partidas:")
for row in cursor.fetchall():
    print(f"Partida {row[0]} - Data: {row[1]} - Estádio: {row[4]} - Resultado: ({row[2]}) {row[5]} x {row[6]} ({row[3]})")

# Consultar e mostrar as informações dos jogadores
cursor.execute("""
SELECT p.player_name, p.date_of_birth, p.gender, p.height, t.team_name
FROM players p
JOIN teams t ON p.id_team = t.id_team
""")

print("\nInformações dos Jogadores:")
for row in cursor.fetchall():
    print(f"Nome: {row[0]}, Data de Nascimento: {row[1]}, Gênero: {row[2]}, Altura: {row[3]} cm, Time: {row[4]}\n")

# Fecha a conexão
conn.close()
