from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
from datetime import datetime
import sqlite3
import subprocess
from openai import OpenAI
import json
import threading

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
DATABASE = 'pgi_ia.db'
ALLOWED_EXTENSIONS = {'pdf'}

# Créer le dossier uploads s'il n'existe pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configuration DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
deepseek_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    """Initialise la base de données"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS documents
                 (id TEXT PRIMARY KEY,
                  filename TEXT NOT NULL,
                  project_id TEXT NOT NULL,
                  upload_date TEXT NOT NULL,
                  status TEXT DEFAULT 'pending',
                  analysis_result TEXT)''')
    conn.commit()
    conn.close()

def extract_text_from_pdf(filepath):
    """Extrait le texte d'un PDF avec pdftotext"""
    try:
        result = subprocess.run(['pdftotext', filepath, '-'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
    except:
        pass
    return "Impossible d'extraire le texte"

def analyze_with_deepseek(text, filename):
    """Analyse le plan électrique avec DeepSeek"""
    
    prompt = f"""
    Analyser ce plan électrique '{filename}' et extraire:
    
    1. Type de plan (distribution, éclairage, télécom, etc.)
    2. Composants principaux détectés
    3. Normes référencées
    4. Problèmes ou alertes
    
    Texte: {text[:2000]}
    
    Format JSON requis.
    """
    
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Expert en génie électrique analysant des plans."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        result = response.choices[0].message.content
        
        # Parser le JSON
        try:
            if "{" in result:
                json_start = result.find("{")
                json_end = result.rfind("}") + 1
                return json.loads(result[json_start:json_end])
        except:
            pass
            
        return {
            "type_plan": "Plan électrique",
            "composants": "Analyse en cours",
            "resume": result[:200]
        }
        
    except Exception as e:
        return {"error": str(e)}

def process_pdf_analysis(file_id, filepath, filename):
    """Analyse un PDF en arrière-plan"""
    print(f"🔍 Analyse de {filename}...")
    
    # Extraire le texte
    text = extract_text_from_pdf(filepath)
    
    # Analyser avec IA
    analysis = analyze_with_deepseek(text, filename)
    
    # Sauvegarder résultats
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("""UPDATE documents 
                 SET status = 'completed', 
                     analysis_result = ? 
                 WHERE id = ?""",
              (json.dumps(analysis, ensure_ascii=False), file_id))
    conn.commit()
    conn.close()
    
    print(f"✅ Analyse terminée pour {filename}")

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'PGI-IA Backend with AI'})

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload avec analyse IA automatique"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier'}), 400
        
        file = request.files['file']
        project_id = request.form.get('project_id', 'default')
        
        if file.filename == '':
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Seuls les PDF sont acceptés'}), 400
        
        # Sauvegarder
        file_id = str(uuid.uuid4())
        filename = f"{file_id}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Base de données
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("""INSERT INTO documents (id, filename, project_id, upload_date, status)
                     VALUES (?, ?, ?, ?, ?)""",
                  (file_id, file.filename, project_id, datetime.now().isoformat(), 'processing'))
        conn.commit()
        conn.close()
        
        # Lancer analyse en arrière-plan
        thread = threading.Thread(
            target=process_pdf_analysis,
            args=(file_id, filepath, file.filename)
        )
        thread.start()
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'filename': file.filename,
            'message': f'✅ {file.filename} uploadé! 🧠 Analyse IA en cours...'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Liste des documents avec statut d'analyse"""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("""SELECT id, filename, project_id, upload_date, status, analysis_result
                     FROM documents 
                     ORDER BY upload_date DESC""")
        
        documents = []
        for row in c.fetchall():
            doc = {
                'id': row[0],
                'filename': row[1],
                'project': row[2],
                'date': row[3],
                'status': row[4]
            }
            
            # Ajouter résumé si analyse terminée
            if row[4] == 'completed' and row[5]:
                try:
                    analysis = json.loads(row[5])
                    doc['type_plan'] = analysis.get('type_plan', 'N/A')
                    doc['has_analysis'] = True
                except:
                    doc['has_analysis'] = False
            else:
                doc['has_analysis'] = False
                
            documents.append(doc)
        
        conn.close()
        return jsonify(documents)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/<file_id>', methods=['GET'])
def get_analysis(file_id):
    """Détails de l'analyse d'un document"""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("""SELECT filename, status, analysis_result 
                     FROM documents WHERE id = ?""", (file_id,))
        
        row = c.fetchone()
        conn.close()
        
        if not row:
            return jsonify({'error': 'Document non trouvé'}), 404
        
        result = {
            'filename': row[0],
            'status': row[1],
            'analysis': json.loads(row[2]) if row[2] else None
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return jsonify({
        'service': 'PGI-IA Backend',
        'version': '2.0',
        'features': ['Upload PDF', 'Analyse IA automatique', 'DeepSeek intégré'],
        'endpoints': ['/upload', '/health', '/api/documents', '/api/analysis/<id>']
    })

if __name__ == '__main__':
    init_db()
    print("🚀 PGI-IA Backend avec IA démarré!")
    print("🧠 DeepSeek configuré pour analyse automatique")
    app.run(host='0.0.0.0', port=5000, debug=True)