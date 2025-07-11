#!/usr/bin/env python3
"""
Gemini Integration pour PGI-IA
Utilise Google AI Studio API (gratuit)
"""

import os
import json
import requests
from typing import List, Dict, Optional
import google.generativeai as genai

class GeminiManager:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise Gemini avec une clé API
        Obtenir une clé gratuite : https://makersuite.google.com/app/apikey
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        
        if self.api_key and self.api_key.startswith('AIza'):
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("✅ Gemini configuré avec succès")
        else:
            print("⚠️ Clé API Gemini non configurée")
            print("👉 Obtiens une clé gratuite : https://makersuite.google.com/app/apikey")
            self.model = None
    
    def chat(self, prompt: str) -> str:
        """Chat simple avec Gemini"""
        if not self.model:
            return "❌ Gemini non configuré. Configure GEMINI_API_KEY"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Erreur Gemini : {str(e)}"
    
    def analyze_pdf_content(self, text: str) -> Dict:
        """Analyse un contenu PDF pour extraction électrique"""
        if not self.model:
            return {"error": "Gemini non configuré"}
        
        prompt = f"""
        Analyse ce document électrique et extrais :
        1. Type de document (plan, devis, etc.)
        2. Références projet
        3. Éléments électriques (tableaux, circuits, etc.)
        4. Quantités et spécifications
        
        Document :
        {text[:3000]}  # Limite pour l'API gratuite
        
        Réponds en JSON structuré.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Tenter de parser le JSON
            try:
                return json.loads(response.text)
            except:
                return {"raw_response": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def generate_code(self, description: str, language: str = "python") -> str:
        """Génération de code avec Gemini"""
        if not self.model:
            return "# ❌ Gemini non configuré"
        
        prompt = f"""
        Génère du code {language} pour : {description}
        
        Inclus :
        - Commentaires explicatifs
        - Gestion d'erreurs
        - Code optimisé et lisible
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"# ❌ Erreur : {str(e)}"
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Analyse multiple de documents"""
        results = []
        for i, text in enumerate(texts):
            print(f"🔄 Analyse {i+1}/{len(texts)}...")
            result = self.analyze_pdf_content(text)
            results.append(result)
        return results


# Script de test
if __name__ == "__main__":
    print("🤖 Gemini Manager pour PGI-IA")
    print("=" * 50)
    
    # Initialiser
    gemini = GeminiManager()
    
    if gemini.model:
        # Test simple
        print("\n🧪 Test de chat...")
        response = gemini.chat("Explique brièvement ce qu'est un tableau électrique")
        print(f"Réponse : {response[:200]}...")
        
        # Test génération de code
        print("\n💻 Test génération de code...")
        code = gemini.generate_code("fonction pour calculer la puissance électrique P=UI")
        print(code[:300])
    else:
        print("\n📋 Pour configurer Gemini :")
        print("1. Va sur https://makersuite.google.com/app/apikey")
        print("2. Crée une clé API (gratuite)")
        print("3. Configure : export GEMINI_API_KEY='AIza...'")
