#!/usr/bin/env python3
"""
Script pour vérifier que les corrections ont été appliquées
"""

def verify_fix():
    with open('frontend/dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        "switchTab function": "function switchTab" in content,
        "Navigation event listeners": "Navigation entre onglets" in content,
        "loadDocuments function": "async function loadDocuments" in content,
        "Error handling in loadDocuments": "Erreur de chargement" in content,
        "Single loadDocuments definition": content.count("async function loadDocuments") == 1,
        "Tab click handlers": "getAttribute('data-tab')" in content
    }
    
    print("🔍 Vérification des corrections:\n")
    
    all_good = True
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}: {'OK' if result else 'MANQUANT'}")
        if not result:
            all_good = False
    
    print("\n" + "="*50)
    if all_good:
        print("✅ Toutes les corrections ont été appliquées avec succès!")
        print("\n📝 Prochaines étapes:")
        print("1. Assurez-vous que le backend est démarré: python3 backend/main.py")
        print("2. Ouvrez le dashboard dans votre navigateur")
        print("3. Cliquez sur l'onglet 'Documents'")
        print("4. Vérifiez la console du navigateur (F12) pour d'éventuelles erreurs")
    else:
        print("❌ Certaines corrections n'ont pas été appliquées correctement.")
        print("Veuillez réexécuter: python3 apply_documents_fix.py")

if __name__ == "__main__":
    verify_fix()