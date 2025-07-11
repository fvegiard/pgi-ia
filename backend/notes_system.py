"""
Système Notes Intelligentes PGI-IA
Workflow: Note utilisateur → IA reformulation → Approbation → Stockage
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
from database_manager import db_manager
import logging

logger = logging.getLogger(__name__)

class NotesSystem:
    """Système de notes intelligentes par projet"""
    
    def __init__(self):
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"
    
    def create_note(self, project_id: int, note_originale: str, 
                   categorie: str = "Général") -> Dict:
        """Crée une nouvelle note et lance la reformulation IA"""
        try:
            # Créer la note en base
            note_id = db_manager.create_note(
                project_id=project_id,
                note_originale=note_originale,
                categorie=categorie,
                metadata={"status": "processing"}
            )
            
            # Lancer reformulation IA asynchrone
            note_reformulee = self.reformulate_with_ai(note_originale, categorie)
            
            if note_reformulee:
                db_manager.update_note_reformulated(note_id, note_reformulee)
                
            return {
                "note_id": note_id,
                "status": "reformulated" if note_reformulee else "draft",
                "note_originale": note_originale,
                "note_reformulee": note_reformulee
            }
            
        except Exception as e:
            logger.error(f"Erreur création note: {e}")
            return {"error": str(e)}
    
    def reformulate_with_ai(self, note_originale: str, categorie: str) -> Optional[str]:
        """Reformule une note avec l'IA DeepSeek"""
        if not self.deepseek_api_key:
            logger.warning("Clé DeepSeek manquante - reformulation ignorée")
            return None
        
        try:
            prompt = self._build_reformulation_prompt(note_originale, categorie)
            
            response = requests.post(
                self.deepseek_url,
                headers={
                    "Authorization": f"Bearer {self.deepseek_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": self._get_system_prompt()},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                logger.error(f"Erreur API DeepSeek: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur reformulation IA: {e}")
            return None
    
    def _get_system_prompt(self) -> str:
        """Prompt système pour l'IA de reformulation"""
        return """Tu es un assistant spécialisé en gestion de projets électriques industriels.
        
Ton rôle est de reformuler les notes de chantier pour les rendre:
- Plus claires et professionnelles
- Structurées et organisées  
- Adaptées au contexte électrique industriel
- Prêtes pour archivage et référence future

Reformule en gardant:
- Toutes les informations techniques importantes
- Les dates, mesures, et références
- Le contexte du projet électrique
- Un ton professionnel mais accessible

Format de sortie souhaité:
**[Catégorie]**: [Titre court]
**Date**: [Si mentionnée]
**Description**: [Description reformulée]
**Points techniques**: [Liste si applicable]
**Actions requises**: [Si applicable]"""

    def _build_reformulation_prompt(self, note_originale: str, categorie: str) -> str:
        """Construit le prompt de reformulation"""
        return f"""Reformule cette note de projet électrique:

**Catégorie**: {categorie}
**Note originale**: {note_originale}

Reformule cette note pour qu'elle soit professionnelle, claire et bien structurée. 
Garde toutes les informations importantes et adapte au contexte électrique industriel."""

    def approve_note(self, note_id: int, note_finale: str) -> Dict:
        """Approuve une note et la finalise"""
        try:
            db_manager.approve_note(note_id, note_finale)
            return {
                "status": "approved",
                "note_id": note_id,
                "message": "Note approuvée et finalisée"
            }
        except Exception as e:
            logger.error(f"Erreur approbation note: {e}")
            return {"error": str(e)}
    
    def get_project_notes(self, project_id: int, 
                         statut: Optional[str] = None) -> List[Dict]:
        """Récupère les notes d'un projet"""
        try:
            notes = db_manager.get_project_notes(project_id)
            
            if statut:
                notes = [n for n in notes if n.get('statut') == statut]
            
            return notes
        except Exception as e:
            logger.error(f"Erreur récupération notes: {e}")
            return []
    
    def get_pending_notes(self, project_id: Optional[int] = None) -> List[Dict]:
        """Récupère les notes en attente d'approbation"""
        try:
            if project_id:
                return self.get_project_notes(project_id, 'reformulated')
            else:
                # Toutes les notes en attente
                with db_manager.get_connection() as conn:
                    cursor = conn.execute("""
                        SELECT n.*, p.nom as project_nom, p.code as project_code
                        FROM project_notes n
                        JOIN projects p ON n.project_id = p.id
                        WHERE n.statut = 'reformulated'
                        ORDER BY n.date_creation DESC
                    """)
                    return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Erreur notes en attente: {e}")
            return []
    
    def search_notes(self, project_id: int, query: str) -> List[Dict]:
        """Recherche dans les notes d'un projet"""
        try:
            with db_manager.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT * FROM project_notes 
                    WHERE project_id = ? AND (
                        note_originale LIKE ? OR 
                        note_reformulee LIKE ? OR 
                        note_finale LIKE ?
                    )
                    ORDER BY date_creation DESC
                """, (project_id, f"%{query}%", f"%{query}%", f"%{query}%"))
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Erreur recherche notes: {e}")
            return []
    
    def get_notes_stats(self, project_id: Optional[int] = None) -> Dict:
        """Statistiques des notes"""
        try:
            with db_manager.get_connection() as conn:
                where_clause = "WHERE project_id = ?" if project_id else ""
                params = (project_id,) if project_id else ()
                
                cursor = conn.execute(f"""
                    SELECT 
                        statut,
                        COUNT(*) as count
                    FROM project_notes 
                    {where_clause}
                    GROUP BY statut
                """, params)
                
                stats = {row['statut']: row['count'] for row in cursor.fetchall()}
                stats['total'] = sum(stats.values())
                return stats
        except Exception as e:
            logger.error(f"Erreur stats notes: {e}")
            return {}

# Instance globale
notes_system = NotesSystem()

if __name__ == "__main__":
    # Test du système
    notes = NotesSystem()
    
    # Test création note
    result = notes.create_note(
        project_id=1,
        note_originale="Problème avec les conduits électriques au 2e étage. Voir avec l'équipe demain matin.",
        categorie="Technique"
    )
    print("Test création note:", result)
    
    # Test récupération notes
    project_notes = notes.get_project_notes(1)
    print(f"Notes projet 1: {len(project_notes)}")
    
    # Stats
    stats = notes.get_notes_stats(1)
    print("Stats notes:", stats)