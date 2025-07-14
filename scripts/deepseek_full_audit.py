#!/usr/bin/env python3
"""
Audit complet du dataset par DeepSeek pour IA électricité
"""

import json
import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# Configuration
load_dotenv('/root/dev/pgi-ia/.env')
client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com/v1"
)

def audit_dataset_complete():
    """Audit détaillé par un expert électricien virtuel"""
    
    print("🔍 AUDIT APPROFONDI PAR DEEPSEEK - EXPERT ÉLECTRICIEN")
    print("=" * 70)
    
    # Charger échantillons des 3 datasets
    datasets = {
        "basic": "/mnt/c/Users/fvegi/deepseek_training_construction.jsonl",
        "enhanced": "/mnt/c/Users/fvegi/deepseek_training_pgi_ia_enhanced.jsonl",
        "complete": "/mnt/c/Users/fvegi/deepseek_training_pgi_ia_complete.jsonl"
    }
    
    samples = {}
    for name, path in datasets.items():
        examples = []
        with open(path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= 10:  # 10 exemples par dataset
                    break
                examples.append(json.loads(line))
        samples[name] = examples
    
    # Prompt d'expert
    expert_prompt = f"""Tu es Jean-Pierre Tremblay, maître électricien avec 25 ans d'expérience au Québec, formateur CCQ et expert en sécurité électrique.

Je dois évaluer des datasets pour former une IA qui assistera des électriciens sur le terrain.

DATASET BASIC ({len(samples['basic'])} exemples sur 54):
{json.dumps(samples['basic'][:3], ensure_ascii=False, indent=2)}

DATASET ENHANCED ({len(samples['enhanced'])} exemples sur 12):
{json.dumps(samples['enhanced'][:3], ensure_ascii=False, indent=2)}

ÉVALUATION TERRAIN - Réponds comme un vrai électricien:

1. UTILITÉ PRATIQUE (0-10)
"Est-ce que ça va vraiment aider mes gars sur le chantier?"
- Pertinence des situations
- Clarté pour un apprenti
- Applicabilité immédiate

2. CONFORMITÉ QUÉBEC (0-10)
"Est-ce conforme à ce qu'on fait ici?"
- Code électrique canadien
- Normes CCQ/RBQ
- Réalités québécoises (gel, français, etc.)

3. SÉCURITÉ (0-10) - LE PLUS IMPORTANT
"Est-ce que ça va éviter des accidents?"
- Procédures cadenassage
- Identification dangers
- Réflexes sécurité

4. CE QUI MANQUE CRUELLEMENT
Dis-moi les 5 choses que mes électriciens DOIVENT savoir et qui ne sont pas là.

5. ERREURS DANGEREUSES
Y a-t-il des informations incorrectes qui pourraient causer des accidents?

6. TON VERDICT FINAL
Recommanderais-tu ce dataset pour former l'IA? Pourquoi?

Parle franchement, comme tu parlerais à un collègue. Pas de langue de bois."""

    try:
        print("\n⏳ Analyse en cours par l'expert...")
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Tu es Jean-Pierre Tremblay, maître électricien québécois avec 25 ans d'expérience terrain."},
                {"role": "user", "content": expert_prompt}
            ],
            temperature=0.7,  # Un peu plus de personnalité
            max_tokens=1500
        )
        
        expert_opinion = response.choices[0].message.content
        
        print("\n" + "="*70)
        print("OPINION DE L'EXPERT ÉLECTRICIEN")
        print("="*70)
        print(expert_opinion)
        
        # Deuxième analyse: perspective sécurité
        print("\n⏳ Analyse sécurité spécifique...")
        
        safety_prompt = f"""Maintenant, mets ton chapeau d'inspecteur CNESST. 

Regarde ces exemples du dataset:
{json.dumps(samples['complete'][:5], ensure_ascii=False, indent=2)}

AUDIT SÉCURITÉ CRITIQUE:

1. MANQUEMENTS GRAVES
Quelles situations dangereuses ne sont PAS couvertes?
- Arc électrique
- Espaces clos
- Travail en hauteur
- Procédures d'urgence

2. FORMATION MANQUANTE
Quelle formation ASP Construction n'est pas mentionnée?

3. CAS RÉELS D'ACCIDENTS
Donne 3 exemples d'accidents électriques qui pourraient arriver si l'IA ne couvre pas:
- Situation
- Conséquence
- Ce que l'IA devrait enseigner

4. RECOMMANDATIONS CNESST
Si tu devais approuver ce dataset, quelles conditions imposerais-tu?

Sois TRÈS sévère - la vie des travailleurs en dépend."""

        response2 = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Tu es inspecteur CNESST spécialisé en sécurité électrique."},
                {"role": "user", "content": safety_prompt}
            ],
            temperature=0.3,  # Plus factuel pour sécurité
            max_tokens=1200
        )
        
        safety_audit = response2.choices[0].message.content
        
        print("\n" + "="*70)
        print("AUDIT SÉCURITÉ CNESST")
        print("="*70)
        print(safety_audit)
        
        # Sauvegarder le rapport complet
        with open("/mnt/c/Users/fvegi/DEEPSEEK_EXPERT_AUDIT_FINAL.md", 'w', encoding='utf-8') as f:
            f.write("# 🔌 AUDIT EXPERT DEEPSEEK - DATASET IA ÉLECTRICITÉ\n\n")
            f.write(f"**Date**: {time.strftime('%Y-%m-%d %H:%M')}\n")
            f.write("**Évaluateurs**: Maître électricien + Inspecteur CNESST (simulés par DeepSeek)\n\n")
            f.write("## 👷 ÉVALUATION PAR MAÎTRE ÉLECTRICIEN\n\n")
            f.write(expert_opinion)
            f.write("\n\n## 🚨 AUDIT SÉCURITÉ CNESST\n\n")
            f.write(safety_audit)
            f.write("\n\n---\n*Audit généré par DeepSeek pour optimisation du dataset de formation*")
        
        print("\n✅ Audit complet sauvegardé: DEEPSEEK_EXPERT_AUDIT_FINAL.md")
        
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")

if __name__ == "__main__":
    audit_dataset_complete()