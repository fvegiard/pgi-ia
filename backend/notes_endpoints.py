"""
Endpoints Flask pour le système de notes intelligentes
"""

from flask import Blueprint, request, jsonify
from notes_system import notes_system
import logging

logger = logging.getLogger(__name__)

# Création du blueprint
notes_bp = Blueprint('notes', __name__, url_prefix='/api/notes')

@notes_bp.route('/', methods=['GET'])
def get_notes():
    """Récupère les notes d'un projet"""
    try:
        project_id = request.args.get('project_id', type=int)
        statut = request.args.get('statut')
        query = request.args.get('search')
        
        if not project_id:
            return jsonify({"error": "project_id requis"}), 400
        
        if query:
            # Recherche dans les notes
            notes = notes_system.search_notes(project_id, query)
        else:
            # Récupération normale
            notes = notes_system.get_project_notes(project_id, statut)
        
        return jsonify({
            "notes": notes,
            "count": len(notes),
            "project_id": project_id
        })
        
    except Exception as e:
        logger.error(f"Erreur GET notes: {e}")
        return jsonify({"error": str(e)}), 500

@notes_bp.route('/', methods=['POST'])
def create_note():
    """Crée une nouvelle note"""
    try:
        data = request.get_json()
        
        if not data or not data.get('note_originale'):
            return jsonify({"error": "note_originale requise"}), 400
        
        if not data.get('project_id'):
            return jsonify({"error": "project_id requis"}), 400
        
        result = notes_system.create_note(
            project_id=data['project_id'],
            note_originale=data['note_originale'],
            categorie=data.get('categorie', 'Général')
        )
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify({
            "status": "success",
            "message": "Note créée et reformulation IA lancée",
            "data": result
        })
        
    except Exception as e:
        logger.error(f"Erreur POST note: {e}")
        return jsonify({"error": str(e)}), 500

@notes_bp.route('/<int:note_id>/approve', methods=['POST'])
def approve_note(note_id):
    """Approuve une note reformulée"""
    try:
        data = request.get_json()
        note_finale = data.get('note_finale')
        
        if not note_finale:
            return jsonify({"error": "note_finale requise"}), 400
        
        result = notes_system.approve_note(note_id, note_finale)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify({
            "status": "success",
            "message": "Note approuvée et finalisée",
            "data": result
        })
        
    except Exception as e:
        logger.error(f"Erreur approbation note: {e}")
        return jsonify({"error": str(e)}), 500

@notes_bp.route('/pending', methods=['GET'])
def get_pending_notes():
    """Récupère les notes en attente d'approbation"""
    try:
        project_id = request.args.get('project_id', type=int)
        
        notes = notes_system.get_pending_notes(project_id)
        
        return jsonify({
            "pending_notes": notes,
            "count": len(notes)
        })
        
    except Exception as e:
        logger.error(f"Erreur notes en attente: {e}")
        return jsonify({"error": str(e)}), 500

@notes_bp.route('/stats', methods=['GET'])
def get_notes_stats():
    """Statistiques des notes"""
    try:
        project_id = request.args.get('project_id', type=int)
        
        stats = notes_system.get_notes_stats(project_id)
        
        return jsonify({
            "stats": stats,
            "project_id": project_id
        })
        
    except Exception as e:
        logger.error(f"Erreur stats notes: {e}")
        return jsonify({"error": str(e)}), 500

@notes_bp.route('/categories', methods=['GET'])
def get_categories():
    """Liste des catégories disponibles"""
    categories = [
        "Général",
        "Technique", 
        "Sécurité",
        "Planification",
        "Problème",
        "Solution",
        "Réunion",
        "Client",
        "Équipe",
        "Matériel",
        "Installation",
        "Test"
    ]
    
    return jsonify({
        "categories": categories
    })

# Test endpoints
@notes_bp.route('/test', methods=['GET'])
def test_notes_system():
    """Test du système de notes"""
    try:
        # Test basique
        stats = notes_system.get_notes_stats()
        
        return jsonify({
            "status": "✅ Système notes opérationnel",
            "stats": stats,
            "endpoints": {
                "GET /": "Récupérer notes projet",
                "POST /": "Créer nouvelle note",  
                "POST /<id>/approve": "Approuver note",
                "GET /pending": "Notes en attente",
                "GET /stats": "Statistiques",
                "GET /categories": "Catégories disponibles"
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "❌ Erreur système notes",
            "error": str(e)
        }), 500