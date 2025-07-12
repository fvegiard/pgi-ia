// Script pour rafraîchir automatiquement la liste des documents

// Fonction pour charger et afficher les documents
function refreshDocumentsList() {
    fetch('http://localhost:5000/api/documents')
        .then(response => response.json())
        .then(documents => {
            console.log(`📄 ${documents.length} documents trouvés`);
            
            const listDiv = document.getElementById('documentsList');
            if (!listDiv) return;
            
            if (documents.length === 0) {
                listDiv.innerHTML = '<p class="p-4 text-gray-500">Aucun document</p>';
                return;
            }
            
            listDiv.innerHTML = documents.map(doc => {
                // Badge de statut
                let statusBadge = '';
                if (doc.status === 'completed') {
                    statusBadge = '<span class="px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">✅ Analysé</span>';
                } else if (doc.status === 'processing') {
                    statusBadge = '<span class="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">🔄 En cours</span>';
                } else {
                    statusBadge = '<span class="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded-full">⏳ En attente</span>';
                }
                
                // Type de plan
                const typePlan = doc.type_plan && doc.type_plan !== 'N/A' ? doc.type_plan : '';
                
                // Date formatée
                const date = new Date(doc.date).toLocaleDateString('fr-CA');
                
                return `
                    <div class="p-4 hover:bg-gray-50 border-b transition-colors">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center flex-1">
                                <i data-lucide="file-text" class="w-8 h-8 text-gray-400 mr-3"></i>
                                <div class="flex-1">
                                    <h4 class="font-medium text-gray-900">${doc.filename}</h4>
                                    <p class="text-sm text-gray-600">
                                        ${doc.project} • ${date}
                                        ${typePlan ? ' • ' + typePlan : ''}
                                    </p>
                                </div>
                                <div class="ml-4">
                                    ${statusBadge}
                                </div>
                            </div>
                            <div class="flex space-x-2 ml-4">
                                ${doc.status === 'completed' ? `
                                <button onclick="viewAnalysis('${doc.id}')" 
                                        class="text-blue-600 hover:text-blue-800 p-2 rounded hover:bg-blue-50" 
                                        title="Voir l'analyse IA">
                                    <i data-lucide="brain" class="w-5 h-5"></i>
                                </button>` : ''}
                                <button class="text-green-600 hover:text-green-800 p-2 rounded hover:bg-green-50" 
                                        title="Télécharger">
                                    <i data-lucide="download" class="w-5 h-5"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
            
            // Réinitialiser les icônes Lucide
            if (typeof lucide !== 'undefined') {
                lucide.createIcons();
            }
            
            // Afficher le compte
            updateDocumentCount(documents.length);
        })
        .catch(error => {
            console.error('Erreur lors du chargement:', error);
        });
}

// Mettre à jour le compteur
function updateDocumentCount(count) {
    const badge = document.querySelector('[data-tab="documents"] .badge');
    if (badge) {
        badge.textContent = count;
    }
}

// Rafraîchir toutes les 3 secondes
setInterval(refreshDocumentsList, 3000);

// Rafraîchir immédiatement
refreshDocumentsList();

console.log('🔄 Auto-refresh des documents activé!');