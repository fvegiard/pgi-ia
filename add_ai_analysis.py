#!/usr/bin/env python3
"""
Ajoute l'analyse IA automatique au backend
"""

import os

# Code pour ajouter l'analyse IA
analysis_code = '''
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
                text += page.extract_text() + "\\n"
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
            text += pytesseract.image_to_string(image) + "\\n"
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

# Modifier la fonction upload pour lancer l'analyse
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
'''

# Lire le backend actuel
with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Ajouter les imports nécessaires
imports = '''from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
from datetime import datetime
import sqlite3
import subprocess
from openai import OpenAI
import json
import threading'''

content = content.replace('from flask import Flask, request, jsonify', imports)

# Ajouter le code d'analyse avant if __name__
main_block = "if __name__ == '__main__':"
content = content.replace(main_block, analysis_code + '\n\n' + main_block)

# Sauvegarder
with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Analyse IA ajoutée au backend!")
print("🧠 DeepSeek configuré pour l'analyse automatique")
print("🔄 L'analyse se lance automatiquement après chaque upload")
print("\n⚠️  Redémarrage du backend nécessaire...")