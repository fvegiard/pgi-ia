"""
Endpoints Email pour PGI-IA
Gestion des emails avec classification DeepSeek
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import os
from typing import List, Dict

# Import du classifier (sera créé après)
try:
    from backend.email_classifier_deepseek import EmailClassifierDeepSeek
except ImportError:
    EmailClassifierDeepSeek = None

# Créer le blueprint
email_bp = Blueprint('emails', __name__, url_prefix='/api/emails')

# Données mockées pour démarrer
MOCK_EMAILS = [
    {
        "id": 1,
        "from": "architecte@xyz.com",
        "subject": "⚡ Directive CD-203 - Modification urgente éclairage",
        "body": "Suite à notre réunion de ce matin concernant le projet Kahnawake...",
        "received_at": "2025-07-11T09:15:00",
        "read": False,
        "type": "DIRECTIVE",
        "project": "S-1086",
        "priority": "haute",
        "attachments": ["CD-203_eclairage.pdf"],
        "classification": {
            "type": "DIRECTIVE",
            "project": "S-1086",
            "priority": "haute",
            "directive_number": "CD-203",
            "confidence": 95
        }
    },
    {
        "id": 2,
        "from": "ingenieur@abc.com",
        "subject": "📐 Rev.3 Plan E-101 - Distribution électrique",
        "body": "Veuillez trouver en pièce jointe la révision 3 du plan...",
        "received_at": "2025-07-11T08:52:00",
        "read": False,
        "type": "PLAN",
        "project": "C-24-048",
        "priority": "normale",
        "attachments": ["E-101_Rev3.pdf", "E-101_Rev3.dwg"],
        "classification": {
            "type": "PLAN",
            "project": "C-24-048",
            "priority": "normale",
            "confidence": 92
        }
    },
    {
        "id": 3,
        "from": "client@kahnawake.ca",
        "subject": "❓ Question sur l'estimation des coûts supplémentaires",
        "body": "Pouvez-vous clarifier les coûts additionnels mentionnés...",
        "received_at": "2025-07-11T08:30:00",
        "read": False,
        "type": "QUESTION",
        "project": "S-1086",
        "priority": "normale",
        "attachments": [],
        "classification": {
            "type": "QUESTION",
            "project": "S-1086",
            "priority": "normale",
            "confidence": 88
        }
    },
    {
        "id": 4,
        "from": "fournisseur@def.com",
        "subject": "Confirmation de livraison - Matériel électrique",
        "body": "La livraison du matériel électrique commandé est confirmée...",
        "received_at": "2025-07-10T14:20:00",
        "read": True,
        "type": "INFORMATION",
        "project": "C-24-048",
        "priority": "basse",
        "attachments": [],
        "classification": {
            "type": "INFORMATION",
            "project": "C-24-048",
            "priority": "basse",
            "confidence": 91
        }
    }
]

# Instance du classifier (sera initialisée au démarrage)
classifier = None

def init_classifier():
    """Initialise le classifier DeepSeek"""
    global classifier
    if EmailClassifierDeepSeek and not classifier:
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if api_key:
            classifier = EmailClassifierDeepSeek(api_key)
            print("✅ Classifier DeepSeek initialisé")
        else:
            print("⚠️ DEEPSEEK_API_KEY non trouvée")

@email_bp.route('/', methods=['GET'])
def get_emails():
    """Récupère la liste des emails avec filtres optionnels"""
    # Filtres
    project = request.args.get('project')
    email_type = request.args.get('type')
    unread_only = request.args.get('unread', '').lower() == 'true'
    
    # Appliquer les filtres
    emails = MOCK_EMAILS.copy()
    
    if project:
        emails = [e for e in emails if e.get('project') == project]
    
    if email_type:
        emails = [e for e in emails if e.get('type') == email_type.upper()]
    
    if unread_only:
        emails = [e for e in emails if not e.get('read', False)]
    
    return jsonify({
        "emails": emails,
        "total": len(emails),
        "unread": len([e for e in emails if not e.get('read', False)])
    })

@email_bp.route('/<int:email_id>', methods=['GET'])
def get_email(email_id):
    """Récupère les détails d'un email spécifique"""
    email = next((e for e in MOCK_EMAILS if e['id'] == email_id), None)
    
    if not email:
        return jsonify({"error": "Email non trouvé"}), 404
    
    # Marquer comme lu
    email['read'] = True
    
    return jsonify(email)

@email_bp.route('/unread', methods=['GET'])
def get_unread_count():
    """Récupère le nombre d'emails non lus"""
    unread = len([e for e in MOCK_EMAILS if not e.get('read', False)])
    
    return jsonify({
        "unread": unread,
        "by_project": {
            "S-1086": len([e for e in MOCK_EMAILS if not e.get('read', False) and e.get('project') == 'S-1086']),
            "C-24-048": len([e for e in MOCK_EMAILS if not e.get('read', False) and e.get('project') == 'C-24-048'])
        }
    })

@email_bp.route('/classify', methods=['POST'])
def classify_email():
    """Classifie un email avec DeepSeek"""
    if not classifier:
        return jsonify({
            "error": "Classifier non initialisé",
            "fallback": {
                "type": "UNKNOWN",
                "confidence": 0
            }
        }), 503
    
    email_data = request.get_json()
    
    if not email_data:
        return jsonify({"error": "Données email requises"}), 400
    
    # Classification avec DeepSeek
    result = classifier.classify_email(email_data)
    
    return jsonify(result)

@email_bp.route('/process/<int:email_id>', methods=['POST'])
def process_email(email_id):
    """Traite automatiquement un email"""
    email = next((e for e in MOCK_EMAILS if e['id'] == email_id), None)
    
    if not email:
        return jsonify({"error": "Email non trouvé"}), 404
    
    action = request.json.get('action')
    
    # Simuler le traitement selon l'action
    result = {
        "email_id": email_id,
        "action": action,
        "status": "completed",
        "timestamp": datetime.now().isoformat()
    }
    
    if action == "create_directive":
        result["result"] = {
            "directive_created": True,
            "directive_number": email['classification'].get('directive_number', 'CD-NEW'),
            "project": email['project']
        }
    elif action == "analyze_pdf":
        result["result"] = {
            "analysis_started": True,
            "files": email.get('attachments', [])
        }
    elif action == "suggest_response":
        result["result"] = {
            "suggested_response": "Bonjour,\n\nMerci pour votre email. Concernant votre question sur les coûts supplémentaires..."
        }
    
    return jsonify(result)

@email_bp.route('/stats', methods=['GET'])
def get_email_stats():
    """Récupère les statistiques des emails"""
    stats = {
        "total": len(MOCK_EMAILS),
        "unread": len([e for e in MOCK_EMAILS if not e.get('read', False)]),
        "processed_today": 12,  # Mockée
        "pending": 5,  # Mockée
        "by_type": {
            "DIRECTIVE": len([e for e in MOCK_EMAILS if e.get('type') == 'DIRECTIVE']),
            "PLAN": len([e for e in MOCK_EMAILS if e.get('type') == 'PLAN']),
            "QUESTION": len([e for e in MOCK_EMAILS if e.get('type') == 'QUESTION']),
            "CHANGEMENT": len([e for e in MOCK_EMAILS if e.get('type') == 'CHANGEMENT']),
            "INFORMATION": len([e for e in MOCK_EMAILS if e.get('type') == 'INFORMATION'])
        },
        "classification_accuracy": 94.5,  # Mockée
        "time_saved_weekly": 4.2  # Heures mockées
    }
    
    return jsonify(stats)

# Initialiser au chargement du module
init_classifier()