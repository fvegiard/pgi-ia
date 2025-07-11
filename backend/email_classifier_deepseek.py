"""
Email Classifier avec DeepSeek pour PGI-IA
Spécialisé dans la classification d'emails du domaine électrique
"""
import json
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import re

class EmailClassifierDeepSeek:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.model = "deepseek-chat"
        
        # Prompt système spécialisé électricité
        self.system_prompt = """Tu es un assistant IA spécialisé dans la gestion de projets électriques pour DR Électrique.
        
Ton rôle est de classifier et analyser les emails selon ces catégories:
1. DIRECTIVE - Instructions de changement (CD, CO-ME, PCE)
2. PLAN - Plans électriques, schémas, dessins techniques
3. CHANGEMENT - Demandes de modification, addenda
4. QUESTION - Questions techniques, clarifications
5. INFORMATION - Confirmations, mises à jour, autres

Pour chaque email, tu dois extraire:
- Type (une des 5 catégories)
- Projet (identifier S-1086 Kahnawake ou C-24-048 Alexis-Nihon)
- Priorité (haute/normale/basse)
- Numéro de directive si applicable (ex: CD-203, CO-ME-039)
- Actions suggérées
- Entités importantes (montants, dates, équipements)
- Confidence score (0-100)

Réponds UNIQUEMENT en JSON valide."""

    def classify_email(self, email_data: Dict) -> Dict:
        """
        Classifie un email et extrait les informations importantes
        
        Args:
            email_data: Dict avec 'subject', 'from', 'body', 'attachments'
            
        Returns:
            Dict avec classification et métadonnées
        """
        # Construire le prompt
        email_text = f"""
Email à analyser:
De: {email_data.get('from', 'Inconnu')}
Sujet: {email_data.get('subject', 'Sans sujet')}
Corps: {email_data.get('body', '')}
Pièces jointes: {', '.join(email_data.get('attachments', [])) or 'Aucune'}
"""

        try:
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": email_text}
                    ],
                    "temperature": 0.3,  # Plus déterministe
                    "max_tokens": 500
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                try:
                    # Essayer de parser le JSON de la réponse
                    content = result['choices'][0]['message']['content']
                    # Nettoyer le contenu (enlever les backticks si présents)
                    content = content.strip()
                    if content.startswith('```json'):
                        content = content[7:]
                    if content.startswith('```'):
                        content = content[3:]
                    if content.endswith('```'):
                        content = content[:-3]
                    content = content.strip()
                    
                    classification = json.loads(content)
                    
                    # Normaliser les clés (DeepSeek peut retourner en français)
                    normalized = {
                        "type": classification.get("Type", classification.get("type", "UNKNOWN")),
                        "project": self._extract_project_id(classification.get("Projet", classification.get("project", ""))),
                        "priority": classification.get("Priorité", classification.get("priority", "normale")).lower(),
                        "directive_number": classification.get("Numéro de directive", classification.get("directive_number")),
                        "confidence": classification.get("Confidence score", classification.get("confidence", 0)),
                        "entities": classification.get("Entités importantes", classification.get("entities", {})),
                        "suggested_actions": classification.get("Actions suggérées", classification.get("suggested_actions", []))
                    }
                    
                    # Ajouter des métadonnées
                    normalized['processed_at'] = datetime.now().isoformat()
                    normalized['api_response_time'] = response.elapsed.total_seconds()
                    
                    return normalized
                except json.JSONDecodeError as e:
                    print(f"Erreur parsing JSON: {e}")
                    print(f"Contenu brut: {result['choices'][0]['message']['content']}")
                    return {
                        "error": f"JSON parsing error: {str(e)}",
                        "raw_response": result['choices'][0]['message']['content'],
                        "type": "UNKNOWN",
                        "confidence": 0
                    }
            else:
                return {
                    "error": f"API Error: {response.status_code}",
                    "type": "UNKNOWN",
                    "confidence": 0
                }
                
        except Exception as e:
            return {
                "error": str(e),
                "type": "UNKNOWN", 
                "confidence": 0
            }
    
    def _extract_project_id(self, project_str: str) -> str:
        """Extrait l'ID du projet depuis une chaîne"""
        if 'S-1086' in project_str:
            return 'S-1086'
        elif 'C-24-048' in project_str:
            return 'C-24-048'
        return project_str
    
    def extract_directive_number(self, text: str) -> Optional[str]:
        """Extrait le numéro de directive du texte"""
        patterns = [
            r'(CD-\d+)',
            r'(CO-ME-\d+)',
            r'(PCE-\d+)',
            r'(DCE-\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).upper()
        return None
    
    def detect_project(self, text: str) -> Optional[str]:
        """Détecte le projet mentionné dans l'email"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in ['kahnawake', 's-1086', 'musée']):
            return "S-1086"
        elif any(term in text_lower for term in ['alexis', 'nihon', 'c-24-048', 'place']):
            return "C-24-048"
        
        return None
    
    def suggest_actions(self, classification: Dict) -> List[Dict]:
        """Suggère des actions basées sur la classification"""
        actions = []
        email_type = classification.get('type', '').upper()
        
        if email_type == 'DIRECTIVE':
            actions.extend([
                {"action": "create_directive", "label": "Créer entrée directive"},
                {"action": "calculate_impact", "label": "Calculer impact financier"},
                {"action": "notify_team", "label": "Notifier équipe projet"}
            ])
        elif email_type == 'PLAN':
            actions.extend([
                {"action": "analyze_pdf", "label": "Analyser avec OCR"},
                {"action": "extract_data", "label": "Extraire données techniques"},
                {"action": "compare_versions", "label": "Comparer avec version précédente"}
            ])
        elif email_type == 'QUESTION':
            actions.extend([
                {"action": "suggest_response", "label": "Suggérer réponse"},
                {"action": "search_similar", "label": "Chercher questions similaires"}
            ])
        elif email_type == 'CHANGEMENT':
            actions.extend([
                {"action": "create_change_order", "label": "Créer ordre de changement"},
                {"action": "estimate_cost", "label": "Estimer coût"}
            ])
            
        return actions
    
    def process_batch(self, emails: List[Dict]) -> List[Dict]:
        """Traite plusieurs emails en batch"""
        results = []
        for email in emails:
            classification = self.classify_email(email)
            classification['suggested_actions'] = self.suggest_actions(classification)
            results.append(classification)
        return results

# Exemple d'utilisation
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv('DEEPSEEK_API_KEY')
    
    classifier = EmailClassifierDeepSeek(api_key)
    
    # Test avec un email exemple
    test_email = {
        "from": "architecte@xyz.com",
        "subject": "⚡ Directive CD-203 - Modification urgente éclairage",
        "body": """Bonjour,

Suite à notre réunion de ce matin concernant le projet Kahnawake, voici la directive 
pour modifier le système d'éclairage du hall principal.

Les luminaires sur rail doivent être repositionnés pour éviter les cloisons de verre.
Impact estimé: 8,500$ en main d'œuvre supplémentaire.

Merci de procéder rapidement.
""",
        "attachments": ["CD-203_eclairage.pdf"]
    }
    
    print("🔍 Classification de l'email de test...")
    result = classifier.classify_email(test_email)
    print(json.dumps(result, indent=2, ensure_ascii=False))