-- =============================================================================
-- PGI-IA DATABASE SCHEMA EXTENDED - Phase Réaliste
-- Foundation pour tous les développements critiques
-- Date: 11/07/2025 13:45
-- =============================================================================

-- Table projets étendue
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(20) UNIQUE NOT NULL,          -- S-1086, C-24-048
    nom VARCHAR(255) NOT NULL,                 -- Musée Kahnawake
    client VARCHAR(100),                       -- QMD, JCB
    statut VARCHAR(50),                        -- Estimation, Construction
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_maj DATETIME DEFAULT CURRENT_TIMESTAMP,
    po_client VARCHAR(100),                    -- Personne contact client
    plan_principal_path VARCHAR(500),          -- Chemin vers plan principal
    plan_principal_gps_bounds TEXT,            -- JSON bounds GPS du plan
    metadata TEXT                              -- JSON métadonnées projet
);

-- Table réunions et transcriptions audio
CREATE TABLE IF NOT EXISTS meetings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    titre VARCHAR(255),
    date_reunion DATETIME NOT NULL,
    duree_minutes INTEGER,
    audio_file_path VARCHAR(500),              -- Chemin fichier audio original
    transcription_text TEXT,                   -- Texte transcrit complet
    transcription_summary TEXT,                -- Résumé IA de la réunion
    participants TEXT,                         -- JSON liste participants
    action_items TEXT,                         -- JSON actions à faire
    status VARCHAR(50) DEFAULT 'pending',      -- pending, transcribed, processed
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Table notes intelligentes par projet
CREATE TABLE IF NOT EXISTS project_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    note_originale TEXT NOT NULL,              -- Note écrite par utilisateur
    note_reformulee TEXT,                      -- Note reformulée par IA
    note_finale TEXT,                          -- Note finale après approbation
    categorie VARCHAR(100),                    -- Technique, Administratif, etc.
    statut VARCHAR(50) DEFAULT 'draft',        -- draft, reformulated, approved
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_approbation DATETIME,
    metadata TEXT,                             -- JSON métadonnées supplémentaires
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Table photos géolocalisées
CREATE TABLE IF NOT EXISTS photos_geolocated (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    gps_latitude DECIMAL(10, 8),               -- GPS iPhone
    gps_longitude DECIMAL(11, 8),              -- GPS iPhone
    gps_altitude DECIMAL(8, 3),                -- Altitude si disponible
    plan_x_coordinate DECIMAL(10, 3),          -- Position X sur plan principal
    plan_y_coordinate DECIMAL(10, 3),          -- Position Y sur plan principal
    description TEXT,                          -- Description photo
    date_prise DATETIME,                       -- Date prise photo (EXIF)
    date_upload DATETIME DEFAULT CURRENT_TIMESTAMP,
    metadata_exif TEXT,                        -- JSON métadonnées EXIF complètes
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Table fichiers CAD et plans
CREATE TABLE IF NOT EXISTS cad_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_path VARCHAR(500),                -- Fichier PDF original
    dwg_path VARCHAR(500),                     -- Fichier DWG converti
    model_3d_path VARCHAR(500),                -- Modèle 3D généré
    file_type VARCHAR(20),                     -- pdf, dwg, 3d, etc.
    conversion_status VARCHAR(50) DEFAULT 'pending', -- pending, converted, error
    plan_bounds TEXT,                          -- JSON coordonnées du plan
    extraction_metadata TEXT,                 -- JSON données extraites
    date_upload DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_conversion DATETIME,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Table chemins de canalisations
CREATE TABLE IF NOT EXISTS cable_paths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    cad_file_id INTEGER,
    path_name VARCHAR(255),                    -- Nom du chemin
    path_type VARCHAR(100),                    -- Type canalisation
    path_coordinates TEXT NOT NULL,            -- JSON coordonnées 3D du chemin
    suggested_by VARCHAR(50),                  -- user, ai_suggestion
    validation_status VARCHAR(50) DEFAULT 'draft', -- draft, validated, rejected
    cost_estimate DECIMAL(10, 2),              -- Estimation coût
    notes TEXT,                                -- Notes sur le chemin
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_validation DATETIME,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (cad_file_id) REFERENCES cad_files(id)
);

