#!/usr/bin/env python3
"""
Nettoie les doublons dans la base de données
"""

import sqlite3

DATABASE = 'pgi_ia.db'

# Connexion
conn = sqlite3.connect(DATABASE)
c = conn.cursor()

# Trouver et supprimer les doublons (garde le plus récent)
print("🧹 Nettoyage des doublons...")

c.execute("""
    DELETE FROM documents 
    WHERE id NOT IN (
        SELECT MAX(id) 
        FROM documents 
        GROUP BY filename
    )
""")

deleted = c.rowcount
conn.commit()

# Compter les documents restants
c.execute("SELECT COUNT(*) FROM documents")
total = c.fetchone()[0]

# Afficher les documents
print(f"\n✅ {deleted} doublons supprimés")
print(f"📄 {total} documents uniques restants\n")

print("Documents dans la base:")
print("-" * 80)

c.execute("""
    SELECT filename, project_id, status, 
           datetime(upload_date) as date 
    FROM documents 
    ORDER BY upload_date DESC
""")

for row in c.fetchall():
    status_icon = "✅" if row[2] == "completed" else "🔄" if row[2] == "processing" else "⏳"
    print(f"{status_icon} {row[0][:50]:<50} | {row[1]:<10} | {row[3]}")

conn.close()

print("\n✨ Base de données nettoyée!")