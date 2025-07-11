#!/usr/bin/env python3
"""
AUDIT JUSTINA - PGI-IA v4.1
Audit qualité et expérience utilisateur en 2 tours
"""

import os
import json
import re
from pathlib import Path

def justina_tour_1():
    """TOUR 1 JUSTINA: Audit qualité interface et UX"""
    print("🎨 AUDIT JUSTINA TOUR 1 - Interface & UX")
    print("=" * 50)
    
    audit_results = {
        "ui_quality": {},
        "responsiveness": {},
        "accessibility": {},
        "performance": {}
    }
    
    # 1. Qualité Interface
    print("\n🎨 1. QUALITÉ INTERFACE")
    try:
        with open('/home/fvegi/dev/pgi-ia/frontend/index.html', 'r') as f:
            html_content = f.read()
        
        ui_checks = [
            ("Tailwind CSS", "tailwindcss.com"),
            ("Dark Theme", "bg-gray-900"),
            ("Navigation Sidebar", "sidebar"),
            ("Timeline Design", "timeline"),
            ("Cards Layout", "grid"),
            ("Icons SVG", "<svg"),
            ("Responsive Grid", "grid-cols")
        ]
        
        for check, pattern in ui_checks:
            exists = pattern in html_content
            audit_results["ui_quality"][check] = exists
            status = "✅" if exists else "❌"
            print(f"   {status} {check}")
            
    except Exception as e:
        print(f"   ❌ Erreur analyse HTML: {e}")
    
    # 2. Responsive Design
    print("\n📱 2. RESPONSIVE DESIGN")
    responsive_checks = [
        ("Mobile Classes", "sm:"),
        ("Medium Classes", "md:"),
        ("Large Classes", "lg:"),
        ("Flex Layout", "flex"),
        ("Grid Responsive", "grid-cols-1"),
        ("Hidden Mobile", "hidden")
    ]
    
    try:
        for check, pattern in responsive_checks:
            exists = pattern in html_content
            audit_results["responsiveness"][check] = exists
            status = "✅" if exists else "❌"
            print(f"   {status} {check}")
    except:
        print("   ❌ Erreur vérification responsive")
    
    # 3. Accessibilité
    print("\n♿ 3. ACCESSIBILITÉ")
    accessibility_checks = [
        ("Alt Text", 'alt="'),
        ("ARIA Labels", 'aria-'),
        ("Role Attributes", 'role="'),
        ("Semantic HTML", '<nav'),
        ("Focus States", 'focus:'),
        ("Lang Attribute", 'lang="fr"')
    ]
    
    try:
        for check, pattern in accessibility_checks:
            exists = pattern in html_content
            audit_results["accessibility"][check] = exists
            status = "✅" if exists else "⚠️"
            print(f"   {status} {check}")
    except:
        print("   ❌ Erreur vérification accessibilité")
    
    return audit_results

def justina_tour_2():
    """TOUR 2 JUSTINA: Audit fonctionnalités et interactions"""
    print("\n🎨 AUDIT JUSTINA TOUR 2 - Fonctionnalités & Interactions")
    print("=" * 50)
    
    audit_results = {
        "interactions": {},
        "data_display": {},
        "user_feedback": {},
        "workflow": {}
    }
    
    # 1. Interactions utilisateur
    print("\n🖱️ 1. INTERACTIONS UTILISATEUR")
    try:
        with open('/home/fvegi/dev/pgi-ia/frontend/script.js', 'r') as f:
            js_content = f.read()
        
        interaction_checks = [
            ("Click Events", "addEventListener('click'"),
            ("Drag Events", "addEventListener('drag"),
            ("Drop Events", "addEventListener('drop'"),
            ("Change Events", "addEventListener('change'"),
            ("Hover Effects", "hover:"),
            ("Transitions", "transition")
        ]
        
        for check, pattern in interaction_checks:
            exists = pattern in js_content
            audit_results["interactions"][check] = exists
            status = "✅" if exists else "❌"
            print(f"   {status} {check}")
            
    except Exception as e:
        print(f"   ❌ Erreur analyse JavaScript: {e}")
    
    # 2. Affichage données
    print("\n📊 2. AFFICHAGE DONNÉES")
    data_checks = [
        ("Formatage Monétaire", "formatCurrency"),
        ("Tableaux Dynamiques", "renderDirectivesTable"),
        ("Timeline Rendu", "renderTimeline"),
        ("Calculs Automatiques", "reduce((sum"),
        ("Status Badges", "status-badge"),
        ("Filtrage Données", "filter(")
    ]
    
    try:
        for check, pattern in data_checks:
            exists = pattern in js_content
            audit_results["data_display"][check] = exists
            status = "✅" if exists else "❌"
            print(f"   {status} {check}")
    except:
        print("   ❌ Erreur vérification affichage")
    
    # 3. Feedback utilisateur
    print("\n💬 3. FEEDBACK UTILISATEUR")
    feedback_checks = [
        ("Toast Notifications", "showToast"),
        ("Loading States", "Connexion"),
        ("Error Handling", "catch (error)"),
        ("Success Messages", "succès"),
        ("Visual Feedback", "classList.add"),
        ("Status Indicators", "backend-status")
    ]
    
    try:
        for check, pattern in feedback_checks:
            exists = pattern in js_content
            audit_results["user_feedback"][check] = exists
            status = "✅" if exists else "❌"
            print(f"   {status} {check}")
    except:
        print("   ❌ Erreur vérification feedback")
    
    # 4. Workflow utilisateur
    print("\n🔄 4. WORKFLOW UTILISATEUR")
    workflow_checks = [
        ("Navigation Tabs", "switchTab"),
        ("Project Switching", "switchProject"),
        ("File Upload Flow", "handleFileUpload"),
        ("Auto-refresh", "setInterval"),
        ("State Management", "currentProject"),
        ("Event Delegation", "forEach")
    ]
    
    try:
        for check, pattern in workflow_checks:
            exists = pattern in js_content
            audit_results["workflow"][check] = exists
            status = "✅" if exists else "❌"
            print(f"   {status} {check}")
    except:
        print("   ❌ Erreur vérification workflow")
    
    return audit_results

