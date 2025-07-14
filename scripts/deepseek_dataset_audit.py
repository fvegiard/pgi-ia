#!/usr/bin/env python3
"""
Audit complet du dataset DeepSeek pour PGI-IA
"""

import json
import re
from collections import Counter, defaultdict
import statistics

def audit_dataset(filename):
    """Analyser en profondeur le dataset"""
    
    print(f"🔍 AUDIT DU DATASET: {filename}")
    print("=" * 80)
    
    # Charger les données
    messages = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                messages.append(json.loads(line))
            except:
                print(f"⚠️ Ligne invalide détectée")
    
    print(f"\n📊 STATISTIQUES GÉNÉRALES")
    print(f"Total d'exemples: {len(messages)}")
    
    # 1. ANALYSE DES RÔLES
    print(f"\n🎭 ANALYSE DES RÔLES")
    role_counts = Counter()
    for msg in messages:
        for m in msg['messages']:
            role_counts[m['role']] += 1
    
    for role, count in role_counts.items():
        print(f"  - {role}: {count} messages")
    
    # 2. ANALYSE DES SYSTEM PROMPTS
    print(f"\n🤖 TYPES DE SYSTEM PROMPTS")
    system_prompts = []
    for msg in messages:
        system_msg = next((m['content'] for m in msg['messages'] if m['role'] == 'system'), None)
        if system_msg:
            system_prompts.append(system_msg)
    
    system_types = Counter(system_prompts)
    for prompt, count in system_types.most_common(10):
        print(f"  - [{count}x] {prompt[:80]}...")
    
    # 3. ANALYSE DE LA LONGUEUR
    print(f"\n📏 ANALYSE DES LONGUEURS")
    user_lengths = []
    assistant_lengths = []
    
    for msg in messages:
        for m in msg['messages']:
            if m['role'] == 'user':
                user_lengths.append(len(m['content']))
            elif m['role'] == 'assistant':
                assistant_lengths.append(len(m['content']))
    
    print(f"Questions utilisateur:")
    print(f"  - Moyenne: {statistics.mean(user_lengths):.0f} caractères")
    print(f"  - Min/Max: {min(user_lengths)}/{max(user_lengths)}")
    
    print(f"Réponses assistant:")
    print(f"  - Moyenne: {statistics.mean(assistant_lengths):.0f} caractères")
    print(f"  - Min/Max: {min(assistant_lengths)}/{max(assistant_lengths)}")
    
    # 4. ANALYSE DU CONTENU QUÉBÉCOIS
    print(f"\n🍁 SPÉCIFICITÉ QUÉBÉCOISE")
    quebec_keywords = ['québec', 'ccq', 'cnesst', 'csa', 'mohawk', 'kahnawake', 
                      'hydro-québec', 'rbq', 'première nation', 'first nation',
                      'compagnon', 'cominar', 'tps', 'tvq']
    
    quebec_count = 0
    for msg in messages:
        content = json.dumps(msg, ensure_ascii=False).lower()
        if any(keyword in content for keyword in quebec_keywords):
            quebec_count += 1
    
    print(f"  - Exemples avec contexte Québec: {quebec_count}/{len(messages)} ({quebec_count/len(messages)*100:.1f}%)")
    
    # 5. ANALYSE DES PROJETS MENTIONNÉS
    print(f"\n🏗️ PROJETS MENTIONNÉS")
    project_mentions = Counter()
    project_patterns = [
        (r'[CS]\d{2}-\d{3,4}', 'Codes projets'),
        (r'kahnawake|musée', 'Kahnawake'),
        (r'alexis[\s-]?nihon', 'Alexis Nihon'),
        (r'qmd|entreprises qmd', 'QMD'),
        (r'cominar', 'Cominar')
    ]
    
    for msg in messages:
        content = json.dumps(msg, ensure_ascii=False).lower()
        for pattern, name in project_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                project_mentions[name] += 1
    
    for project, count in project_mentions.most_common():
        print(f"  - {project}: {count} mentions")
    
    # 6. ANALYSE TECHNIQUE
    print(f"\n⚡ CONTENU TECHNIQUE ÉLECTRIQUE")
    tech_keywords = {
        'Panneaux': ['panneau', 'panel', 'distribution'],
        'Câblage': ['câble', 'conduit', 'fil', 'conducteur'],
        'Normes': ['csa', 'code électrique', 'article', 'norme'],
        'Sécurité': ['cadenassage', 'sécurité', 'cnesst', 'mise à terre'],
        'Équipements': ['disjoncteur', 'prise', 'luminaire', 'transformateur'],
        'Documents': ['plan', 'devis', 'directive', 'facture']
    }
    
    tech_counts = defaultdict(int)
    for msg in messages:
        content = json.dumps(msg, ensure_ascii=False).lower()
        for category, keywords in tech_keywords.items():
            if any(kw in content for kw in keywords):
                tech_counts[category] += 1
    
    for category, count in sorted(tech_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {category}: {count} exemples ({count/len(messages)*100:.1f}%)")
    
    # 7. DÉTECTION DE PROBLÈMES
    print(f"\n⚠️ PROBLÈMES POTENTIELS")
    problems = []
    
    # Vérifier les réponses génériques
    generic_responses = 0
    for msg in messages:
        assistant_msg = next((m['content'] for m in msg['messages'] if m['role'] == 'assistant'), "")
        if "plans électriques" in assistant_msg and "éléments clés incluent" in assistant_msg:
            generic_responses += 1
    
    if generic_responses > 5:
        problems.append(f"Réponses génériques détectées: {generic_responses} exemples utilisent la même formulation")
    
    # Vérifier la diversité
    unique_questions = len(set(m['messages'][1]['content'] for m in messages if len(m['messages']) > 1))
    if unique_questions < len(messages) * 0.8:
        problems.append(f"Manque de diversité: seulement {unique_questions} questions uniques sur {len(messages)}")
    
    # Vérifier l'équilibre des catégories
    if tech_counts['Documents'] > len(messages) * 0.5:
        problems.append("Surreprésentation des documents par rapport aux aspects techniques")
    
    if problems:
        for p in problems:
            print(f"  ❌ {p}")
    else:
        print("  ✅ Aucun problème majeur détecté")
    
    # 8. RECOMMANDATIONS
    print(f"\n💡 RECOMMANDATIONS D'AMÉLIORATION")
    recommendations = []
    
    if quebec_count < len(messages) * 0.7:
        recommendations.append("Ajouter plus de contexte spécifique au Québec (réglementation, organismes)")
    
    if tech_counts['Sécurité'] < 5:
        recommendations.append("Enrichir avec plus d'exemples de sécurité (ASP Construction, procédures)")
    
    if 'estimation' not in str(tech_counts):
        recommendations.append("Ajouter des exemples de calculs et estimations détaillées")
    
    if not any('erreur' in json.dumps(m).lower() for m in messages):
        recommendations.append("Inclure des exemples de résolution de problèmes et erreurs courantes")
    
    for r in recommendations:
        print(f"  → {r}")
    
    # 9. SCORE DE QUALITÉ
    print(f"\n🏆 SCORE DE QUALITÉ GLOBAL")
    scores = {
        'Diversité': min(100, (unique_questions / len(messages)) * 100),
        'Spécificité Québec': (quebec_count / len(messages)) * 100,
        'Couverture technique': len(tech_counts) * 10,
        'Longueur réponses': min(100, (statistics.mean(assistant_lengths) / 300) * 100),
        'Absence problèmes': 100 if not problems else 50
    }
    
    for critere, score in scores.items():
        print(f"  - {critere}: {score:.0f}/100")
    
    score_global = statistics.mean(scores.values())
    print(f"\n  📊 SCORE GLOBAL: {score_global:.0f}/100")
    
    if score_global >= 80:
        print("  ✅ Dataset de haute qualité!")
    elif score_global >= 60:
        print("  🔶 Dataset acceptable mais peut être amélioré")
    else:
        print("  ❌ Dataset nécessite des améliorations significatives")
    
    return score_global, problems, recommendations

if __name__ == "__main__":
    # Auditer les trois datasets
    datasets = [
        "/mnt/c/Users/fvegi/deepseek_training_construction.jsonl",
        "/mnt/c/Users/fvegi/deepseek_training_pgi_ia_enhanced.jsonl",
        "/mnt/c/Users/fvegi/deepseek_training_pgi_ia_complete.jsonl"
    ]
    
    for dataset in datasets:
        try:
            print("\n" + "="*80 + "\n")
            audit_dataset(dataset)
        except FileNotFoundError:
            print(f"❌ Fichier non trouvé: {dataset}")
        except Exception as e:
            print(f"❌ Erreur lors de l'audit: {str(e)}")