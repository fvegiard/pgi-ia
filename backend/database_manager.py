"""
Database Manager pour PGI-IA - Phase Réaliste
Gestionnaire centralisé pour toutes les opérations base de données
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gestionnaire centralisé base de données PGI-IA"""
    
    def __init__(self, db_path: str = "pgi_ia.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données avec le schéma étendu"""
        try:
            # Lire et exécuter le schéma SQL
            schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                     "database_schema_extended.sql")
            
            if os.path.exists(schema_path):
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schema_sql = f.read()
                
                with sqlite3.connect(self.db_path) as conn:
                    conn.executescript(schema_sql)
                logger.info("✅ Base données initialisée avec schéma étendu")
            else:
                logger.error("❌ Fichier schéma non trouvé")
        except Exception as e:
            logger.error(f"❌ Erreur init database: {e}")
    
    def get_connection(self):
        """Retourne une connexion à la base de données"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Pour accès par nom de colonne
        return conn
    
    # =============================================================================
    # PROJETS
    # =============================================================================
    
    def get_projects(self) -> List[Dict]:
        """Récupère tous les projets avec statistiques"""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM project_overview")
            return [dict(row) for row in cursor.fetchall()]
    
    def get_project(self, project_id: int) -> Optional[Dict]:
        """Récupère un projet spécifique"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM project_overview WHERE id = ?", 
                (project_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def create_project(self, code: str, nom: str, **kwargs) -> int:
        """Crée un nouveau projet"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO projects (code, nom, client, statut, po_client, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                code, nom,
                kwargs.get('client', ''),
                kwargs.get('statut', 'Planification'),
                kwargs.get('po_client', ''),
                json.dumps(kwargs.get('metadata', {}))
            ))
            return cursor.lastrowid
    
    # =============================================================================
    # NOTES INTELLIGENTES
    # =============================================================================
    
    def create_note(self, project_id: int, note_originale: str, **kwargs) -> int:
        """Crée une nouvelle note"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO project_notes 
                (project_id, note_originale, categorie, metadata)
                VALUES (?, ?, ?, ?)
            """, (
                project_id, note_originale,
                kwargs.get('categorie', 'Général'),
                json.dumps(kwargs.get('metadata', {}))
            ))
            return cursor.lastrowid
    
    def update_note_reformulated(self, note_id: int, note_reformulee: str):
        """Met à jour une note avec la version reformulée par IA"""
        with self.get_connection() as conn:
            conn.execute("""
                UPDATE project_notes 
                SET note_reformulee = ?, statut = 'reformulated'
                WHERE id = ?
            """, (note_reformulee, note_id))
    
    def approve_note(self, note_id: int, note_finale: str):
        """Approuve une note et la marque comme finale"""
        with self.get_connection() as conn:
            conn.execute("""
                UPDATE project_notes 
                SET note_finale = ?, statut = 'approved', 
                    date_approbation = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (note_finale, note_id))
    
    def get_project_notes(self, project_id: int) -> List[Dict]:
        """Récupère toutes les notes d'un projet"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM project_notes 
                WHERE project_id = ? 
                ORDER BY date_creation DESC
            """, (project_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    # =============================================================================
    # PHOTOS GÉOLOCALISÉES
    # =============================================================================
    
    def create_photo(self, project_id: int, filename: str, file_path: str, 
                    gps_data: Dict, **kwargs) -> int:
        """Crée une entrée photo avec données GPS"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO photos_geolocated 
                (project_id, filename, file_path, gps_latitude, gps_longitude, 
                 gps_altitude, description, date_prise, metadata_exif)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                project_id, filename, file_path,
                gps_data.get('latitude'),
                gps_data.get('longitude'),
                gps_data.get('altitude'),
                kwargs.get('description', ''),
                kwargs.get('date_prise'),
                json.dumps(kwargs.get('metadata_exif', {}))
            ))
            return cursor.lastrowid
    
    def update_photo_plan_coordinates(self, photo_id: int, plan_x: float, plan_y: float):
        """Met à jour les coordonnées sur le plan principal"""
        with self.get_connection() as conn:
            conn.execute("""
                UPDATE photos_geolocated 
                SET plan_x_coordinate = ?, plan_y_coordinate = ?
                WHERE id = ?
            """, (plan_x, plan_y, photo_id))
    
    def get_project_photos(self, project_id: int) -> List[Dict]:
        """Récupère toutes les photos d'un projet"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM photos_geolocated 
                WHERE project_id = ? 
                ORDER BY date_upload DESC
            """, (project_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    # =============================================================================
    # RÉUNIONS ET TRANSCRIPTIONS
    # =============================================================================
    
    def create_meeting(self, project_id: int, titre: str, date_reunion: datetime,
                      audio_file_path: str, **kwargs) -> int:
        """Crée une nouvelle réunion"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO meetings 
                (project_id, titre, date_reunion, audio_file_path, 
                 duree_minutes, participants)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                project_id, titre, date_reunion, audio_file_path,
                kwargs.get('duree_minutes'),
                json.dumps(kwargs.get('participants', []))
            ))
            return cursor.lastrowid
    
    def update_meeting_transcription(self, meeting_id: int, 
                                   transcription_text: str, summary: str):
        """Met à jour la transcription d'une réunion"""
        with self.get_connection() as conn:
            conn.execute("""
                UPDATE meetings 
                SET transcription_text = ?, transcription_summary = ?, 
                    status = 'transcribed'
                WHERE id = ?
            """, (transcription_text, summary, meeting_id))
    
    def get_project_meetings(self, project_id: int) -> List[Dict]:
        """Récupère toutes les réunions d'un projet"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM meetings 
                WHERE project_id = ? 
                ORDER BY date_reunion DESC
            """, (project_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    # =============================================================================
    # FICHIERS CAD ET PLANS
    # =============================================================================
    
    def create_cad_file(self, project_id: int, filename: str, 
                       original_path: str, file_type: str) -> int:
        """Crée une entrée fichier CAD"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO cad_files 
                (project_id, filename, original_path, file_type)
                VALUES (?, ?, ?, ?)
            """, (project_id, filename, original_path, file_type))
            return cursor.lastrowid
    
    def update_cad_conversion(self, cad_id: int, dwg_path: str, 
                            model_3d_path: str, status: str):
        """Met à jour le statut de conversion CAD"""
        with self.get_connection() as conn:
            conn.execute("""
                UPDATE cad_files 
                SET dwg_path = ?, model_3d_path = ?, 
                    conversion_status = ?, date_conversion = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (dwg_path, model_3d_path, status, cad_id))
    
    # =============================================================================
    # ACTIVITÉ RÉCENTE
    # =============================================================================
    
    def get_recent_activity(self, project_id: Optional[int] = None, 
                          limit: int = 20) -> List[Dict]:
        """Récupère l'activité récente"""
        with self.get_connection() as conn:
            if project_id:
                cursor = conn.execute("""
                    SELECT * FROM recent_activity 
                    WHERE project_id = ? 
                    ORDER BY activity_date DESC 
                    LIMIT ?
                """, (project_id, limit))
            else:
                cursor = conn.execute("""
                    SELECT * FROM recent_activity 
                    ORDER BY activity_date DESC 
                    LIMIT ?
                """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    # =============================================================================
    # UTILITIES
    # =============================================================================
    
    def get_database_stats(self) -> Dict:
        """Retourne les statistiques de la base de données"""
        with self.get_connection() as conn:
            stats = {}
            tables = ['projects', 'meetings', 'project_notes', 
                     'photos_geolocated', 'cad_files', 'cable_paths', 'emails']
            
            for table in tables:
                cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = cursor.fetchone()[0]
            
            return stats

# Instance globale
db_manager = DatabaseManager()

if __name__ == "__main__":
    # Test rapide
    db = DatabaseManager("test_pgi_ia.db")
    stats = db.get_database_stats()
    print("📊 Statistiques DB:", stats)
    
    projects = db.get_projects()
    print("📁 Projets:", len(projects))
    for project in projects:
        print(f"  - {project['code']}: {project['nom']}")