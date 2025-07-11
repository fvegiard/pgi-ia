"""
Système Photos GPS PGI-IA
Extraction métadonnées GPS iPhone + géolocalisation sur plan principal
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import logging
from database_manager import db_manager

logger = logging.getLogger(__name__)

class PhotoGPSSystem:
    """Système de gestion photos géolocalisées"""
    
    def __init__(self, upload_dir: str = "data/photos"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)
    
    def extract_gps_from_image(self, image_path: str) -> Dict:
        """Extrait les données GPS d'une image iPhone"""
        try:
            with Image.open(image_path) as image:
                exif_data = image._getexif()
                
                if not exif_data:
                    return {"error": "Pas de données EXIF"}
                
                # Extraire données GPS
                gps_data = {}
                exif_dict = {}
                
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    exif_dict[tag] = value
                    
                    if tag == "GPSInfo":
                        for gps_tag_id, gps_value in value.items():
                            gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                            gps_data[gps_tag] = gps_value
                
                if not gps_data:
                    return {"error": "Pas de données GPS dans l'image"}
                
                # Convertir coordonnées GPS
                coords = self._convert_gps_coordinates(gps_data)
                
                # Extraire autres métadonnées utiles
                metadata = {
                    "datetime": exif_dict.get("DateTime"),
                    "datetime_original": exif_dict.get("DateTimeOriginal"),
                    "camera_make": exif_dict.get("Make"),
                    "camera_model": exif_dict.get("Model"),
                    "image_width": exif_dict.get("ExifImageWidth"),
                    "image_height": exif_dict.get("ExifImageHeight"),
                    "orientation": exif_dict.get("Orientation")
                }
                
                result = {
                    "gps_data": coords,
                    "metadata": metadata,
                    "raw_gps": gps_data,
                    "raw_exif": exif_dict
                }
                
                return result
                
        except Exception as e:
            logger.error(f"Erreur extraction GPS: {e}")
            return {"error": str(e)}
    
    def _convert_gps_coordinates(self, gps_data: Dict) -> Dict:
        """Convertit les coordonnées GPS au format décimal"""
        try:
            # Latitude
            lat_dms = gps_data.get("GPSLatitude")
            lat_ref = gps_data.get("GPSLatitudeRef")
            
            # Longitude  
            lon_dms = gps_data.get("GPSLongitude")
            lon_ref = gps_data.get("GPSLongitudeRef")
            
            if not (lat_dms and lon_dms):
                return {"error": "Coordonnées GPS incomplètes"}
            
            # Conversion DMS vers décimal
            latitude = self._dms_to_decimal(lat_dms, lat_ref)
            longitude = self._dms_to_decimal(lon_dms, lon_ref)
            
            # Altitude si disponible
            altitude = None
            if "GPSAltitude" in gps_data:
                alt_value = gps_data["GPSAltitude"]
                alt_ref = gps_data.get("GPSAltitudeRef", 0)
                if isinstance(alt_value, tuple):
                    altitude = float(alt_value[0]) / float(alt_value[1])
                    if alt_ref == 1:  # Sous le niveau de la mer
                        altitude = -altitude
            
            return {
                "latitude": latitude,
                "longitude": longitude,
                "altitude": altitude,
                "accuracy": gps_data.get("GPSHPositioningError")
            }
            
        except Exception as e:
            logger.error(f"Erreur conversion coordonnées: {e}")
            return {"error": str(e)}
    
    def _dms_to_decimal(self, dms: Tuple, ref: str) -> float:
        """Convertit DMS (Degrés, Minutes, Secondes) en décimal"""
        degrees = float(dms[0])
        minutes = float(dms[1]) / 60.0
        seconds = float(dms[2]) / 3600.0
        
        decimal = degrees + minutes + seconds
        
        # Appliquer référence (N/S pour lat, E/W pour lon)
        if ref in ['S', 'W']:
            decimal = -decimal
            
        return decimal
    
    def upload_photo(self, project_id: int, file_data, filename: str, 
                    description: str = "") -> Dict:
        """Upload et traitement d'une photo avec extraction GPS"""
        try:
            # Générer nom fichier unique
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{filename}"
            file_path = os.path.join(self.upload_dir, safe_filename)
            
            # Sauvegarder fichier
            file_data.save(file_path)
            
            # Extraire données GPS
            gps_extraction = self.extract_gps_from_image(file_path)
            
            if "error" in gps_extraction:
                # Photo sans GPS - sauvegarder quand même
                photo_id = db_manager.create_photo(
                    project_id=project_id,
                    filename=safe_filename,
                    file_path=file_path,
                    gps_data={},
                    description=description,
                    metadata_exif={}
                )
                
                return {
                    "photo_id": photo_id,
                    "filename": safe_filename,
                    "status": "uploaded_no_gps",
                    "message": "Photo uploadée sans données GPS",
                    "error": gps_extraction["error"]
                }
            
            # Extraire date de prise si disponible
            date_prise = None
            if gps_extraction["metadata"].get("DateTimeOriginal"):
                try:
                    date_prise = datetime.strptime(
                        gps_extraction["metadata"]["DateTimeOriginal"],
                        "%Y:%m:%d %H:%M:%S"
                    )
                except:
                    pass
            
            # Sauvegarder en base avec GPS
            photo_id = db_manager.create_photo(
                project_id=project_id,
                filename=safe_filename,
                file_path=file_path,
                gps_data=gps_extraction["gps_data"],
                description=description,
                date_prise=date_prise,
                metadata_exif=gps_extraction["metadata"]
            )
            
            return {
                "photo_id": photo_id,
                "filename": safe_filename,
                "status": "uploaded_with_gps",
                "gps_data": gps_extraction["gps_data"],
                "metadata": gps_extraction["metadata"],
                "message": "Photo uploadée avec succès et GPS extrait"
            }
            
        except Exception as e:
            logger.error(f"Erreur upload photo: {e}")
            return {"error": str(e)}
    
    def calculate_plan_coordinates(self, photo_id: int, 
                                 plan_bounds: Dict) -> Optional[Tuple[float, float]]:
        """Calcule les coordonnées sur le plan principal depuis GPS"""
        try:
            # Récupérer photo
            with db_manager.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT gps_latitude, gps_longitude FROM photos_geolocated WHERE id = ?",
                    (photo_id,)
                )
                row = cursor.fetchone()
                
                if not row or not (row[0] and row[1]):
                    return None
                
                photo_lat, photo_lon = row[0], row[1]
            
            # Convertir GPS vers coordonnées plan
            # Formule de projection simple (à améliorer selon le plan)
            plan_x = self._map_coordinate(
                photo_lon,
                plan_bounds["lon_min"], plan_bounds["lon_max"],
                plan_bounds["x_min"], plan_bounds["x_max"]
            )
            
            plan_y = self._map_coordinate(
                photo_lat,
                plan_bounds["lat_min"], plan_bounds["lat_max"],
                plan_bounds["y_min"], plan_bounds["y_max"]
            )
            
            # Mettre à jour en base
            db_manager.update_photo_plan_coordinates(photo_id, plan_x, plan_y)
            
            return (plan_x, plan_y)
            
        except Exception as e:
            logger.error(f"Erreur calcul coordonnées plan: {e}")
            return None
    
    def _map_coordinate(self, value: float, 
                       src_min: float, src_max: float,
                       dst_min: float, dst_max: float) -> float:
        """Mappe une coordonnée d'un espace vers un autre"""
        return dst_min + (value - src_min) * (dst_max - dst_min) / (src_max - src_min)
    
    def get_project_photos(self, project_id: int, 
                          has_gps: Optional[bool] = None) -> List[Dict]:
        """Récupère les photos d'un projet"""
        try:
            photos = db_manager.get_project_photos(project_id)
            
            if has_gps is not None:
                if has_gps:
                    photos = [p for p in photos if p.get('gps_latitude') and p.get('gps_longitude')]
                else:
                    photos = [p for p in photos if not (p.get('gps_latitude') and p.get('gps_longitude'))]
            
            return photos
        except Exception as e:
            logger.error(f"Erreur récupération photos: {e}")
            return []
    
    def get_photo_markers_for_map(self, project_id: int) -> List[Dict]:
        """Retourne les markers pour affichage carte/plan"""
        try:
            photos = self.get_project_photos(project_id, has_gps=True)
            
            markers = []
            for photo in photos:
                if photo.get('gps_latitude') and photo.get('gps_longitude'):
                    markers.append({
                        "id": photo['id'],
                        "filename": photo['filename'],
                        "description": photo['description'],
                        "lat": photo['gps_latitude'],
                        "lon": photo['gps_longitude'],
                        "plan_x": photo.get('plan_x_coordinate'),
                        "plan_y": photo.get('plan_y_coordinate'),
                        "date_prise": photo.get('date_prise'),
                        "file_path": photo['file_path']
                    })
            
            return markers
        except Exception as e:
            logger.error(f"Erreur markers carte: {e}")
            return []
    
    def delete_photo(self, photo_id: int) -> Dict:
        """Supprime une photo"""
        try:
            # Récupérer infos photo
            with db_manager.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT file_path FROM photos_geolocated WHERE id = ?",
                    (photo_id,)
                )
                row = cursor.fetchone()
                
                if not row:
                    return {"error": "Photo non trouvée"}
                
                file_path = row[0]
                
                # Supprimer fichier physique
                if os.path.exists(file_path):
                    os.remove(file_path)
                
                # Supprimer de la base
                conn.execute("DELETE FROM photos_geolocated WHERE id = ?", (photo_id,))
                
                return {"status": "deleted", "photo_id": photo_id}
                
        except Exception as e:
            logger.error(f"Erreur suppression photo: {e}")
            return {"error": str(e)}

# Instance globale
photo_gps_system = PhotoGPSSystem()

if __name__ == "__main__":
    # Test du système
    system = PhotoGPSSystem()
    print("📸 Système photos GPS initialisé")
    
    # Test extraction GPS sur image de test
    # (nécessite une image avec GPS pour test complet)