// Code JavaScript à ajouter dans dashboard.html pour corriger l'affichage des documents

// 1. Ajouter ce code dans la section <script> existante ou dans une nouvelle section <script>

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

// 2. Ajouter les gestionnaires d'événements au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Ajouter les écouteurs de clic sur tous les boutons de navigation
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
    
    // Optionnel : Charger les documents au démarrage si nécessaire
    // loadDocuments();
});

// 3. Correction de la fonction loadDocuments pour gérer les erreurs
// Remplacer toutes les occurrences de la fonction loadDocuments par cette version corrigée :

async function loadDocuments() {
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
                    <div class="p-4 hover:bg-gray-50">
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
                                <button class="text-blue-600 hover:text-blue-800" title="Voir les détails">
                                    <i data-lucide="eye" class="w-5 h-5"></i>
                                </button>
                                <button class="text-green-600 hover:text-green-800" title="Télécharger">
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
                </div>
            `;
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
        }
    }
}