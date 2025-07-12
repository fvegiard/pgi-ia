#!/usr/bin/env python3
"""
Force l'analyse du premier fichier pour tester
"""

import sqlite3
import subprocess
import json
from openai import OpenAI

# Config
DATABASE = 'pgi_ia.db'
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

# Client DeepSeek
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

# Récupérer le premier fichier
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
c.execute("SELECT id, filename FROM documents WHERE status = 'pending' LIMIT 1")
row = c.fetchone()
conn.close()

if not row:
    print("Aucun fichier à analyser")
    exit()

file_id, filename = row
print(f"🔍 Analyse de {filename}...")

# Trouver le fichier
import os
filepath = None
for f in os.listdir('uploads'):
    if filename in f:
        filepath = os.path.join('uploads', f)
        break

if not filepath:
    print("Fichier non trouvé!")
    exit()

# Extraire le texte
print("📄 Extraction du texte...")
result = subprocess.run(['pdftotext', filepath, '-'], capture_output=True, text=True)
text = result.stdout[:2000]  # Limiter pour le test

# Analyse rapide
print("🧠 Analyse DeepSeek...")
try:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Tu es un expert électrique. Réponds en JSON."},
            {"role": "user", "content": f"Analyse ce plan: {filename}\n\nTexte: {text[:500]}\n\nDonne: type_plan, resume (50 mots max)"}
        ],
        max_tokens=200,
        temperature=0.3
    )
    
    analysis = {
        "type_plan": "Plan électrique",
        "resume": response.choices[0].message.content[:200],
        "status": "Analysé avec DeepSeek"
    }
    
    # Sauvegarder
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE documents SET status = 'completed', analysis_result = ? WHERE id = ?",
              (json.dumps(analysis), file_id))
    conn.commit()
    conn.close()
    
    print("✅ Analyse terminée!")
    print(f"📊 Résultat: {analysis}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")