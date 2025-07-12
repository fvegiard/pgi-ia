#!/usr/bin/env python3
"""
Ajoute l'interface d'upload PDF à dashboard.html
"""

# Lire le fichier
with open('/home/fvegi/dev/pgi-ia/frontend/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# HTML pour la section upload
upload_html = '''                <div id="documents" class="tab-content">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="text-2xl font-bold">Documents</h2>
                        <button id="uploadBtn" class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg flex items-center">
                            <i data-lucide="upload" class="w-5 h-5 mr-2"></i>
                            Upload PDF
                        </button>
                    </div>
                    
                    <!-- Zone d'upload -->
                    <div id="uploadZone" class="bg-white rounded-lg shadow p-8 mb-6 border-2 border-dashed border-gray-300 hover:border-blue-400 transition-colors">
                        <div class="text-center">
                            <i data-lucide="file-text" class="w-16 h-16 text-gray-400 mx-auto mb-4"></i>
                            <h3 class="text-xl font-medium mb-2">Glissez-déposez vos plans PDF ici</h3>
                            <p class="text-gray-600 mb-4">ou cliquez pour sélectionner des fichiers</p>
                            <input type="file" id="fileInput" multiple accept=".pdf" class="hidden">
                            <button id="selectFiles" class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg">
                                Sélectionner des fichiers
                            </button>
                        </div>
                    </div>
                    
                    <!-- Liste des documents -->
                    <div class="bg-white rounded-lg shadow">
                        <div class="p-6 border-b">
                            <h3 class="text-lg font-semibold">Documents récents</h3>
                        </div>
                        <div id="documentsList" class="divide-y divide-gray-200">
                            <!-- Les documents apparaîtront ici -->
                        </div>
                    </div>
                </div>'''

# Remplacer la section documents vide
content = content.replace(
    '''                <div id="documents" class="tab-content">
                    <h2 class="text-2xl font-bold mb-6">Documents</h2>
                    <!-- Documents content -->
                </div>''',
    upload_html
)

# Ajouter le JavaScript pour l'upload
js_code = '''
    
    // Upload PDF functionality
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const selectFilesBtn = document.getElementById('selectFiles');
    const uploadBtn = document.getElementById('uploadBtn');
    
    // Click to select files
    selectFilesBtn?.addEventListener('click', () => fileInput.click());
    uploadBtn?.addEventListener('click', () => fileInput.click());
    
    // File input change
    fileInput?.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
    
    // Drag and drop
    uploadZone?.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('border-blue-500', 'bg-blue-50');
    });
    
    uploadZone?.addEventListener('dragleave', () => {
        uploadZone.classList.remove('border-blue-500', 'bg-blue-50');
    });
    
    uploadZone?.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('border-blue-500', 'bg-blue-50');
        handleFiles(e.dataTransfer.files);
    });
    
    // Handle files
    async function handleFiles(files) {
        for (const file of files) {
            if (file.type === 'application/pdf') {
                await uploadFile(file);
            } else {
                alert(`${file.name} n'est pas un fichier PDF`);
            }
        }
    }
    
    // Upload file
    async function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('project_id', 'kahnawake'); // Default project
        
        // Show progress
        const progressDiv = document.createElement('div');
        progressDiv.className = 'p-4 bg-blue-50 border-l-4 border-blue-500 mb-4';
        progressDiv.innerHTML = `
            <div class="flex items-center">
                <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mr-3"></div>
                <span>Upload de ${file.name}...</span>
            </div>
        `;
        document.getElementById('documentsList').prepend(progressDiv);
        
        try {
            const response = await fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                progressDiv.innerHTML = `
                    <div class="flex items-center text-green-600">
                        <i data-lucide="check-circle" class="w-6 h-6 mr-3"></i>
                        <span>${file.name} uploadé avec succès!</span>
                    </div>
                `;
                
                // Refresh documents list
                setTimeout(() => {
                    loadDocuments();
                }, 2000);
            } else {
                throw new Error('Upload failed');
            }
        } catch (error) {
            progressDiv.innerHTML = `
                <div class="flex items-center text-red-600">
                    <i data-lucide="x-circle" class="w-6 h-6 mr-3"></i>
                    <span>Erreur lors de l'upload de ${file.name}</span>
                </div>
            `;
        }
        
        // Re-initialize lucide icons
        lucide.createIcons();
    }
    
    // Load documents list
    async function loadDocuments() {
        try {
            const response = await fetch('http://localhost:5000/api/documents');
            if (response.ok) {
                const documents = await response.json();
                const listDiv = document.getElementById('documentsList');
                listDiv.innerHTML = documents.map(doc => `
                    <div class="p-4 hover:bg-gray-50">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center">
                                <i data-lucide="file-text" class="w-8 h-8 text-gray-400 mr-3"></i>
                                <div>
                                    <h4 class="font-medium">${doc.filename}</h4>
                                    <p class="text-sm text-gray-600">${doc.project} - ${doc.date}</p>
                                </div>
                            </div>
                            <div class="flex space-x-2">
                                <button class="text-blue-600 hover:text-blue-800">
                                    <i data-lucide="eye" class="w-5 h-5"></i>
                                </button>
                                <button class="text-green-600 hover:text-green-800">
                                    <i data-lucide="download" class="w-5 h-5"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                `).join('');
                lucide.createIcons();
            }
        } catch (error) {
            console.error('Error loading documents:', error);
        }
    }'''

# Ajouter le JS avant la fermeture du script
content = content.replace('</script>', js_code + '\n</script>')

# Sauvegarder le fichier modifié
with open('/home/fvegi/dev/pgi-ia/frontend/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Interface d'upload PDF ajoutée à dashboard.html!")
print("📍 Ouvrez http://localhost:8000/dashboard.html")
print("📂 Cliquez sur l'onglet 'Documents' dans le menu")
print("📤 Vous verrez la zone d'upload PDF!")