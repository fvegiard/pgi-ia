"""
Orchestrateur Principal - Léna
Le cerveau du système qui identifie et délègue aux agents appropriés
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum
import asyncio
import mimetypes

from agents.directive_agent import directive_agent

logger = logging.getLogger(__name__)

class FileType(Enum):
    """Types de fichiers supportés"""
    DIRECTIVE = "directive"
    PLAN = "plan"
    PHOTO = "photo"
    EMAIL = "email"
    DEVIS = "devis"
    UNKNOWN = "unknown"

class Orchestrator:
    """
    Orchestrateur principal du système PGI-IA
    
    Rôle: Analyser les entrées et déléguer aux agents spécialisés
    """
    
    def __init__(self):
        self.agents = {
            FileType.DIRECTIVE: directive_agent,
            # FileType.PLAN: plan_agent,  # À implémenter
            # FileType.PHOTO: photo_agent,  # À implémenter
            # FileType.EMAIL: email_agent,  # À implémenter
            # FileType.DEVIS: estimation_agent,  # À implémenter
        }
        
        self.file_patterns = {
            FileType.DIRECTIVE: [
                r'CO-ME-\d+',
                r'CD\s+A\d+',
                r'PCE-\d+',
                r'directive',
                r'changement'
            ],
            FileType.PLAN: [
                r'E-\d{3}',
                r'plan',
                r'drawing',
                r'\.dwg$',
                r'rev[a-z]'
            ],
            FileType.PHOTO: [
                r'\.jpg$',
                r'\.jpeg$',
                r'\.png$',
                r'IMG_\d+'
            ],
            FileType.EMAIL: [
                r'\.eml$',
                r'\.msg$',
                r'RFI',
                r'RE:'
            ],
            FileType.DEVIS: [
                r'devis',
                r'soumission',
                r'quote',
                r'estimation'
            ]
        }
        
        logger.info("🧠 Orchestrateur Léna initialisé")
    
    async def process_file(self, file_path: Path, project_id: str) -> Dict[str, Any]:
        """
        Traite un fichier uploadé en le déléguant au bon agent
        
        Args:
            file_path: Chemin vers le fichier
            project_id: ID du projet concerné
            
        Returns:
            Résultat du traitement
        """
        logger.info(f"🎯 Nouveau fichier reçu: {file_path.name}")
        
        try:
            # 1. Identifier le type de fichier
            file_type = self._identify_file_type(file_path)
            logger.info(f"📁 Type identifié: {file_type.value}")
            
            # 2. Vérifier si on a un agent pour ce type
            if file_type not in self.agents:
                logger.warning(f"⚠️ Pas d'agent disponible pour le type: {file_type.value}")
                return {
                    "status": "pending",
                    "message": f"Type {file_type.value} identifié mais agent en développement",
                    "file_type": file_type.value
                }
            
            # 3. Déléguer à l'agent approprié
            agent = self.agents[file_type]
            result = await agent.process_directive(file_path)
            
            # 4. Mettre à jour la base de données
            if file_type == FileType.DIRECTIVE:
                await agent.update_tracking_table(project_id, result)
            
            # 5. Créer événement pour la timeline
            timeline_event = self._create_timeline_event(file_type, result)
            
            return {
                "status": "success",
                "file_type": file_type.value,
                "data": result,
                "timeline_event": timeline_event
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur orchestrateur: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _identify_file_type(self, file_path: Path) -> FileType:
        """
        Identifie le type de fichier basé sur:
        - Le nom du fichier
        - L'extension
        - Le contenu (si nécessaire)
        """
        filename = file_path.name.lower()
        
        # Vérifier chaque type via patterns
        for file_type, patterns in self.file_patterns.items():
            for pattern in patterns:
                import re
                if re.search(pattern, filename, re.IGNORECASE):
                    return file_type
        
        # Vérification par mimetype
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type:
            if mime_type.startswith('image'):
                return FileType.PHOTO
            elif mime_type == 'message/rfc822':
                return FileType.EMAIL
        
        # Si on ne peut pas identifier, retourner UNKNOWN
        return FileType.UNKNOWN
    
    def _create_timeline_event(self, file_type: FileType, data: Dict) -> Dict:
        """Crée un événement pour la timeline du projet"""
        
        icons = {
            FileType.DIRECTIVE: "file-signature",
            FileType.PLAN: "drafting-compass",
            FileType.PHOTO: "camera",
            FileType.EMAIL: "envelope",
            FileType.DEVIS: "calculator"
        }
        
        titles = {
            FileType.DIRECTIVE: f"Directive {data.get('numero', 'N/A')} traitée",
            FileType.PLAN: "Plan analysé et converti en 3D",
            FileType.PHOTO: "Photo de chantier géolocalisée",
            FileType.EMAIL: "Communication analysée",
            FileType.DEVIS: "Devis analysé"
        }
        
        return {
            "type": file_type.value,
            "icon": icons.get(file_type, "file"),
            "title": titles.get(file_type, "Fichier traité"),
            "description": data.get('description', 'Traitement terminé'),
            "data": data,
            "timestamp": data.get('extracted_at')
        }
    
    async def analyze_project_status(self, project_id: str) -> Dict:
        """
        Analyse globale du statut d'un projet
        Utilise tous les agents pour compiler un rapport
        """
        logger.info(f"📊 Analyse globale du projet {project_id}")
        
        # TODO: Implémenter l'analyse croisée
        # - Vérifier cohérence directives vs plans
        # - Détecter conflits potentiels
        # - Calculer métriques de progression
        
        return {
            "project_id": project_id,
            "status": "analysis_pending",
            "message": "Fonctionnalité en développement"
        }


# Instance singleton
orchestrator = Orchestrator()