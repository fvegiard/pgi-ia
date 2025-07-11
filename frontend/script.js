// PGI-IA Frontend Script - Version Intégrée avec données Gemini
const API_BASE = 'http://localhost:5000';

// Données réelles des projets (intégrées depuis demo Gemini)
const projectsData = {
    kahnawake: {
        id: "S-1086",
        nom: "Musée Kahnawake",
        statut: "Estimation",
        po_client: "QMD",
        directives: [
            { id: 'CO-ME-039', dateRecue: '2025-06-16', desc: "Repositionnement des luminaires sur rail pour éviter les cloisons de verre.", po: '', dateSoumis: '', price: 0, status: 'À préparer' },
            { id: 'CO-ME-28', dateRecue: '2025-04-22', desc: "Ajout vanne supervisée (raccordement électrique requis) et modif. tuyaux.", po: '', dateSoumis: '', price: 0, status: 'À préparer' },
            { id: 'CO-ME-17', dateRecue: '2025-01-21', desc: "Modification du tracé de conduits suite aux commentaires d'Hydro-Québec.", po: '', dateSoumis: '2025-01-22', price: 8451.30, status: 'Soumis' },
            { id: 'CO-ME-32', dateRecue: '2025-05-27', desc: "Déplacement conduits électriques suite modif. ventilation (Réf. CD A32).", po: '', dateSoumis: '2025-05-30', price: 2157.30, status: 'Soumis' },
            { id: 'CO-ME-35', dateRecue: '2025-06-17', desc: "Modification protection électrique (disjoncteur 80A) suite à FS-01.", po: '', dateSoumis: '2025-07-02', price: 644.95, status: 'Soumis' },
            { id: 'CO-ME-20', dateRecue: '2025-05-07', desc: "Modification éclairage rampe musée, ajout/retrait A/V, ajout connexions vitrines (Réf. A27).", po: 'EDC0144R2', dateSoumis: '2025-06-16', price: 60966.56, status: 'Approuvé' },
            { id: 'CO-ME-03', dateRecue: '2024-08-28', desc: "Modification du tracé des conduits de télécom (poteau Bell).", po: 'EDC0039', dateSoumis: '2025-01-17', price: 33878.77, status: 'Approuvé' },
            { id: 'CO-ME-16', dateRecue: '2025-02-17', desc: "Modifications majeures au lot d'éclairage (retraits M4A, M5A, M5D, etc.).", po: 'EDC0119', dateSoumis: '2025-05-22', price: -389778.16, status: 'Approuvé' },
        ]
    },
    "alexis-nihon": {
        id: "C-24-048", 
        nom: "Place Alexis-Nihon",
        statut: "Construction",
        po_client: "JCB",
        directives: [
            {"id":"PCE-12","dateRecue":"","desc":"Coordination foire alimentaire (mezzanine). Ajout relais & module supervision.","po":"","dateSoumis":"2025-05-20","price":1485,"status":"À préparer"},
            {"id":"PCE-21","dateRecue":"","desc":"Boitiers avec température contrôlée pour téléphones pompiers.","po":"","dateSoumis":"","price":2615,"status":"À préparer"},
            {"id":"PCE-1","dateRecue":"","desc":"Inclus dans 6 JCB16 (Prix visé)","po":"195151","price":-45525.39,"status":"Soumis"},
            {"id":"PCE-2","dateRecue":"","desc":"Inclus dans 5 JCB16 (Prix visé)","po":"195298","price":38643.62,"status":"Soumis"},
            {"id":"PCE-20","dateRecue":"","desc":"Travaux selon JCB-22 (Prix visé)","po":"196960","price":4710.11,"status":"Soumis"},
            {"id":"PCE-22","dateRecue":"","desc":"Interface temporaire entre ancien et nouveau système d'alarme incendie.","po":"","price":7576.93,"status":"Soumis"},
        ]
    }
};

// Timeline events data
const timelineEvents = [
    {
        time: "09:02",
        type: "email",
        title: "Courriel reçu de l'architecte",
        description: "Sujet: Précisions sur les luminaires. Classé automatiquement.",
        icon: "email"
    },
    {
        time: "08:25", 
        type: "3d",
        title: "Jumeau Numérique mis à jour",
        description: "La géométrie 3D du plan E-101 a été intégrée.",
        icon: "cube"
    },
    {
        time: "08:16",
        type: "processing",
        title: "Lancement de l'agent de vectorisation",
        description: "L'IA a initié la conversion du plan E-101 en format DWG.",
        icon: "cog"
    },
    {
        time: "08:15",
        type: "upload",
        title: "Plan E-101 Rev A reçu",
        description: "Fichier PDF du plan électrique principal déposé.",
        icon: "document"
    }
];

