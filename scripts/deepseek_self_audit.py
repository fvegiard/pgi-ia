#!/usr/bin/env python3
"""
DeepSeek auto-audit du dataset pour IA électricité spécialisée
"""

import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv('/root/dev/pgi-ia/.env')

# Configuration DeepSeek
client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com/v1"
)

def load_dataset_sample(filename, sample_size=10):
    """Charger un échantillon du dataset"""
    examples = []
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= sample_size:
                break
            examples.append(json.loads(line))
    return examples

def deepseek_audit(dataset_file):
    """Demander à DeepSeek d'auditer le dataset"""
    
    print(f"🤖 AUDIT PAR DEEPSEEK: {dataset_file}")
    print("=" * 80)
    
    # Charger échantillon
    examples = load_dataset_sample(dataset_file, 15)
    
    # Préparer le prompt d'audit
    audit_prompt = f"""Tu es un expert en formation d'IA pour le domaine de l'électricité de construction au Québec.

Je vais te montrer {len(examples)} exemples d'un dataset destiné à entraîner une IA spécialisée en électricité pour la construction.

CONTEXTE:
- L'IA cible doit aider des électriciens et gestionnaires de projets électriques au Québec
- Elle doit connaître: Code électrique canadien, normes CCQ, CNESST, pratiques terrain
- Projets types: commercial (Alexis Nihon), institutionnel (Kahnawake)

EXEMPLES DU DATASET:
{json.dumps(examples[:5], ensure_ascii=False, indent=2)}

... ({len(examples)-5} autres exemples similaires)

ÉVALUE CE DATASET sur les critères suivants:

1. PERTINENCE TECHNIQUE (0-10)
   - Précision du vocabulaire électrique
   - Conformité aux normes québécoises
   - Utilité pratique pour électriciens

2. COUVERTURE MÉTIER (0-10)
   - Installation et câblage
   - Dépannage et diagnostic
   - Sécurité et procédures
   - Estimation et gestion projet

3. SPÉCIFICITÉ QUÉBEC (0-10)
   - Réglementation locale (CCQ, RBQ)
   - Contexte linguistique français
   - Particularités territoriales (ex: Kahnawake)

4. QUALITÉ PÉDAGOGIQUE (0-10)
   - Clarté des explications
   - Progression logique
   - Exemples concrets vs théorie

5. LACUNES CRITIQUES
   - Quels sujets essentiels manquent?
   - Quelles erreurs techniques vois-tu?
   - Quels biais pourraient être problématiques?

6. RECOMMANDATIONS PRIORITAIRES
   - Top 5 améliorations nécessaires
   - Exemples spécifiques à ajouter

Fournis une évaluation structurée et honnête. Sois critique - il vaut mieux identifier les problèmes maintenant."""

    try:
        # Appel à DeepSeek
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Tu es un expert formateur en IA spécialisé dans le domaine électrique au Québec."},
                {"role": "user", "content": audit_prompt}
            ],
            temperature=0.3,  # Plus déterministe pour l'analyse
            max_tokens=2000
        )
        
        # Afficher la réponse
        audit_result = response.choices[0].message.content
        print(audit_result)
        
        # Sauvegarder le résultat
        output_file = dataset_file.replace('.jsonl', '_deepseek_audit.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Audit DeepSeek du Dataset\n\n")
            f.write(f"**Fichier audité**: {dataset_file}\n")
            f.write(f"**Échantillon analysé**: {len(examples)} exemples\n\n")
            f.write(audit_result)
            
        print(f"\n💾 Audit sauvegardé: {output_file}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'appel DeepSeek: {str(e)}")
        
def comparative_audit():
    """Audit comparatif des différents datasets"""
    
    print("\n🔄 ANALYSE COMPARATIVE PAR DEEPSEEK")
    print("=" * 80)
    
    datasets_info = {
        "basic": load_dataset_sample("/mnt/c/Users/fvegi/deepseek_training_construction.jsonl", 20),
        "enhanced": load_dataset_sample("/mnt/c/Users/fvegi/deepseek_training_pgi_ia_enhanced.jsonl", 12),
        "complete": load_dataset_sample("/mnt/c/Users/fvegi/deepseek_training_pgi_ia_complete.jsonl", 30)
    }
    
    comparison_prompt = f"""Compare ces 3 datasets pour formation d'une IA électricité construction Québec:

DATASET 1 - BASIC ({len(datasets_info['basic'])} exemples):
{json.dumps(datasets_info['basic'][:3], ensure_ascii=False, indent=2)}

DATASET 2 - ENHANCED ({len(datasets_info['enhanced'])} exemples):
{json.dumps(datasets_info['enhanced'][:3], ensure_ascii=False, indent=2)}

DATASET 3 - COMPLETE ({len(datasets_info['complete'])} exemples):
(Combinaison des deux premiers)

Pour une IA qui doit:
- Aider électriciens terrain au Québec
- Gérer projets construction électrique
- Respecter normes CCQ/CSA/CNESST
- Comprendre contexte autochtone (Kahnawake)

ÉVALUE:
1. Quel dataset est le plus adapté et pourquoi?
2. Forces/faiblesses de chaque approche
3. Comment optimiser le dataset final?
4. Quels exemples CRITIQUES manquent pour sécurité électrique?
5. Note globale /100 pour chaque dataset

Sois direct et critique. L'objectif est une IA vraiment utile sur le terrain."""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Tu es un maître électricien et formateur IA au Québec avec 20 ans d'expérience."},
                {"role": "user", "content": comparison_prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        comparison_result = response.choices[0].message.content
        print(comparison_result)
        
        # Sauvegarder
        with open("/mnt/c/Users/fvegi/deepseek_comparative_audit.md", 'w', encoding='utf-8') as f:
            f.write("# Analyse Comparative DeepSeek des Datasets\n\n")
            f.write(comparison_result)
            
        print("\n💾 Analyse comparative sauvegardée")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    print("🚀 LANCEMENT AUDIT DEEPSEEK\n")
    
    # Auditer le dataset complet
    deepseek_audit("/mnt/c/Users/fvegi/deepseek_training_pgi_ia_complete.jsonl")
    
    # Faire l'analyse comparative
    comparative_audit()
    
    print("\n✅ Audit DeepSeek terminé!")