-- Table emails existante étendue
CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    message_id VARCHAR(255) UNIQUE,
    subject VARCHAR(255),
    sender VARCHAR(255),
    recipient VARCHAR(255),
    date_received DATETIME,
    body_text TEXT,
    body_html TEXT,
    classification VARCHAR(100),               -- DIRECTIVE, PLAN, CHANGEMENT, etc.
    confidence_score DECIMAL(3, 2),           -- Score confiance classification
    has_attachments BOOLEAN DEFAULT FALSE,
    attachments_processed BOOLEAN DEFAULT FALSE,
    status VARCHAR(50) DEFAULT 'new',          -- new, processed, archived
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Table directives existante étendue
CREATE TABLE IF NOT EXISTS directives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    numero_directive VARCHAR(50) UNIQUE,
    date_recue DATE NOT NULL,
    description TEXT NOT NULL,
    po_client VARCHAR(100),
    prix DECIMAL(10, 2),
    statut VARCHAR(50) DEFAULT 'À préparer',
    source_type VARCHAR(50) DEFAULT 'manual',  -- manual, email, upload
    source_reference VARCHAR(255),            -- Référence source (email_id, etc.)
    ai_enhanced BOOLEAN DEFAULT FALSE,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_maj DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- =============================================================================
-- INDEX POUR PERFORMANCE
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_projects_code ON projects(code);
CREATE INDEX IF NOT EXISTS idx_meetings_project ON meetings(project_id);
CREATE INDEX IF NOT EXISTS idx_meetings_date ON meetings(date_reunion);
CREATE INDEX IF NOT EXISTS idx_notes_project ON project_notes(project_id);
CREATE INDEX IF NOT EXISTS idx_notes_status ON project_notes(statut);
CREATE INDEX IF NOT EXISTS idx_photos_project ON photos_geolocated(project_id);
CREATE INDEX IF NOT EXISTS idx_photos_gps ON photos_geolocated(gps_latitude, gps_longitude);
CREATE INDEX IF NOT EXISTS idx_cad_project ON cad_files(project_id);
CREATE INDEX IF NOT EXISTS idx_cad_status ON cad_files(conversion_status);
CREATE INDEX IF NOT EXISTS idx_paths_project ON cable_paths(project_id);
CREATE INDEX IF NOT EXISTS idx_emails_project ON emails(project_id);
CREATE INDEX IF NOT EXISTS idx_emails_classification ON emails(classification);

-- =============================================================================
-- DONNÉES INITIALES
-- =============================================================================

-- Projets existants
INSERT OR REPLACE INTO projects (code, nom, client, statut, po_client) VALUES
('S-1086', 'Musée Kahnawake', 'QMD', 'Estimation', 'Jean-Claude Beaumont'),
('C-24-048', 'Place Alexis-Nihon', 'JCB', 'Construction', 'Marie Tremblay');

-- =============================================================================
-- VUES POUR FACILITER LES REQUÊTES
-- =============================================================================

-- Vue projet complet avec statistiques
CREATE VIEW IF NOT EXISTS project_overview AS
SELECT 
    p.*,
    COUNT(DISTINCT m.id) as meetings_count,
    COUNT(DISTINCT n.id) as notes_count,
    COUNT(DISTINCT ph.id) as photos_count,
    COUNT(DISTINCT c.id) as cad_files_count,
    COUNT(DISTINCT e.id) as emails_count
FROM projects p
LEFT JOIN meetings m ON p.id = m.project_id
LEFT JOIN project_notes n ON p.id = n.project_id  
LEFT JOIN photos_geolocated ph ON p.id = ph.project_id
LEFT JOIN cad_files c ON p.id = c.project_id
LEFT JOIN emails e ON p.id = e.project_id
GROUP BY p.id;

-- Vue activité récente par projet
CREATE VIEW IF NOT EXISTS recent_activity AS
SELECT 
    'meeting' as activity_type,
    m.project_id,
    m.titre as title,
    m.date_creation as activity_date
FROM meetings m
UNION ALL
SELECT 
    'note' as activity_type,
    n.project_id,
    SUBSTR(n.note_originale, 1, 50) || '...' as title,
    n.date_creation as activity_date
FROM project_notes n
UNION ALL  
SELECT 
    'photo' as activity_type,
    ph.project_id,
    ph.filename as title,
    ph.date_upload as activity_date
FROM photos_geolocated ph
ORDER BY activity_date DESC;