// State management
let currentProject = 'kahnawake';
let currentTab = 'dashboard';

// Utility functions
function formatCurrency(value) {
    const formatted = new Intl.NumberFormat('fr-CA', { style: 'currency', currency: 'CAD' }).format(Math.abs(value));
    return value < 0 ? `(${formatted})` : formatted;
}

function getStatusClass(status) {
    const mapping = {
        'À préparer': 'status-a-preparer',
        'Soumis': 'status-soumis', 
        'Approuvé': 'status-approuve',
        'Sans Frais': 'status-sans-frais',
        'Estimation': 'status-estimation',
        'Construction': 'status-construction'
    };
    return mapping[status] || 'status-default';
}

function showToast(message) {
    const toast = document.getElementById('toast-success');
    const messageEl = document.getElementById('toast-message');
    messageEl.textContent = message;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 3000);
}

// Project management
function switchProject(projectKey) {
    currentProject = projectKey;
    const project = projectsData[projectKey];
    
    // Update header
    document.getElementById('main-title').textContent = `${project.id} - ${project.nom}`;
    document.getElementById('main-subtitle').textContent = `Tableau de bord central du projet - ${project.statut}`;
    
    // Update project cards in sidebar
    document.querySelectorAll('.project-card').forEach(card => {
        card.classList.remove('active');
        if (card.dataset.project === projectKey) {
            card.classList.add('active');
        }
    });
    
    // Update data
    updateDashboard();
    updateDirectives();
}

// Dashboard functions
function updateDashboard() {
    const project = projectsData[currentProject];
    const directives = project.directives;
    
    // Calculate totals
    const approvedAndSubmitted = directives.filter(d => d.status === 'Approuvé' || d.status === 'Soumis');
    const totalExtras = approvedAndSubmitted.filter(d => d.price > 0).reduce((sum, d) => sum + d.price, 0);
    const totalCredits = approvedAndSubmitted.filter(d => d.price < 0).reduce((sum, d) => sum + d.price, 0);
    const netImpact = totalExtras + totalCredits;
    
    // Update dashboard cards
    document.getElementById('total-extras').textContent = formatCurrency(totalExtras);
    document.getElementById('total-credits').textContent = formatCurrency(totalCredits);
    document.getElementById('net-impact').textContent = formatCurrency(netImpact);
    document.getElementById('total-directives').textContent = directives.length;
    
    // Update timeline
    renderTimeline();
}

function renderTimeline() {
    const container = document.getElementById('timeline-container');
    container.innerHTML = timelineEvents.map(event => `
        <div class="flex items-start space-x-4">
            <div class="flex-shrink-0">
                ${getTimelineIcon(event.icon)}
            </div>
            <div class="flex-grow">
                <div class="flex items-center justify-between">
                    <h4 class="text-sm font-medium text-white">${event.title}</h4>
                    <span class="text-xs text-gray-400">${event.time}</span>
                </div>
                <p class="text-xs text-gray-400 mt-1">${event.description}</p>
            </div>
        </div>
    `).join('');
}

function getTimelineIcon(type) {
    const icons = {
        email: '<svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>',
        cube: '<svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>',
        cog: '<svg class="w-6 h-6 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>',
        document: '<svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>'
    };
    return icons[type] || icons.document;
}

// Directives functions
function updateDirectives() {
    const project = projectsData[currentProject];
    const directives = project.directives;
    
    // Update project summary
    const approvedAndSubmitted = directives.filter(d => d.status === 'Approuvé' || d.status === 'Soumis');
    const totalExtras = approvedAndSubmitted.filter(d => d.price > 0).reduce((sum, d) => sum + d.price, 0);
    const totalCredits = approvedAndSubmitted.filter(d => d.price < 0).reduce((sum, d) => sum + d.price, 0);
    const netImpact = totalExtras + totalCredits;
    
    document.getElementById('project-total-extras').textContent = formatCurrency(totalExtras);
    document.getElementById('project-total-credits').textContent = formatCurrency(totalCredits);
    document.getElementById('project-net-impact').textContent = formatCurrency(netImpact);
    
    // Render table
    renderDirectivesTable(directives);
}

