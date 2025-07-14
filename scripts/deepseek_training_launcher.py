#!/usr/bin/env python3
"""
Lancement de l'entraînement DeepSeek avec le dataset enrichi
"""

import json
import os
from openai import OpenAI
from dotenv import load_dotenv
import time

# Configuration
load_dotenv('/root/dev/pgi-ia/.env')
DATASET_PATH = "/mnt/c/Users/fvegi/deepseek_training_final_quebec_fixed.jsonl"

client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com/v1"
)

def validate_dataset():
    """Valider le dataset avant entraînement"""
    print("🔍 VALIDATION DATASET DEEPSEEK")
    print("=" * 60)
    
    examples = []
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            examples.append(json.loads(line))
    
    print(f"✅ Exemples chargés: {len(examples)}")
    
    # Statistiques
    stats = {
        'total': len(examples),
        'system_prompts': set(),
        'avg_messages': 0,
        'categories': {}
    }
    
    total_messages = 0
    for ex in examples:
        total_messages += len(ex['messages'])
        system_content = ex['messages'][0]['content']
        stats['system_prompts'].add(system_content)
        
        # Catégoriser
        if 'sécurité' in system_content:
            stats['categories']['sécurité'] = stats['categories'].get('sécurité', 0) + 1
        elif 'First Nations' in system_content or 'autochtone' in system_content:
            stats['categories']['autochtone'] = stats['categories'].get('autochtone', 0) + 1
        elif 'CCQ' in system_content or 'québécois' in system_content:
            stats['categories']['québec'] = stats['categories'].get('québec', 0) + 1
        else:
            stats['categories']['général'] = stats['categories'].get('général', 0) + 1
    
    stats['avg_messages'] = total_messages / len(examples)
    stats['unique_prompts'] = len(stats['system_prompts'])
    
    print(f"\n📊 STATISTIQUES:")
    print(f"  • Prompts système uniques: {stats['unique_prompts']}")
    print(f"  • Messages moyens par exemple: {stats['avg_messages']:.1f}")
    print(f"\n📂 CATÉGORIES:")
    for cat, count in stats['categories'].items():
        print(f"  • {cat}: {count} ({count/stats['total']*100:.1f}%)")
    
    return examples, stats

def test_with_examples(examples):
    """Tester DeepSeek avec quelques exemples"""
    print("\n\n🧪 TEST AVEC EXEMPLES RÉELS")
    print("=" * 60)
    
    # Prendre 3 exemples variés
    test_cases = [
        examples[0],  # Premier exemple
        examples[len(examples)//2],  # Milieu
        examples[-1]  # Dernier
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}/3:")
        user_msg = case['messages'][1]['content']
        expected = case['messages'][2]['content']
        
        print(f"Question: {user_msg[:100]}...")
        
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": case['messages'][0]['content']},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.5,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            print(f"✅ Réponse DeepSeek reçue ({len(answer)} caractères)")
            
            # Comparer avec attendu
            if len(expected) > 100:
                print(f"Attendu: {expected[:100]}...")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            
        time.sleep(1)  # Rate limiting

def create_training_config():
    """Créer configuration pour fine-tuning"""
    config = {
        "model": "deepseek-chat",
        "dataset": "pgi_ia_quebec_electrical",
        "training_file": DATASET_PATH,
        "validation_split": 0.1,
        "hyperparameters": {
            "epochs": 3,
            "batch_size": 4,
            "learning_rate": 2e-5,
            "warmup_steps": 100
        },
        "metadata": {
            "project": "PGI-IA",
            "domain": "Construction électrique Québec",
            "language": "français",
            "safety": "Disclaimers CNESST inclus",
            "version": "1.0"
        }
    }
    
    config_path = "/mnt/c/Users/fvegi/deepseek_training_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Configuration sauvegardée: {config_path}")
    return config

def generate_deployment_script():
    """Créer script de déploiement pour production"""
    script = """#!/usr/bin/env python3
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
        system_prompt += f"\\n\\nContexte projet actuel: {project_context}"
    
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
    print("\\n📋 Test Directive:")
    response = query_pgi_ia(
        "J'ai reçu la directive PCE-47 pour Kahnawake, comment procéder?",
        "C24-060 - Centre Culturel Kahnawake"
    )
    print(response)
    
    # Test 2: Question CCQ
    print("\\n👷 Test CCQ:")
    response = query_pgi_ia("Quel est le ratio compagnon/apprenti pour un chantier commercial?")
    print(response)
    
    # Test 3: Sécurité (doit rediriger)
    print("\\n⚠️ Test Sécurité:")
    response = query_pgi_ia("Comment faire le cadenassage d'un panneau 600V?")
    print(response)
"""
    
    script_path = "/mnt/c/Users/fvegi/deploy_pgi_ia_production.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)
    
    print(f"\n🚀 Script de déploiement créé: {script_path}")

def main():
    """Pipeline principal"""
    print("🚀 LANCEMENT ENTRAÎNEMENT DEEPSEEK - PGI-IA")
    print("=" * 60)
    
    # 1. Valider dataset
    examples, stats = validate_dataset()
    
    # 2. Tester avec exemples
    test_with_examples(examples)
    
    # 3. Créer configuration
    config = create_training_config()
    
    # 4. Générer script déploiement
    generate_deployment_script()
    
    # 5. Instructions finales
    print("\n\n📌 PROCHAINES ÉTAPES:")
    print("=" * 60)
    print("1. ENTRAÎNEMENT (si API le permet):")
    print("   deepseek train --config deepseek_training_config.json")
    print("\n2. VALIDATION:")
    print("   python deploy_pgi_ia_production.py")
    print("\n3. INTÉGRATION:")
    print("   - Remplacer MODEL_ID dans le script de déploiement")
    print("   - Intégrer dans l'API Flask existante")
    print("   - Tester avec vrais utilisateurs DR Électrique")
    print("\n4. MONITORING:")
    print("   - Logger toutes les requêtes")
    print("   - Mesurer satisfaction utilisateurs")
    print("   - Identifier cas non couverts")
    
    print(f"\n✅ Dataset prêt: {stats['total']} exemples")
    print(f"🎯 Focus: Construction électrique Québec (sans sécurité CNESST)")

if __name__ == "__main__":
    main()