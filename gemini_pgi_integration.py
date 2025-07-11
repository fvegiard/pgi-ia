#!/usr/bin/env python3
"""
Intégration Gemini avec PGI-IA
Fonctionnalités spécifiques pour l'électricité industrielle
"""

import os
import json
from typing import List, Dict
from gemini_manager import GeminiManager
import PyPDF2
import glob

class GeminiPGIIntegration:
    def __init__(self):
        self.gemini = GeminiManager()
        self.templates = {
            "kahnawake": "Analyse pour projet S-1086 Musée Kahnawake",
            "alexis_nihon": "Analyse pour projet C-24-048 Place Alexis-Nihon"
        }
    
    def analyze_electrical_plan(self, pdf_path: str) -> Dict:
        """Analyse un plan électrique PDF avec Gemini"""
        if not self.gemini.model:
            return {"error": "Gemini non configuré"}
        
        print(f"📄 Analyse de {pdf_path}...")
        
        try:
            # Extraire texte du PDF
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages[:5]:  # Limiter aux 5 premières pages
                    text += page.extract_text()
            
            # Prompt spécialisé électricité
            prompt = f"""
            Tu es un expert en électricité industrielle. Analyse ce plan électrique et extrais :
            
            1. IDENTIFICATION :
               - Type de document (plan, devis, schéma)
               - Numéro de projet
               - Date et révision
            
            2. COMPOSANTS ÉLECTRIQUES :
               - Tableaux de distribution
               - Circuits et leur ampérage
               - Types de protection (disjoncteurs, fusibles)
               - Câblage (types, calibres)
            
            3. SPÉCIFICATIONS :
               - Tension d'alimentation
               - Puissance totale
               - Facteur de charge
            
            4. NORMES :
               - Codes référencés (CSA, NEC)
               - Exigences spéciales
            
            Document :
            {text[:4000]}
            
            Réponds en JSON structuré avec ces catégories.
            """
            
            response = self.gemini.model.generate_content(prompt)
            
            # Parser la réponse
            try:
                result = json.loads(response.text)
            except:
                # Si pas JSON, structurer la réponse
                result = {
                    "analyse_brute": response.text,
                    "status": "parsing_manuel_requis"
                }
            
            result["fichier"] = os.path.basename(pdf_path)
            return result
            
        except Exception as e:
            return {
                "fichier": os.path.basename(pdf_path),
                "error": str(e)
            }
    
    def batch_analyze_plans(self, directory: str) -> List[Dict]:
        """Analyse tous les PDFs d'un dossier"""
        pdf_files = glob.glob(f"{directory}/*.pdf")
        print(f"📁 {len(pdf_files)} PDFs trouvés dans {directory}")
        
        results = []
        for i, pdf in enumerate(pdf_files):
            print(f"\n[{i+1}/{len(pdf_files)}] Analyse en cours...")
            result = self.analyze_electrical_plan(pdf)
            results.append(result)
            
            # Sauvegarder au fur et à mesure
            self.save_results(results, f"{directory}/gemini_analysis.json")
        
        return results
    
    def generate_estimation(self, analysis_results: List[Dict]) -> str:
        """Génère une estimation basée sur les analyses"""
        if not self.gemini.model:
            return "❌ Gemini non configuré"
        
        prompt = f"""
        Basé sur ces analyses de plans électriques, génère une estimation détaillée incluant :
        
        1. RÉSUMÉ DU PROJET
        2. LISTE DES MATÉRIAUX avec quantités
        3. MAIN D'ŒUVRE estimée (heures)
        4. COÛTS APPROXIMATIFS
        5. DÉLAIS DE RÉALISATION
        
        Analyses :
        {json.dumps(analysis_results, indent=2)[:3000]}
        
        Format l'estimation de façon professionnelle.
        """
        
        response = self.gemini.model.generate_content(prompt)
        return response.text
    
    def chat_about_project(self, question: str, context: Dict = None) -> str:
        """Chat interactif sur le projet"""
        if not self.gemini.model:
            return "❌ Gemini non configuré"
        
        context_str = json.dumps(context, indent=2) if context else "Aucun contexte"
        
        prompt = f"""
        Tu es Léa, l'orchestrateur IA spécialisé en électricité industrielle pour PGI-IA.
        
        Contexte du projet :
        {context_str}
        
        Question : {question}
        
        Réponds de façon professionnelle et détaillée.
        """
        
        response = self.gemini.model.generate_content(prompt)
        return response.text
    
    def save_results(self, results: List[Dict], output_path: str):
        """Sauvegarde les résultats d'analyse"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"💾 Résultats sauvegardés : {output_path}")


# Interface en ligne de commande
if __name__ == "__main__":
    import sys
    
    print("🤖 Gemini x PGI-IA - Analyse Électrique")
    print("=" * 50)
    
    integration = GeminiPGIIntegration()
    
    if not integration.gemini.model:
        print("\n❌ Configure d'abord GEMINI_API_KEY")
        print("👉 Lance : ./setup_gemini.sh")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        # Mode ligne de commande
        command = sys.argv[1]
        
        if command == "analyze" and len(sys.argv) > 2:
            pdf_path = sys.argv[2]
            result = integration.analyze_electrical_plan(pdf_path)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif command == "batch" and len(sys.argv) > 2:
            directory = sys.argv[2]
            results = integration.batch_analyze_plans(directory)
            print(f"\n✅ Analyse terminée : {len(results)} fichiers")
        
        elif command == "chat":
            question = " ".join(sys.argv[2:])
            response = integration.chat_about_project(question)
            print(f"\n💬 Léa : {response}")
        
        else:
            print("Usage :")
            print("  python gemini_pgi_integration.py analyze <pdf>")
            print("  python gemini_pgi_integration.py batch <directory>")
            print("  python gemini_pgi_integration.py chat <question>")
    
    else:
        # Mode interactif
        print("\n✅ Gemini connecté et prêt !")
        print("\nCommandes disponibles :")
        print("1. Analyser un PDF")
        print("2. Analyser un dossier complet")
        print("3. Générer une estimation")
        print("4. Chat sur le projet")
        
        choice = input("\nChoix : ")
        
        if choice == "1":
            pdf = input("Chemin du PDF : ")
            result = integration.analyze_electrical_plan(pdf)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif choice == "2":
            directory = input("Dossier des PDFs : ")
            integration.batch_analyze_plans(directory)
        
        elif choice == "3":
            print("📊 Génération d'estimation...")
            # Charger analyses existantes
            json_path = input("Fichier d'analyses JSON : ")
            with open(json_path, 'r') as f:
                analyses = json.load(f)
            estimation = integration.generate_estimation(analyses)
            print(estimation)
        
        elif choice == "4":
            print("💬 Chat avec Léa (Gemini)")
            while True:
                question = input("\nToi : ")
                if question.lower() in ['exit', 'quit']:
                    break
                response = integration.chat_about_project(question)
                print(f"\nLéa : {response}")
