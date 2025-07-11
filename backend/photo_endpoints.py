"""
Endpoints Flask pour le système photos GPS
"""

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from photo_gps_system import photo_gps_system
import os
import logging

logger = logging.getLogger(__name__)

# Blueprint photos
photos_bp = Blueprint('photos', __name__, url_prefix='/api/photos')

# Extensions autorisées
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'heic', 'heif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@photos_bp.route('/upload', methods=['POST'])
def upload_photo():
    """Upload d'une photo avec extraction GPS"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier fourni"}), 400
        
        file = request.files['file']
        project_id = request.form.get('project_id', type=int)
        description = request.form.get('description', '')
        
        if not project_id:
            return jsonify({"error": "project_id requis"}), 400
        
        if file.filename == '':
            return jsonify({"error": "Nom fichier vide"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                "error": "Type fichier non autorisé",
                "allowed": list(ALLOWED_EXTENSIONS)
            }), 400
        
        # Sécuriser nom fichier
        filename = secure_filename(file.filename)
        
        # Upload et traitement
        result = photo_gps_system.upload_photo(
            project_id=project_id,
            file_data=file,
            filename=filename,
            description=description
        )
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify({
            "status": "success",
            "message": "Photo uploadée avec succès",
            "data": result
        })
        
    except Exception as e:
        logger.error(f"Erreur upload photo: {e}")
        return jsonify({"error": str(e)}), 500

@photos_bp.route('/project/<int:project_id>', methods=['GET'])
def get_project_photos(project_id):
    """Récupère les photos d'un projet"""
    try:
        has_gps = request.args.get('has_gps')
        if has_gps is not None:
            has_gps = has_gps.lower() == 'true'
        
        photos = photo_gps_system.get_project_photos(project_id, has_gps)
        
        return jsonify({
            "photos": photos,
            "count": len(photos),
            "project_id": project_id
        })
        
    except Exception as e:
        logger.error(f"Erreur récupération photos: {e}")
        return jsonify({"error": str(e)}), 500

@photos_bp.route('/markers/<int:project_id>', methods=['GET'])
def get_photo_markers(project_id):
    """Récupère les markers photos pour carte/plan"""
    try:
        markers = photo_gps_system.get_photo_markers_for_map(project_id)
        
        return jsonify({
            "markers": markers,
            "count": len(markers),
            "project_id": project_id
        })
        
    except Exception as e:
        logger.error(f"Erreur markers photos: {e}")
        return jsonify({"error": str(e)}), 500

@photos_bp.route('/<int:photo_id>/coordinates', methods=['POST'])
def update_plan_coordinates(photo_id):
    """Met à jour les coordonnées plan d'une photo"""
    try:
        data = request.get_json()
        plan_bounds = data.get('plan_bounds')
        
        if not plan_bounds:
            return jsonify({"error": "plan_bounds requis"}), 400
        
        # Calculer coordonnées plan depuis GPS
        coordinates = photo_gps_system.calculate_plan_coordinates(
            photo_id, plan_bounds
        )
        
        if coordinates is None:
            return jsonify({"error": "Impossible de calculer coordonnées"}), 400
        
        return jsonify({
            "status": "success",
            "photo_id": photo_id,
            "plan_coordinates": {
                "x": coordinates[0],
                "y": coordinates[1]
            }
        })
        
    except Exception as e:
        logger.error(f"Erreur coordonnées plan: {e}")
        return jsonify({"error": str(e)}), 500

@photos_bp.route('/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    """Supprime une photo"""
    try:
        result = photo_gps_system.delete_photo(photo_id)
        
        if 'error' in result:
            return jsonify(result), 404 if "non trouvée" in result['error'] else 500
        
        return jsonify({
            "status": "success",
            "message": "Photo supprimée",
            "data": result
        })
        
    except Exception as e:
        logger.error(f"Erreur suppression photo: {e}")
        return jsonify({"error": str(e)}), 500

@photos_bp.route('/<int:photo_id>/file', methods=['GET'])
def get_photo_file(photo_id):
    """Récupère le fichier image"""
    try:
        # Récupérer chemin fichier
        from database_manager import db_manager
        
        with db_manager.get_connection() as conn:
            cursor = conn.execute(
                "SELECT file_path, filename FROM photos_geolocated WHERE id = ?",
                (photo_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                return jsonify({"error": "Photo non trouvée"}), 404
            
            file_path, filename = row[0], row[1]
            
            if not os.path.exists(file_path):
                return jsonify({"error": "Fichier physique introuvable"}), 404
            
            return send_file(file_path, as_attachment=False, download_name=filename)
        
    except Exception as e:
        logger.error(f"Erreur récupération fichier: {e}")
        return jsonify({"error": str(e)}), 500

@photos_bp.route('/<int:photo_id>/info', methods=['GET'])
def get_photo_info(photo_id):
    """Récupère les informations détaillées d'une photo"""
    try:
        from database_manager import db_manager
        
        with db_manager.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM photos_geolocated WHERE id = ?",
                (photo_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                return jsonify({"error": "Photo non trouvée"}), 404
            
            photo_info = dict(row)
            
            # Parser métadonnées JSON si présentes
            if photo_info.get('metadata_exif'):
                try:
                    import json
                    photo_info['metadata_exif'] = json.loads(photo_info['metadata_exif'])
                except:
                    pass
            
            return jsonify({
                "photo": photo_info
            })
        
    except Exception as e:
        logger.error(f"Erreur info photo: {e}")
        return jsonify({"error": str(e)}), 500

@photos_bp.route('/test', methods=['GET'])
def test_photo_system():
    """Test du système photos"""
    try:
        # Vérifier répertoire upload
        upload_dir = photo_gps_system.upload_dir
        
        return jsonify({
            "status": "✅ Système photos GPS opérationnel",
            "upload_dir": upload_dir,
            "upload_dir_exists": os.path.exists(upload_dir),
            "allowed_extensions": list(ALLOWED_EXTENSIONS),
            "endpoints": {
                "POST /upload": "Upload photo avec GPS",
                "GET /project/<id>": "Photos du projet",
                "GET /markers/<id>": "Markers pour carte",
                "POST /<id>/coordinates": "Coordonnées plan",
                "DELETE /<id>": "Supprimer photo",
                "GET /<id>/file": "Fichier image",
                "GET /<id>/info": "Infos détaillées"
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "❌ Erreur système photos",
            "error": str(e)
        }), 500