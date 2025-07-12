#!/usr/bin/env python3
"""
Script pour corriger l'affichage des documents dans dashboard.html
"""

import re

def apply_fix():
    # Lire le fichier dashboard.html
    with open('frontend/dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Supprimer les définitions dupliquées de loadDocuments (garder seulement la première)
    # Compter le nombre d'occurrences
    pattern = r'async function loadDocuments\(\) \{[\s\S]*?\n\s*\}'
    matches = list(re.finditer(pattern, content))
    
    if len(matches) > 1:
        print(f"✅ Trouvé {len(matches)} définitions de loadDocuments, suppression des doublons...")
        # Garder seulement la première occurrence
        for match in reversed(matches[1:]):  # Parcourir en sens inverse pour ne pas décaler les indices
            content = content[:match.start()] + content[match.end():]
    
    # 2. Ajouter le code de navigation si pas déjà présent
    if 'function switchTab' not in content:
        print("✅ Ajout de la fonction switchTab...")
        
        # Trouver où insérer le code (avant la dernière balise </script>)
        last_script_close = content.rfind('</script>')
        
        navigation_code = '''
    // Fonction pour changer d'onglet
    function switchTab(tabName) {
        // Masquer tous les contenus d'onglet
        document.querySelectorAll('.tab-content').forEach(content => {
            content.style.display = 'none';
        });
        
        // Retirer la classe active de tous les boutons
        document.querySelectorAll('.sidebar-item').forEach(button => {
            button.classList.remove('active');
        });
        
        // Afficher le contenu de l'onglet sélectionné
        const selectedContent = document.getElementById(tabName);
        if (selectedContent) {
            selectedContent.style.display = 'block';
            
            // Si c'est l'onglet documents, charger la liste
            if (tabName === 'documents') {
                loadDocuments();
            }
        }
        
        // Ajouter la classe active au bouton sélectionné
        const selectedButton = document.querySelector(`[data-tab="${tabName}"]`);
        if (selectedButton) {
            selectedButton.classList.add('active');
        }
    }
'''
        
        content = content[:last_script_close] + navigation_code + '\n' + content[last_script_close:]
    
    # 3. Ajouter l'initialisation au DOMContentLoaded existant ou créer un nouveau
    if 'document.addEventListener(\'DOMContentLoaded\',' in content:
        # Modifier le DOMContentLoaded existant
        print("✅ Modification du DOMContentLoaded existant...")
        
        # Trouver le DOMContentLoaded
        dom_pattern = r'document\.addEventListener\([\'"]DOMContentLoaded[\'"],\s*function\s*\(\)\s*\{'
        match = re.search(dom_pattern, content)
        
        if match:
            insert_pos = match.end()
            
            init_code = '''
        // Navigation entre onglets
        document.querySelectorAll('.sidebar-item[data-tab]').forEach(button => {
            button.addEventListener('click', function() {
                const tabName = this.getAttribute('data-tab');
                switchTab(tabName);
            });
        });
        
        // Masquer tous les contenus sauf le dashboard au démarrage
        document.querySelectorAll('.tab-content').forEach(content => {
            content.style.display = 'none';
        });
        
        // Afficher le dashboard par défaut
        const dashboardContent = document.getElementById('dashboard');
        if (dashboardContent) {
            dashboardContent.style.display = 'block';
        }
        
'''
            
            # Vérifier si ce code n'est pas déjà présent
            if 'Navigation entre onglets' not in content:
                content = content[:insert_pos] + '\n' + init_code + content[insert_pos:]
    else:
        # Ajouter un nouveau DOMContentLoaded
        print("✅ Ajout d'un nouveau DOMContentLoaded...")
        
        last_script_close = content.rfind('</script>')
        
        init_code = '''
    // Initialisation au chargement de la page
    document.addEventListener('DOMContentLoaded', function() {
        // Navigation entre onglets
        document.querySelectorAll('.sidebar-item[data-tab]').forEach(button => {
            button.addEventListener('click', function() {
                const tabName = this.getAttribute('data-tab');
                switchTab(tabName);
            });
        });
        
        // Masquer tous les contenus sauf le dashboard au démarrage
        document.querySelectorAll('.tab-content').forEach(content => {
            content.style.display = 'none';
        });
        
        // Afficher le dashboard par défaut
        const dashboardContent = document.getElementById('dashboard');
        if (dashboardContent) {
            dashboardContent.style.display = 'block';
        }
    });
'''
        
        content = content[:last_script_close] + init_code + '\n' + content[last_script_close:]
    
    # 4. Améliorer la fonction loadDocuments
    print("✅ Amélioration de la fonction loadDocuments...")
    
    # Remplacer la fonction loadDocuments par une version améliorée
    old_load_pattern = r'async function loadDocuments\(\) \{[\s\S]*?\n\s*\}'
    
    new_load_function = '''async function loadDocuments() {
        try {
            const response = await fetch('http://localhost:5000/api/documents');
            if (response.ok) {
                const documents = await response.json();
                const listDiv = document.getElementById('documentsList');
                
                if (!listDiv) {
                    console.error('Element documentsList not found');
                    return;
                }
                
                if (documents.length === 0) {
                    listDiv.innerHTML = `
                        <div class="p-8 text-center text-gray-500">
                            <i data-lucide="inbox" class="w-16 h-16 mx-auto mb-4 text-gray-300"></i>
                            <p class="text-lg">Aucun document trouvé</p>
                            <p class="text-sm mt-2">Uploadez votre premier plan PDF pour commencer</p>
                        </div>
                    `;
                } else {
                    listDiv.innerHTML = documents.map(doc => `
                        <div class="p-4 hover:bg-gray-50 transition-colors cursor-pointer">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center">
                                    <i data-lucide="file-text" class="w-8 h-8 text-gray-400 mr-3"></i>
                                    <div>
                                        <h4 class="font-medium">${doc.filename}</h4>
                                        <p class="text-sm text-gray-600">${doc.project} - ${new Date(doc.date).toLocaleDateString('fr-CA')}</p>
                                        ${doc.status === 'completed' ? 
                                            '<span class="text-xs text-green-600">✓ Analyse complétée</span>' : 
                                            '<span class="text-xs text-yellow-600">⏳ Analyse en cours...</span>'
                                        }
                                    </div>
                                </div>
                                <div class="flex space-x-2">
                                    <button class="text-blue-600 hover:text-blue-800 p-1" title="Voir les détails">
                                        <i data-lucide="eye" class="w-5 h-5"></i>
                                    </button>
                                    <button class="text-green-600 hover:text-green-800 p-1" title="Télécharger">
                                        <i data-lucide="download" class="w-5 h-5"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    `).join('');
                }
                
                // Re-initialiser les icônes Lucide
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            } else {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        } catch (error) {
            console.error('Error loading documents:', error);
            const listDiv = document.getElementById('documentsList');
            if (listDiv) {
                listDiv.innerHTML = `
                    <div class="p-8 text-center text-red-500">
                        <i data-lucide="alert-circle" class="w-16 h-16 mx-auto mb-4"></i>
                        <p class="text-lg">Erreur de chargement</p>
                        <p class="text-sm mt-2">Impossible de charger les documents. Vérifiez que le serveur est démarré.</p>
                        <button onclick="loadDocuments()" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                            Réessayer
                        </button>
                    </div>
                `;
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            }
        }
    }'''
    
    content = re.sub(old_load_pattern, new_load_function, content, count=1)
    
    # 5. Sauvegarder le fichier modifié
    with open('frontend/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Corrections appliquées avec succès!")
    print("\n📋 Résumé des modifications:")
    print("1. Suppression des fonctions loadDocuments dupliquées")
    print("2. Ajout de la fonction switchTab pour la navigation")
    print("3. Ajout des gestionnaires d'événements pour les boutons de navigation")
    print("4. Amélioration de la fonction loadDocuments avec gestion d'erreurs")
    print("\n🚀 Redémarrez le serveur et testez l'onglet Documents!")

if __name__ == "__main__":
    apply_fix()