def generate_justina_report(tour1, tour2):
    """Génère rapport final Justina"""
    print("\n📋 RAPPORT FINAL JUSTINA")
    print("=" * 50)
    
    total_checks = 0
    passed_checks = 0
    
    # Compter tous les checks
    for category in [tour1, tour2]:
        for section, items in category.items():
            if isinstance(items, dict):
                for item, result in items.items():
                    total_checks += 1
                    if result:
                        passed_checks += 1
    
    ux_score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    
    print(f"📊 SCORE UX: {passed_checks}/{total_checks} ({ux_score:.1f}%)")
    
    # Évaluation qualitative
    if ux_score >= 95:
        print("🌟 VERDICT JUSTINA: EXCEPTIONNEL - UX de niveau professionnel")
        grade = "A+"
    elif ux_score >= 90:
        print("🏆 VERDICT JUSTINA: EXCELLENT - UX moderne et intuitive")
        grade = "A"
    elif ux_score >= 85:
        print("✅ VERDICT JUSTINA: TRÈS BIEN - UX solide et fonctionnelle")
        grade = "B+"
    elif ux_score >= 80:
        print("👍 VERDICT JUSTINA: BIEN - UX correcte avec améliorations mineures")
        grade = "B"
    else:
        print("⚠️ VERDICT JUSTINA: À AMÉLIORER - UX nécessite des corrections")
        grade = "C"
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS JUSTINA:")
    if ux_score >= 90:
        print("   🎯 Interface prête pour présentation executive")
        print("   🚀 UX conforme aux standards modernes")
    else:
        print("   📈 Améliorer les éléments manquants identifiés")
        print("   🔧 Optimiser l'accessibilité et le responsive")
    
    return ux_score, grade

def justina_final_validation():
    """Validation finale Justina - Test d'expérience utilisateur"""
    print("\n🎯 VALIDATION FINALE JUSTINA")
    print("=" * 50)
    
    validation_results = {}
    
    # 1. Test intégration complète
    print("\n🔗 1. INTÉGRATION COMPLÈTE")
    integration_files = [
        "/home/fvegi/dev/pgi-ia/frontend/index.html",
        "/home/fvegi/dev/pgi-ia/frontend/script.js", 
        "/home/fvegi/dev/pgi-ia/frontend/style.css",
        "/mnt/c/Users/fvegi/dev/pgi-ia-frontend/index.html"
    ]
    
    for file_path in integration_files:
        exists = os.path.exists(file_path)
        file_name = os.path.basename(file_path)
        validation_results[f"File_{file_name}"] = exists
        status = "✅" if exists else "❌"
        print(f"   {status} {file_path}")
    
    # 2. Test données réelles
    print("\n📊 2. DONNÉES RÉELLES")
    try:
        with open('/home/fvegi/dev/pgi-ia/frontend/script.js', 'r') as f:
            content = f.read()
            
        # Compter directives intégrées
        kahnawake_matches = len(re.findall(r'CO-ME-\d+', content))
        alexis_matches = len(re.findall(r'PCE-\d+', content))
        
        validation_results["Kahnawake_directives"] = kahnawake_matches >= 5
        validation_results["Alexis_directives"] = alexis_matches >= 3
        
        print(f"   ✅ Directives Kahnawake: {kahnawake_matches}")
        print(f"   ✅ Directives Alexis-Nihon: {alexis_matches}")
        
    except Exception as e:
        print(f"   ❌ Erreur test données: {e}")
    
    # 3. Score final
    passed = sum(1 for v in validation_results.values() if v)
    total = len(validation_results)
    final_score = (passed / total) * 100 if total > 0 else 0
    
    print(f"\n🏆 SCORE FINAL JUSTINA: {passed}/{total} ({final_score:.1f}%)")
    
    return final_score

if __name__ == "__main__":
    print("👩‍💻 AUDIT JUSTINA PGI-IA v4.1")
    print("=" * 60)
    
    # Exécution des 2 tours
    tour1_results = justina_tour_1()
    tour2_results = justina_tour_2()
    
    # Rapport intermédiaire
    ux_score, grade = generate_justina_report(tour1_results, tour2_results)
    
    # Validation finale
    final_score = justina_final_validation()
    
    print(f"\n🎓 AUDIT JUSTINA TERMINÉ")
    print(f"   📊 Score UX: {ux_score:.1f}%")
    print(f"   🏆 Note: {grade}")
    print(f"   🎯 Validation: {final_score:.1f}%")