#!/usr/bin/env python3
'''
Déploiement PGI-IA avec modèle DeepSeek entraîné
'''

import os
from openai import OpenAI

# Configuration production
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
MODEL_ID = "pgi-ia-quebec-electrical-v1"  # À remplacer par ID réel après training

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

def query_pgi_ia(question, project_context=None):
    '''Interroger PGI-IA'''
    
    system_prompt = '''Tu es PGI-IA, l'assistant intelligent de gestion de projets électriques 
    pour DR Électrique Inc. Tu connais les normes québécoises, les procédures CCQ, et tu gères 
    les projets de construction électrique. Pour toute question de sécurité, tu rediriges vers 
    les ressources officielles CNESST.'''
    
    if project_context:
        system_prompt += f"\n\nContexte projet actuel: {project_context}"
    
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Erreur PGI-IA: {str(e)}"

# Exemples d'utilisation
if __name__ == "__main__":
    print("🤖 PGI-IA PRÊT!")
    
    # Test 1: Gestion directive
    print("\n📋 Test Directive:")
    response = query_pgi_ia(
        "J'ai reçu la directive PCE-47 pour Kahnawake, comment procéder?",
        "C24-060 - Centre Culturel Kahnawake"
    )
    print(response)
    
    # Test 2: Question CCQ
    print("\n👷 Test CCQ:")
    response = query_pgi_ia("Quel est le ratio compagnon/apprenti pour un chantier commercial?")
    print(response)
    
    # Test 3: Sécurité (doit rediriger)
    print("\n⚠️ Test Sécurité:")
    response = query_pgi_ia("Comment faire le cadenassage d'un panneau 600V?")
    print(response)