function renderDirectivesTable(directives) {
    const tbody = document.getElementById('directives-tbody');
    
    if (directives.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center py-8 text-gray-400">Aucune directive trouvée</td></tr>';
        return;
    }
    
    tbody.innerHTML = directives.map(directive => `
        <tr class="hover:bg-gray-700 transition-colors duration-200">
            <td class="px-4 py-3 text-sm font-medium text-white">${directive.id}</td>
            <td class="px-4 py-3 text-sm text-gray-300">${directive.dateRecue || '-'}</td>
            <td class="px-4 py-3 text-sm text-gray-300">${directive.desc}</td>
            <td class="px-4 py-3 text-sm text-gray-300">${directive.po || '-'}</td>
            <td class="px-4 py-3 text-sm text-right font-mono ${directive.price < 0 ? 'text-red-400' : 'text-gray-300'}">${directive.price !== 0 ? formatCurrency(directive.price) : '-'}</td>
            <td class="px-4 py-3 text-sm">
                <span class="status-badge ${getStatusClass(directive.status)}">${directive.status}</span>
            </td>
        </tr>
    `).join('');
}

// Tab management
function switchTab(tabName) {
    currentTab = tabName;
    
    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });
    
    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');
    
    // Update subtitle
    const subtitles = {
        dashboard: 'Tableau de bord central du projet',
        projects: 'Gestion des plans et modèles 3D',
        directives: 'Suivi des directives de changement',
        estimations: 'Analyse des estimations et coûts',
        ai: 'Orchestration et commandes IA'
    };
    document.getElementById('main-subtitle').textContent = subtitles[tabName] || 'PGI-IA';
}

// File upload handling
async function handleFileUpload(files) {
    for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch(`${API_BASE}/upload`, {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                showToast(`Fichier ${file.name} traité avec succès`);
                
                // Add to timeline
                timelineEvents.unshift({
                    time: new Date().toLocaleTimeString('fr-CA', { hour: '2-digit', minute: '2-digit' }),
                    type: "upload",
                    title: `${file.name} traité`,
                    description: result.result?.description || `Fichier ${file.name} traité automatiquement`,
                    icon: "document"
                });
                
                // Refresh displays
                if (currentTab === 'dashboard') renderTimeline();
                
            } else {
                showToast(`Erreur lors du traitement de ${file.name}`);
            }
        } catch (error) {
            showToast(`Erreur de connexion`);
        }
    }
}

// Backend status check
async function checkBackendStatus() {
    const statusEl = document.getElementById('backend-status');
    const spinner = document.getElementById('loading-spinner');
    
    try {
        // Show loading state
        spinner.style.display = 'inline-block';
        statusEl.innerHTML = '<span class="loading-spinner mr-2"></span>Connexion...';
        
        const response = await fetch(`${API_BASE}/`);
        if (response.ok) {
            const data = await response.json();
            spinner.style.display = 'none';
            statusEl.textContent = `✅ ${data.status}`;
        }
    } catch (error) {
        spinner.style.display = 'none';
        statusEl.textContent = '❌ Hors ligne';
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });
    
    // Project cards
    document.querySelectorAll('.project-card').forEach(card => {
        card.addEventListener('click', () => switchProject(card.dataset.project));
    });
    
    // Project filter
    const projectFilter = document.getElementById('project-filter');
    if (projectFilter) {
        projectFilter.addEventListener('change', (e) => switchProject(e.target.value));
    }
    
    // File upload
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    
    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('border-blue-500');
    });
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('border-blue-500');
    });
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-blue-500');
        handleFileUpload(Array.from(e.dataTransfer.files));
    });
    
    fileInput.addEventListener('change', (e) => {
        handleFileUpload(Array.from(e.target.files));
    });
    
    // Action buttons
    document.getElementById('save-btn')?.addEventListener('click', () => {
        showToast('Données sauvegardées avec succès');
    });
    
    document.getElementById('print-btn')?.addEventListener('click', () => {
        window.print();
    });
    
    // Initialize
    checkBackendStatus();
    switchProject('kahnawake');
    switchTab('dashboard');
    
    // Auto-refresh status every 30 seconds
    setInterval(checkBackendStatus, 30000);
});

// CSS styles for nav and project cards
const styles = `
.nav-btn {
    display: flex;
    align-items: center;
    width: 100%;
    padding: 0.75rem 1rem;
    text-left;
    background: none;
    border: none;
    border-radius: 0.5rem;
    color: #9CA3AF;
    font-size: 0.875rem;
    font-weight: 500;
    transition: all 0.2s ease;
    cursor: pointer;
}

.nav-btn:hover {
    background-color: #374151;
    color: #F3F4F6;
}

.nav-btn.active {
    background-color: #1F2937;
    color: #3B82F6;
}

.project-card {
    padding: 0.75rem;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid transparent;
}

.project-card:hover {
    background-color: #374151;
}

.project-card.active {
    background-color: #1F2937;
    border-color: #3B82F6;
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}

.status-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    line-height: 1.25;
    text-align: center;
    white-space: nowrap;
}
`;

// Inject styles
const styleSheet = document.createElement('style');
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);