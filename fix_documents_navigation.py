#!/usr/bin/env python3
"""
Script pour corriger le problème de navigation vers l'onglet Documents
"""

import re

def fix_documents_navigation():
    """Corrige le problème de navigation dans dashboard.html"""
    
    # Lire le fichier
    with open('frontend/dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Chercher où ajouter les event listeners
    # On doit les ajouter après la définition de switchTab mais avant la fermeture du script
    
    # Code à ajouter pour gérer la navigation
    navigation_code = """
    // Configuration de la navigation entre onglets
    document.addEventListener('DOMContentLoaded', function() {
        // Attacher les event listeners aux boutons de navigation
        document.querySelectorAll('.sidebar-item[data-tab]').forEach(button => {
            button.addEventListener('click', function() {
                const tabName = this.getAttribute('data-tab');
                switchTab(tabName);
            });
        });
        
        // Initialiser avec le dashboard par défaut
        switchTab('dashboard');
        
        // Charger les documents si on arrive directement sur cet onglet
        const urlParams = new URLSearchParams(window.location.search);
        const tab = urlParams.get('tab');
        if (tab) {
            switchTab(tab);
        }
    });
"""
    
    # Trouver la position juste avant la fermeture du script
    # On cherche la dernière occurrence de </script> avant </body>
    pattern = r'(function switchTab.*?}\s*)(</script>)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # Insérer le code de navigation après la fonction switchTab
        new_content = content[:match.end(1)] + navigation_code + content[match.end(1):]
        
        # Écrire le fichier modifié
        with open('frontend/dashboard.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Navigation corrigée avec succès!")
        print("\n🔍 Changements appliqués:")
        print("- Event listeners ajoutés pour tous les boutons de navigation")
        print("- Initialisation au chargement de la page")
        print("- Support des paramètres URL pour navigation directe")
        print("\n🚀 Pour tester:")
        print("1. Démarrez le backend: python3 backend/main.py")
        print("2. Ouvrez http://localhost:5000")
        print("3. Cliquez sur 'Documents' dans la barre latérale")
        
    else:
        print("❌ Impossible de trouver la fonction switchTab dans le fichier")

if __name__ == "__main__":
    fix_documents_navigation()