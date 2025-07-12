import sqlite3
from datetime import datetime

conn = sqlite3.connect("pgi_ia.db")
cursor = conn.cursor()

# Créer tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    code TEXT UNIQUE,
    client TEXT,
    status TEXT,
    start_date DATE,
    budget REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS directives (
    id INTEGER PRIMARY KEY,
    project_id INTEGER,
    code TEXT,
    description TEXT,
    amount REAL,
    status TEXT,
    date DATE,
    FOREIGN KEY (project_id) REFERENCES projects (id)
)
""")

# Insérer données réelles
projects = [
    ("Centre Culturel Kahnawake", "C24-060", "Les Entreprises QMD", "active", "2024-03-15", 1455940.00),
    ("Place Alexis-Nihon", "S-1086", "Alexis Nihon REIT", "active", "2024-06-01", 892000.00)
]

for project in projects:
    cursor.execute("INSERT OR IGNORE INTO projects (name, code, client, status, start_date, budget) VALUES (?, ?, ?, ?, ?, ?)", project)

# Directives réelles Kahnawake
directives = [
    (1, "CO-ME-05", "Boites de jonction 347V non requises", -8806.07, "approuvé", "2024-10-15"),
    (1, "CO-ME-16", "Modification éclairage architectural", -389778.16, "approuvé", "2024-11-20"),
    (1, "CO-ME-20", "Alimentation pompes additionnelles", 60966.12, "soumis", "2024-12-01")
]

for directive in directives:
    cursor.execute("INSERT OR IGNORE INTO directives (project_id, code, description, amount, status, date) VALUES (?, ?, ?, ?, ?, ?)", directive)

conn.commit()
conn.close()

print("✅ Base de données créée avec données réelles")
