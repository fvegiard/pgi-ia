#!/usr/bin/env python3
"""
Corrige le backend pour accepter les uploads
"""

import os
import shutil

# Créer le fichier backend corrigé
backend_code = '''from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
from datetime import datetime
import sqlite3

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
DATABASE = 'pgi_ia.db'
ALLOWED_EXTENSIONS = {'pdf'}

# Créer le dossier uploads s'il n'existe pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    """Initialise la base de données"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(\'\'\'CREATE TABLE IF NOT EXISTS documents
                 (id TEXT PRIMARY KEY,
                  filename TEXT NOT NULL,
                  project_id TEXT NOT NULL,
                  upload_date TEXT NOT NULL,
                  status TEXT DEFAULT 'pending',
                  analysis_result TEXT)\'\'\')
    conn.commit()
    conn.close()

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'PGI-IA Backend'})

@app.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint pour upload de fichiers PDF"""
    try:
        # Vérifier si un fichier est présent
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier trouvé'}), 400
        
        file = request.files['file']
        project_id = request.form.get('project_id', 'default')
        
        # Vérifier si un fichier a été sélectionné
        if file.filename == '':
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
        # Vérifier l'extension
        if not allowed_file(file.filename):
            return jsonify({'error': 'Seuls les fichiers PDF sont acceptés'}), 400
        
        # Générer un ID unique
        file_id = str(uuid.uuid4())
        
        # Sauvegarder le fichier
        filename = f"{file_id}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Enregistrer dans la base de données
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("""INSERT INTO documents (id, filename, project_id, upload_date)
                     VALUES (?, ?, ?, ?)""",
                  (file_id, file.filename, project_id, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        # Retourner le succès
        return jsonify({
            'success': True,
            'file_id': file_id,
            'filename': file.filename,
            'message': f'{file.filename} uploadé avec succès!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Récupère la liste des documents"""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("""SELECT id, filename, project_id, upload_date, status 
                     FROM documents 
                     ORDER BY upload_date DESC 
                     LIMIT 20""")
        
        documents = []
        for row in c.fetchall():
            documents.append({
                'id': row[0],
                'filename': row[1],
                'project': row[2],
                'date': row[3],
                'status': row[4]
            })
        
        conn.close()
        return jsonify(documents)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return jsonify({
        'service': 'PGI-IA Backend',
        'version': '1.0',
        'endpoints': ['/upload', '/health', '/api/documents']
    })

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
'''

# Sauvegarder l'ancien backend
if os.path.exists('backend/main.py'):
    shutil.copy('backend/main.py', 'backend/main.py.backup')
    print("✅ Backup de l'ancien backend créé")

# Créer le dossier backend s'il n'existe pas
os.makedirs('backend', exist_ok=True)

# Écrire le nouveau backend
with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(backend_code)

print("✅ Backend mis à jour avec support upload!")
print("📁 Dossier uploads créé")
print("🗄️ Base de données SQLite configurée")
print("\nRedémarrage du backend nécessaire...")