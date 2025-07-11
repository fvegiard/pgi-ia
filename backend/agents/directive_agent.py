"""
Agent de Suivi des Directives
Extrait les informations des PDFs de directives et met à jour les tableaux
"""

import re
import logging
from typing import Dict, Optional, List
from datetime import datetime
from pathlib import Path
import PyPDF2
import json

logger = logging.getLogger(__name__)

class DirectiveAgent:
    """
    Agent spécialisé dans le traitement des directives de changement
    
    Capacités:
    - Extraction d'informations depuis PDF
    - Identification des patterns de directives
    - Mise à jour automatique des tableaux de suivi
    """
    
    def __init__(self):
        self.patterns = {
            'numero': [
                r'CO-ME-(\d+)',
                r'CD\s+A(\d+)',
                r'PCE-(\d+)',
                r'Directive\s+#?(\d+)'
            ],
            'date': [
                r'(\d{4}-\d{2}-\d{2})',
                r'(\d{2}/\d{2}/\d{4})',
                r'(\d{1,2}\s+\w+\s+\d{4})'
            ],
            'prix': [
                r'\$\s?([\d,]+\.?\d*)',
                r'([\d,]+\.?\d*)\s?\$',
                r'Prix\s*:\s*([\d,]+\.?\d*)'
            ]
        }
        
        self.status_keywords = {
            'à_preparer': ['à préparer', 'en attente', 'pending'],
            'soumis': ['soumis', 'submitted', 'envoyé'],
            'approuve': ['approuvé', 'approved', 'accepté'],
            'sans_frais': ['sans frais', 'no charge', 'aucun coût']
        }
    
    async def process_directive(self, file_path: Path) -> Dict:
        """
        Traite un fichier de directive et extrait les informations
        
        Args:
            file_path: Chemin vers le fichier PDF
            
        Returns:
            Dict contenant les informations extraites
        """
        logger.info(f"🔍 Traitement de la directive: {file_path.name}")
        
        try:
            # Extraction du texte
            text = self._extract_pdf_text(file_path)
            
            # Extraction des informations
            result = {
                'filename': file_path.name,
                'numero': self._extract_numero(text, file_path.name),
                'date': self._extract_date(text),
                'description': self._extract_description(text),
                'prix': self._extract_prix(text),
                'status': self._determine_status(text),
                'extracted_at': datetime.now().isoformat()
            }
            
            # Validation
            if not result['numero']:
                logger.warning(f"⚠️ Numéro de directive non trouvé dans {file_path.name}")
            
            logger.info(f"✅ Directive {result['numero']} extraite avec succès")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du traitement: {str(e)}")
            raise
    
    def _extract_pdf_text(self, file_path: Path) -> str:
        """Extrait le texte d'un fichier PDF"""
        text = ""
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
        
        return text
    
    def _extract_numero(self, text: str, filename: str) -> Optional[str]:
        """Extrait le numéro de directive"""
        # D'abord essayer dans le texte
        for pattern in self.patterns['numero']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        # Si pas trouvé, essayer dans le nom du fichier
        for pattern in self.patterns['numero']:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_date(self, text: str) -> Optional[str]:
        """Extrait la date de la directive"""
        for pattern in self.patterns['date']:
            match = re.search(pattern, text)
            if match:
                date_str = match.group(0)
                # Normaliser au format ISO
                try:
                    # Tentative de parsing
                    if '/' in date_str:
                        parts = date_str.split('/')
                        if len(parts[2]) == 2:
                            parts[2] = '20' + parts[2]
                        return f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
                    return date_str
                except:
                    return date_str
        
        return None
    
    def _extract_prix(self, text: str) -> float:
        """Extrait le prix de la directive"""
        for pattern in self.patterns['prix']:
            match = re.search(pattern, text)
            if match:
                prix_str = match.group(1).replace(',', '').replace(' ', '')
                try:
                    return float(prix_str)
                except ValueError:
                    continue
        
        return 0.0
    
    def _extract_description(self, text: str) -> str:
        """Extrait la description de la directive"""
        # Chercher des patterns communs
        desc_patterns = [
            r'Description\s*:\s*([^\n]+)',
            r'Objet\s*:\s*([^\n]+)',
            r'Subject\s*:\s*([^\n]+)',
            r'RE\s*:\s*([^\n]+)'
        ]
        
        for pattern in desc_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Si pas trouvé, prendre les premières lignes significatives
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        for line in lines[:10]:  # Chercher dans les 10 premières lignes
            if len(line) > 20 and not any(p in line for p in ['Date:', 'No:', 'Page']):
                return line[:200]  # Limiter à 200 caractères
        
        return "Description à extraire manuellement"
    
    def _determine_status(self, text: str) -> str:
        """Détermine le statut de la directive"""
        text_lower = text.lower()
        
        for status, keywords in self.status_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return status.replace('_', ' ').title()
        
        return "À préparer"  # Statut par défaut
    
    async def update_tracking_table(self, project_id: str, directive_data: Dict):
        """
        Met à jour le tableau de suivi avec les données extraites
        
        Args:
            project_id: Identifiant du projet
            directive_data: Données de la directive extraites
        """
        # TODO: Implémenter la mise à jour en base de données
        logger.info(f"📊 Mise à jour du tableau de suivi pour {project_id}")
        logger.info(f"   Directive: {directive_data['numero']}")
        
        # Pour l'instant, sauvegarder dans un fichier JSON
        tracking_file = Path(f"data/tracking_{project_id}.json")
        tracking_file.parent.mkdir(exist_ok=True)
        
        # Charger les données existantes
        if tracking_file.exists():
            with open(tracking_file, 'r') as f:
                tracking_data = json.load(f)
        else:
            tracking_data = []
        
        # Ajouter ou mettre à jour
        existing = next((d for d in tracking_data if d['numero'] == directive_data['numero']), None)
        if existing:
            existing.update(directive_data)
        else:
            tracking_data.append(directive_data)
        
        # Sauvegarder
        with open(tracking_file, 'w') as f:
            json.dump(tracking_data, f, indent=2, ensure_ascii=False)
        
        logger.info("✅ Tableau de suivi mis à jour")


# Instance singleton
directive_agent = DirectiveAgent()