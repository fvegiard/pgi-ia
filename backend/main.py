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
    c.execute('''CREATE TABLE IF NOT EXISTS documents
                 (id TEXT PRIMARY KEY,
                  filename TEXT NOT NULL,
                  project_id TEXT NOT NULL,
                  upload_date TEXT NOT NULL,
                  status TEXT DEFAULT 'pending',
                  analysis_result TEXT)''')
    conn.commit()
    conn.close()

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'PGI-IA Backend'})

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


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status and statistics"""
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        # Get document count by status
        c.execute("""SELECT status, COUNT(*) FROM documents GROUP BY status""")
        status_counts = dict(c.fetchall())
        
        # Get total documents
        c.execute("""SELECT COUNT(*) FROM documents""")
        total_docs = c.fetchone()[0]
        
        # Get project statistics
        c.execute("""SELECT project_id, COUNT(*) FROM documents GROUP BY project_id""")
        project_counts = dict(c.fetchall())
        
        conn.close()
        
        # Check API status
        api_status = {
            "openai": bool(os.getenv("OPENAI_API_KEY", "").startswith("sk-")),
            "deepseek": bool(os.getenv("DEEPSEEK_API_KEY", "").startswith("sk-")),
            "gemini": bool(os.getenv("GEMINI_API_KEY", "") and "YOUR_" not in os.getenv("GEMINI_API_KEY", "")),
            "anthropic": bool(os.getenv("ANTHROPIC_API_KEY", "").startswith("sk-"))
        }
        
        # Get GPU status
        gpu_available = False
        try:
            import subprocess
            result = subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                gpu_available = True
        except:
            pass
        
        status = {
            "service": "PGI-IA Backend",
            "version": "4.1",
            "timestamp": datetime.now().isoformat(),
            "status": "operational",
            "statistics": {
                "total_documents": total_docs,
                "documents_by_status": status_counts,
                "documents_by_project": project_counts
            },
            "apis": api_status,
            "gpu_available": gpu_available,
            "endpoints": [
                "/health",
                "/api/status", 
                "/api/documents",
                "/api/upload",
                "/api/analyze"
            ]
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({
            "service": "PGI-IA Backend",
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/')
def index():
    return jsonify({
        'service': 'PGI-IA Backend',
        'version': '1.0',
        'endpoints': ['/upload', '/health', '/api/documents']
    })


import subprocess
from openai import OpenAI
import json
import PyPDF2
from pdf2image import convert_from_path
import pytesseract

# Configuration DeepSeek
DEEPSEEK_API_KEY = "sk-ccc37a109afb461989af8cf994a8bc60"
deepseek_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

def extract_text_from_pdf(filepath):
    """Extrait le texte d'un PDF avec plusieurs méthodes"""
    text = ""
    
    # Méthode 1: PyPDF2
    try:
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        if len(text.strip()) > 100:
            return text
    except:
        pass
    
    # Méthode 2: pdftotext
    try:
        result = subprocess.run(['pdftotext', filepath, '-'], 
                              capture_output=True, text=True)
        if result.returncode == 0 and len(result.stdout) > 100:
            return result.stdout
    except:
        pass
    
    # Méthode 3: OCR avec Tesseract
    try:
        images = convert_from_path(filepath)
        for image in images:
            text += pytesseract.image_to_string(image) + "\n"
    except:
        pass
    
    return text

def analyze_with_deepseek(text, filename):
    """Analyse le plan électrique avec DeepSeek"""
    
    prompt = f"""
    Analyser ce plan électrique '{filename}' et extraire les informations suivantes:
    
    1. Type de plan (distribution, éclairage, télécom, etc.)
    2. Composants principaux (panneaux, circuits, équipements)
    3. Normes et codes référencés
    4. Alertes ou problèmes potentiels
    5. Résumé technique
    
    Texte du plan:
    {text[:3000]}
    
    Retourner le résultat en format JSON.
    """
    
    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Tu es un expert en génie électrique analysant des plans techniques."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        result = response.choices[0].message.content
        
        # Essayer de parser en JSON
        try:
            # Extraire le JSON du texte
            if "{" in result:
                json_start = result.find("{")
                json_end = result.rfind("}") + 1
                json_str = result[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
            
        # Si pas de JSON, retourner le texte brut
        return {
            "type_plan": "À déterminer",
            "composants": result,
            "normes": [],
            "alertes": [],
            "resume": result[:200]
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "type_plan": "Erreur d'analyse",
            "resume": "Erreur lors de l'analyse IA"
        }

def process_pdf_analysis(file_id, filepath, filename):
    """Traite l'analyse complète d'un PDF"""
    
    print(f"🔍 Début de l'analyse pour {filename}...")
    
    # 1. Extraire le texte
    print("📄 Extraction du texte...")
    text = extract_text_from_pdf(filepath)
    
    if not text or len(text) < 50:
        return {
            "status": "error",
            "message": "Impossible d'extraire le texte du PDF"
        }
    
    print(f"✅ Texte extrait: {len(text)} caractères")
    
    # 2. Analyse avec DeepSeek
    print("🧠 Analyse IA en cours...")
    analysis = analyze_with_deepseek(text, filename)
    
    # 3. Mettre à jour la base de données
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("""UPDATE documents 
                 SET status = 'completed', 
                     analysis_result = ? 
                 WHERE id = ?""",
              (json.dumps(analysis, ensure_ascii=False), file_id))
    conn.commit()
    conn.close()
    
    print("✅ Analyse terminée et sauvegardée!")
    
    return {
        "status": "success",
        "analysis": analysis
    }

@app.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint pour upload de fichiers PDF avec analyse automatique"""
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
        c.execute("""INSERT INTO documents (id, filename, project_id, upload_date, status)
                     VALUES (?, ?, ?, ?, ?)""",
                  (file_id, file.filename, project_id, datetime.now().isoformat(), 'processing'))
        conn.commit()
        conn.close()
        
        # Lancer l'analyse IA en arrière-plan
        import threading
        thread = threading.Thread(
            target=process_pdf_analysis,
            args=(file_id, filepath, file.filename)
        )
        thread.start()
        
        # Retourner le succès
        return jsonify({
            'success': True,
            'file_id': file_id,
            'filename': file.filename,
            'message': f'{file.filename} uploadé! Analyse IA en cours...'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis/<file_id>', methods=['GET'])
def get_analysis(file_id):
    """Récupère les résultats d'analyse d'un document"""
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


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
