/**
 * PGI-IA Frontend JavaScript
 * Interface hub central avec agents IA
 */

// Configuration
const API_BASE = 'http://localhost:5000';

// Données projets (simulées pour démo)  
const projects = {
    kahnawake: {
        title: "S-1086 - Musée Kahnawake",
        po_column: "NO. PO QMD",
        directives: [
            { id: 'CD-050', date: '2024-12-15', description: 'Ajout 3 prises 120V local 201', prix: '$ 324,87', po: '2025-001', statut: 'Approuvé' },
            { id: 'CO-ME-12', date: '2024-12-18', description: 'Modification panneau PCE-03', prix: '$ 1,247,32', po: '2025-003', statut: 'Approuvé' },
            { id: 'CD-051', date: '2024-12-20', description: 'Installation éclairage urgence', prix: '$ 867,45', po: '', statut: 'À préparer' },
            { id: 'CO-ME-13', date: '2024-12-22', description: 'Déplacement interrupteurs hall', prix: '$ 2,063,43', po: '2025-005', statut: 'Approuvé' }
        ],
        timeline: [
            { icon: 'fa-file-pdf', title: 'Plan E-101 Rev A reçu', body: 'Fichier PDF du plan électrique principal déposé.', time: '08:15' },
            { icon: 'fa-cogs', title: 'Agent IA activé', body: 'Traitement automatique du plan E-101 initié.', time: '08:16', color: 'var(--accent-orange)' },
            { icon: 'fa-cube', title: 'Jumeau Numérique mis à jour', body: 'Géométrie 3D intégrée avec succès.', time: '08:25', color: 'var(--accent-blue)' }
        ]
    },
    alexis_nihon: {
        title: "C-24-048 - Place Alexis-Nihon",
        po_column: "NO. PO JCB", 
        directives: [
            { id: 'CD-100', date: '2024-12-10', description: 'Ajout prises étage 3 local 304', prix: '$ 1,456,78', po: 'JCB-2024-089', statut: 'Approuvé' },
            { id: 'CO-ME-25', date: '2024-12-14', description: 'Modification éclairage hall principal', prix: '$ 3,247,91', po: 'JCB-2024-092', statut: 'Approuvé' },
            { id: 'CD-101', date: '2024-12-16', description: 'Installation panneau distribution B-12', prix: '$ 5,789,45', po: 'JCB-2024-095', statut: 'Approuvé' },
            { id: 'CO-ME-26', date: '2024-12-19', description: 'Déplacement conduits garage sous-sol', prix: '$ 2,134,67', po: '', statut: 'À préparer' },
            { id: 'CD-102', date: '2024-12-21', description: 'Ajout système détection incendie', prix: '$ 4,567,23', po: 'JCB-2024-098', statut: 'Approuvé' }
        ],
        timeline: [
            { icon: 'fa-camera', title: 'Photos chantier reçues', body: '3 photos géolocalisées ajoutées automatiquement.', time: '10:30' },
            { icon: 'fa-file-signature', title: 'Directive CD-102 traitée', body: 'Extraction données et intégration tableau terminées.', time: '11:15', color: 'var(--accent-green)' }
        ]
    }
};

let currentProject = 'kahnawake';
let currentTab = 'timeline';