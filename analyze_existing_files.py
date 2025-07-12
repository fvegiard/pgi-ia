#!/usr/bin/env python3
"""
Lance l'analyse IA sur les fichiers déjà uploadés
"""

import sqlite3
import os
import sys
sys.path.append('/home/fvegi/dev/pgi-ia')
from backend_with_ai import process_pdf_analysis

DATABASE = 'pgi_ia.db'
UPLOAD_FOLDER = 'uploads'

def analyze_pending_files():
    """Analyse tous les fichiers en statut 'pending'"""
    
    # Connexion à la base
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Récupérer les fichiers non analysés
    c.execute("""SELECT id, filename FROM documents 
                 WHERE status = 'pending' OR status = 'completed'""")
    
    files = c.fetchall()
    conn.close()
    
    if not files:
        print("❌ Aucun fichier trouvé dans la base de données")
        return
    
    print(f"📁 {len(files)} fichiers trouvés")
    
    # Analyser chaque fichier
    for file_id, filename in files:
        # Trouver le fichier physique
        filepath = None
        for f in os.listdir(UPLOAD_FOLDER):
            if f.endswith(filename):
                filepath = os.path.join(UPLOAD_FOLDER, f)
                break
        
        if filepath and os.path.exists(filepath):
            print(f"\n🔄 Analyse de {filename}...")
            
            # Mettre à jour le statut
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("UPDATE documents SET status = 'processing' WHERE id = ?", (file_id,))
            conn.commit()
            conn.close()
            
            # Lancer l'analyse
            try:
                process_pdf_analysis(file_id, filepath, filename)
                print(f"✅ {filename} analysé avec succès!")
            except Exception as e:
                print(f"❌ Erreur pour {filename}: {str(e)}")
        else:
            print(f"⚠️  Fichier physique non trouvé pour {filename}")
    
    print("\n✨ Analyse terminée!")
    
    # Afficher le résumé
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM documents WHERE status = 'completed'")
    completed = c.fetchone()[0]
    conn.close()
    
    print(f"📊 Total analysés: {completed} fichiers")

if __name__ == "__main__":
    print("🧠 ANALYSE IA DES FICHIERS EXISTANTS")
    print("=" * 50)
    analyze_pending_files()