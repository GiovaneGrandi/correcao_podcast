import sqlite3
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Adiciona o caminho da raiz do projeto ao sys.path
from config import *

# Conecta ao banco de dados (o arquivo .db será criado se não existir)
conn = sqlite3.connect(DB_IATITUS)
cursor = conn.cursor()

querysCriacaoBD = [
    '''CREATE TABLE IF NOT EXISTS TBContexto (
        PkIdCon INTEGER PRIMARY KEY AUTOINCREMENT,
        FkIdCad INTEGER NOT NULL,
        TituloCon TEXT,
        FOREIGN KEY (FkIdCad) REFERENCES TBCadeira (PkIdCad)
    )''',
    '''CREATE TABLE IF NOT EXISTS TBCadeira (
        PkIdCad INTEGER PRIMARY KEY AUTOINCREMENT,
        NomeCad TEXT
    )''',
    '''CREATE TABLE IF NOT EXISTS TBCadAlu (
        PkIdCA INTEGER PRIMARY KEY AUTOINCREMENT,
        FkIdCad INTEGER NOT NULL,
        FkIdAlu INTEGER NOT NULL,
        FOREIGN KEY (FkIdCad) REFERENCES TBCadeira (PkIdCad),
        FOREIGN KEY (FkIdAlu) REFERENCES TBAluno (PkIdAlu)
    )''',
    '''CREATE TABLE IF NOT EXISTS TBAluno (
        PkIdAlu INTEGER PRIMARY KEY AUTOINCREMENT,
        NomeCad TEXT
    )''',
    '''CREATE TABLE IF NOT EXISTS TBArqCon (
        PkIdAC INTEGER PRIMARY KEY AUTOINCREMENT,
        FkIdCon INTEGER NOT NULL,
        FkIdArq INTEGER NOT NULL,
        FOREIGN KEY (FkIdCon) REFERENCES TBContexto (PkIdCon),
        FOREIGN KEY (FkIdArq) REFERENCES TBArquivo (PkIdArq)
    )''',
    '''CREATE TABLE IF NOT EXISTS TBArquivo (
        PkIdArq INTEGER PRIMARY KEY AUTOINCREMENT,
        FkIdCad INTEGER NOT NULL,
        TituloArq TEXT,
        ConteudoArq BLOB,
        FlgResumoArq INTEGER CHECK (FlgResumoArq >= 0 AND FlgResumoArq <= 1),
        FOREIGN KEY (FkIdCad) REFERENCES TBCadeira (PkIdCad)
    )''',
]

querysAlimentacaoBD = [
    '''INSERT INTO TBCadeira (NomeCad) VALUES ('Gestão de Projetos')''',
    '''INSERT INTO TBCadeira (NomeCad) VALUES ('Big Data')''',
    '''INSERT INTO TBCadeira (NomeCad) VALUES ('IA e Machine Learning')''',
]

# Ativa a verificação de chaves estrangeiras
cursor.execute('PRAGMA foreign_keys = ON;')

# Cria as tabelas
for query in querysCriacaoBD:
    try:
        cursor.execute(query)
    except sqlite3.OperationalError as e:
        print(f"Erro ao executar a query: {query}")
        print(f"Erro: {e}")

# Salva as mudanças e fecha a conexão
conn.commit()
conn.close()

print("Banco de dados e tabelas criados com sucesso!")
