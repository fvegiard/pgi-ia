"""
Service d'orchestration principal PGI-IA
Gère DeepSeek, Gemini et Ollama local
"""
import os
import requests
import json
from typing import Dict, Any, List
import google.generativeai as genai
from datetime import datetime

class PGIOrchestrator:
    def __init__(self):
        # Configuration APIs
        self.deepseek_key = os.getenv('DEEPSEEK_API_KEY')
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        
        # Configuration Gemini
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        
        # Endpoints
        self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # État du système
        self.active_projects = {
            "kahnawake": {
                "name": "Kahnawake Station",
                "status": "active",
                "pdf_count": 300,
                "processed": 0
            },
            "alexis_nihon": {
                "name": "Alexis-Nihon",
                "status": "active",
                "directives": []
            }
        }
    
    def process_with_deepseek(self, prompt: str) -> str:
        """Traite avec DeepSeek API"""
        if not self.deepseek_key:
            return self._mock_response("DeepSeek", prompt)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.deepseek_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Tu es un expert en gestion électrique industrielle."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            
            response = requests.post(self.deepseek_url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"Erreur DeepSeek: {response.status_code}"
                
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    def process_with_gemini(self, prompt: str) -> str:
        """Traite avec Gemini API"""
        if not self.gemini_key:
            return self._mock_response("Gemini", prompt)
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erreur Gemini: {str(e)}"
    
    def process_with_ollama(self, prompt: str, model: str = "llama3") -> str:
        """Traite avec Ollama local"""
        try:
            data = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(self.ollama_url, json=data)
            if response.status_code == 200:
                return response.json()['response']
            else:
                return self._mock_response("Ollama", prompt)
                
        except:
            return self._mock_response("Ollama", prompt)
    
    def _mock_response(self, agent: str, prompt: str) -> str:
        """Réponse simulée quand l'API n'est pas disponible"""
        return f"[{agent} - Mode simulation] Traitement de: {prompt[:50]}..."
    
    def process_directive(self, file_path: str) -> Dict[str, Any]:
        """Traite une directive avec l'IA appropriée"""
        # Extraction du texte (simulé pour le moment)
        content = f"Contenu extrait de {file_path}"
        
        # Analyse avec DeepSeek
        analysis = self.process_with_deepseek(
            f"Analyse cette directive électrique: {content}"
        )
        
        # Validation avec Gemini
        validation = self.process_with_gemini(
            f"Valide cette analyse: {analysis}"
        )
        
        return {
            "file": file_path,
            "analysis": analysis,
            "validation": validation,
            "timestamp": datetime.now().isoformat(),
            "status": "processed"
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Retourne l'état complet du système"""
        return {
            "orchestrator": "PGI-IA v4.1",
            "apis": {
                "deepseek": bool(self.deepseek_key),
                "gemini": bool(self.gemini_key),
                "ollama": self._check_ollama()
            },
            "projects": self.active_projects,
            "timestamp": datetime.now().isoformat()
        }
    
    def _check_ollama(self) -> bool:
        """Vérifie si Ollama est actif"""
        try:
            response = requests.get("http://localhost:11434/api/version", timeout=2)
            return response.status_code == 200
        except:
            return False

# Instance globale
orchestrator = PGIOrchestrator()
