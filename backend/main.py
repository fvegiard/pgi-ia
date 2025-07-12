"""
PGI-IA Backend API
Progiciel de Gestion Intégré assisté par Intelligence Artificielle
Développé pour DR Électrique - Francis Végiard
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import yaml
import logging
from datetime import datetime
import json

# Import des agents
try:
    from agents.directive_agent import DirectiveAgent
    from core.orchestrator import AgentOrchestrator
except ImportError:
    print("⚠️ Modules agents non trouvés - Mode démo activé")
    DirectiveAgent = None
    AgentOrchestrator = None

# Import du nouvel orchestrateur
try:
    from services.orchestrator import orchestrator as pgi_orchestrator
except ImportError:
    print("⚠️ Orchestrateur PGI non trouvé")
    pgi_orchestrator = None

# Configuration
app = Flask(__name__)
CORS(app)

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Chargement configuration agents
def load_config():
    """Charge la configuration des agents IA"""
    try:
        config_path = os.path.join('config', 'agents.yaml')
        if not os.path.exists(config_path):
            config_path = os.path.join('config', 'agents.example.yaml')
            logger.warning("Utilisation du fichier example - Créez config/agents.yaml")
            
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Erreur chargement config: {e}")
        return None

# Initialisation
config = load_config()
orchestrator = None

if config and AgentOrchestrator:
    try:
        orchestrator = AgentOrchestrator(config)
        logger.info("✅ PGI-IA Backend initialisé avec succès")
    except Exception as e:
        logger.error(f"Erreur init orchestrateur: {e}")
else:
    logger.info("🔄 Mode démo - Configuration orchestrateur à compléter")

@app.route('/')
def index():
    """Page d'accueil API"""
    status = pgi_orchestrator.get_system_status() if pgi_orchestrator else {
        "status": "Demo mode",
        "apis": {"deepseek": False, "gemini": False, "ollama": False}
    }
    
    return jsonify({
        "service": "PGI-IA Backend API",
        "version": "1.0.0",
        "status": "🚀 Opérationnel",
        "mode": "Production" if orchestrator else "Démo",
        "system": status,
        "endpoints": {
            "/": "GET - État du système",
            "/upload": "POST - Upload fichiers (PDF, images, plans)",
            "/directive/process": "POST - Traitement directive PDF",
            "/plan/analyze": "POST - Analyse plan 2D → 3D",
            "/photo/geolocate": "POST - Géolocalisation photo",
            "/projects": "GET - Liste projets actifs",
            "/ai/command": "POST - Commande IA naturelle"
        }
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload et traitement automatique des fichiers"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier fourni"}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Nom fichier vide"}), 400
            
        # Sauvegarde dans drop_zone
        os.makedirs('data/drop_zone', exist_ok=True)
        upload_path = os.path.join('data', 'drop_zone', file.filename)
        file.save(upload_path)
        
        # Détection type et traitement approprié
        file_ext = file.filename.lower().split('.')[-1]
        
        result = {
            "id": f"AUTO-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "date_recue": datetime.now().strftime("%Y-%m-%d"),
            "description": f"Fichier {file.filename} traité automatiquement",
            "prix": "À déterminer",
            "po_client": "",
            "statut": "À préparer",
            "ai_enhanced": False
        }
        
        if file_ext == 'pdf' and orchestrator:
            # Traitement directive PDF
            try:
                result = orchestrator.process_directive(upload_path)
            except Exception as e:
                logger.error(f"Erreur traitement PDF: {e}")
                result["description"] = f"Erreur traitement {file.filename}: {str(e)}"
        
        return jsonify({
            "status": "✅ Traitement terminé",
            "file": file.filename,
            "type": file_ext,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erreur upload: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/projects', methods=['GET'])
def get_projects():
    """Retourne la liste des projets actifs"""
    try:
        projects = {
            "kahnawake": {
                "id": "S-1086",
                "nom": "Musée Kahnawake", 
                "statut": "Estimation",
                "po_client": "QMD",
                "directives_count": 4,
                "derniere_maj": "2025-01-10"
            },
            "alexis_nihon": {
                "id": "C-24-048",
                "nom": "Place Alexis-Nihon",
                "statut": "Construction", 
                "po_client": "JCB",
                "directives_count": 5,
                "derniere_maj": "2025-01-09"
            }
        }
        return jsonify(projects)
        
    except Exception as e:
        logger.error(f"Erreur projets: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/ai/command', methods=['POST'])
def ai_command():
    """Interface commande IA naturelle"""
    try:
        data = request.get_json()
        command = data.get('command', '')
        
        if not command:
            return jsonify({"error": "Commande vide"}), 400
        
        # Traitement basique si orchestrateur disponible
        if orchestrator:
            try:
                response = orchestrator.process_command(command)
            except Exception as e:
                response = {
                    "response": f"Erreur traitement commande: {str(e)}",
                    "agent_used": "error"
                }
        else:
            # Mode démo
            response = {
                "response": f"Commande reçue: '{command}' - Mode démo actif. Configurez les agents IA dans config/agents.yaml",
                "agent_used": "demo"
            }
        
        return jsonify({
            "command": command,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erreur commande IA: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Vérification environnement
    if not os.path.exists('data/drop_zone'):
        os.makedirs('data/drop_zone')
        logger.info("📁 Dossier drop_zone créé")
        
    if not os.path.exists('config/agents.yaml'):
        logger.warning("⚠️  Créez config/agents.yaml depuis agents.example.yaml")
    
    # Message démarrage
    print("\n" + "="*60)
    print("🚀 PGI-IA Backend API - Démarrage")
    print("="*60)
    print(f"📍 URL: http://localhost:{int(os.environ.get('PORT', 5001))}")
    print(f"📂 Drop Zone: data/drop_zone/")
    print(f"🔧 Config: config/agents.yaml")
    print(f"📋 Mode: {'Production' if orchestrator else 'Démo'}")
    print("="*60)
    
    # Démarrage serveur
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)