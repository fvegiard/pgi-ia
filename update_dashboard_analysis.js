// Code JavaScript pour afficher l'analyse dans le dashboard

// Modifier la fonction loadDocuments pour afficher le statut d'analyse
async function loadDocuments() {
    try {
        const response = await fetch('http://localhost:5000/api/documents');
        if (response.ok) {
            const documents = await response.json();
            const listDiv = document.getElementById('documentsList');
            
            if (documents.length === 0) {
                listDiv.innerHTML = '<p class="p-4 text-gray-500">Aucun document uploadé</p>';
                return;
            }
            
            listDiv.innerHTML = documents.map(doc => {
                const statusBadge = doc.status === 'completed' 
                    ? '<span class="px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">✅ Analysé</span>'
                    : doc.status === 'processing'
                    ? '<span class="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">🔄 En cours</span>'
                    : '<span class="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded-full">⏳ En attente</span>';
                
                const typePlan = doc.type_plan || 'Non analysé';
                
                return `
                    <div class="p-4 hover:bg-gray-50 border-b">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center flex-1">
                                <i data-lucide="file-text" class="w-8 h-8 text-gray-400 mr-3"></i>
                                <div class="flex-1">
                                    <h4 class="font-medium">${doc.filename}</h4>
                                    <p class="text-sm text-gray-600">
                                        ${doc.project} • ${new Date(doc.date).toLocaleDateString('fr-CA')}
                                        ${doc.has_analysis ? ' • ' + typePlan : ''}
                                    </p>
                                </div>
                                ${statusBadge}
                            </div>
                            <div class="flex space-x-2 ml-4">
                                ${doc.status === 'completed' ? `
                                <button onclick="viewAnalysis('${doc.id}')" class="text-blue-600 hover:text-blue-800" title="Voir l'analyse">
                                    <i data-lucide="brain" class="w-5 h-5"></i>
                                </button>` : ''}
                                <button class="text-green-600 hover:text-green-800" title="Télécharger">
                                    <i data-lucide="download" class="w-5 h-5"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
            
            lucide.createIcons();
        }
    } catch (error) {
        console.error('Error loading documents:', error);
    }
}

// Fonction pour voir l'analyse détaillée
async function viewAnalysis(fileId) {
    try {
        const response = await fetch(`http://localhost:5000/api/analysis/${fileId}`);
        if (response.ok) {
            const data = await response.json();
            
            // Créer un modal pour afficher l'analyse
            const modal = document.createElement('div');
            modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
            modal.innerHTML = `
                <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full m-4 max-h-[80vh] overflow-hidden">
                    <div class="p-6 border-b">
                        <div class="flex justify-between items-center">
                            <h2 class="text-xl font-bold">🧠 Analyse IA - ${data.filename}</h2>
                            <button onclick="this.closest('.fixed').remove()" class="text-gray-400 hover:text-gray-600">
                                <i data-lucide="x" class="w-6 h-6"></i>
                            </button>
                        </div>
                    </div>
                    <div class="p-6 overflow-y-auto max-h-[60vh]">
                        ${formatAnalysis(data.analysis)}
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
            lucide.createIcons();
        }
    } catch (error) {
        console.error('Error loading analysis:', error);
    }
}

// Formater l'analyse pour l'affichage
function formatAnalysis(analysis) {
    if (!analysis) return '<p class="text-gray-500">Aucune analyse disponible</p>';
    
    if (analysis.error) {
        return `<div class="text-red-600">Erreur: ${analysis.error}</div>`;
    }
    
    let html = '<div class="space-y-4">';
    
    if (analysis.type_plan) {
        html += `
            <div>
                <h3 class="font-semibold text-gray-700">Type de plan</h3>
                <p class="mt-1">${analysis.type_plan}</p>
            </div>
        `;
    }
    
    if (analysis.composants) {
        html += `
            <div>
                <h3 class="font-semibold text-gray-700">Composants détectés</h3>
                <p class="mt-1">${analysis.composants}</p>
            </div>
        `;
    }
    
    if (analysis.normes && analysis.normes.length > 0) {
        html += `
            <div>
                <h3 class="font-semibold text-gray-700">Normes référencées</h3>
                <ul class="mt-1 list-disc list-inside">
                    ${analysis.normes.map(n => `<li>${n}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (analysis.alertes && analysis.alertes.length > 0) {
        html += `
            <div>
                <h3 class="font-semibold text-gray-700">Alertes</h3>
                <ul class="mt-1 space-y-1">
                    ${analysis.alertes.map(a => `<li class="text-orange-600">⚠️ ${a}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    if (analysis.resume) {
        html += `
            <div>
                <h3 class="font-semibold text-gray-700">Résumé</h3>
                <p class="mt-1">${analysis.resume}</p>
            </div>
        `;
    }
    
    html += '</div>';
    return html;
}

// Ajouter au code existant
console.log('📊 Mise à jour de l\'interface pour afficher les analyses IA');

// Recharger automatiquement toutes les 5 secondes pour voir les nouvelles analyses
setInterval(loadDocuments, 5000);