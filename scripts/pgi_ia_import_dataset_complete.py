#!/usr/bin/env python3
"""
Import complet du dataset OneDrive pour PGI-IA
Spécialisé pour construction électrique Québec
"""

import os
import sys
import sqlite3
import json
import re
import hashlib
from datetime import datetime
from pathlib import Path
import fitz  # PyMuPDF for PDF text extraction
import openpyxl
from collections import defaultdict

# Configuration
DATASET_BASE = "/mnt/c/Users/fvegi/OneDrive/Desktop/dataset"
DB_PATH = "/root/dev/pgi-ia/database.db"
OUTPUT_JSONL = "/mnt/c/Users/fvegi/deepseek_training_quebec_construction.jsonl"

# Patterns pour extraction
PROJECT_PATTERN = re.compile(r'C(\d{2})-(\d{3})\s*-\s*(.+)')
DIRECTIVE_PATTERN = re.compile(r'(PCE|ODT|DIR)-?(\d+)', re.IGNORECASE)
DRAWING_PATTERN = re.compile(r'([A-Z])-(\d{3,4})')
DATE_PATTERN = re.compile(r'(\d{4}[-/]\d{2}[-/]\d{2})')

# Mapping types de documents
DOCUMENT_TYPES = {
    'plan': ['dwg', 'pdf'],
    'devis': ['pdf', 'doc', 'docx'],
    'directive': ['pdf', 'doc'],
    'photo': ['jpg', 'jpeg', 'png'],
    'calcul': ['xls', 'xlsx'],
    'soumission': ['pdf', 'xls', 'xlsx'],
    'ccq': ['pdf'],
    'permis': ['pdf'],
    'email': ['msg', 'eml']
}

class QuebecDatasetImporter:
    def __init__(self):
        self.stats = defaultdict(int)
        self.training_data = []
        self.projects = {}
        self.documents = []
        self.notes = []
        
    def connect_db(self):
        """Connexion à la base SQLite"""
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        
        # Créer tables si n'existent pas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                project_id TEXT,
                filename TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        ''')
        
        self.conn.commit()
        
    def parse_project_folder(self, folder_name):
        """Extraire infos du nom de dossier projet"""
        match = PROJECT_PATTERN.match(folder_name)
        if match:
            year = match.group(1)
            number = match.group(2)
            name = match.group(3).strip()
            return {
                'code': f"C{year}-{number}",
                'year': f"20{year}",
                'name': name,
                'full_name': folder_name
            }
        return None
        
    def extract_pdf_text(self, file_path, max_pages=5):
        """Extraire texte des premières pages d'un PDF"""
        try:
            doc = fitz.open(file_path)
            text = ""
            for i, page in enumerate(doc):
                if i >= max_pages:
                    break
                text += page.get_text()
            doc.close()
            return text[:2000]  # Limiter à 2000 caractères
        except:
            return ""
            
    def extract_excel_data(self, file_path):
        """Extraire données pertinentes d'Excel"""
        try:
            wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
            data = []
            
            for sheet in wb.worksheets[:3]:  # Max 3 feuilles
                for row in sheet.iter_rows(max_row=20, values_only=True):
                    if any(cell for cell in row if cell):
                        data.append([str(cell) if cell else "" for cell in row])
                        
            wb.close()
            return json.dumps(data, ensure_ascii=False)[:1000]
        except:
            return ""
            
    def categorize_document(self, file_path, folder_context):
        """Catégoriser document selon son contexte"""
        file_lower = file_path.lower()
        folder_lower = folder_context.lower()
        
        if 'directive' in folder_lower or any(p in file_lower for p in ['pce-', 'odt-', 'dir-']):
            return 'directive'
        elif 'plan' in folder_lower or 'devis' in folder_lower:
            return 'plan_devis'
        elif 'soumission' in folder_lower or 'estimation' in folder_lower:
            return 'soumission'
        elif 'ccq' in folder_lower or 'cnesst' in folder_lower:
            return 'reglementation'
        elif 'photo' in folder_lower:
            return 'photo'
        elif 'permis' in folder_lower or 'hydro' in folder_lower:
            return 'permis'
        elif 'facture' in folder_lower or 'comptabilite' in folder_lower:
            return 'comptabilite'
        else:
            return 'general'
            
    def process_project_folder(self, project_path, project_info):
        """Traiter un dossier projet complet"""
        print(f"  📂 Traitement: {project_info['code']} - {project_info['name']}")
        
        project_docs = []
        project_training = []
        
        for root, dirs, files in os.walk(project_path):
            rel_path = os.path.relpath(root, project_path)
            
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = file.split('.')[-1].lower()
                
                if file_ext in ['pdf', 'dwg', 'xls', 'xlsx', 'doc', 'docx']:
                    self.stats[f'files_{file_ext}'] += 1
                    
                    # Créer document
                    doc_id = hashlib.md5(file_path.encode()).hexdigest()[:12]
                    doc_type = self.categorize_document(file, rel_path)
                    
                    doc = {
                        'id': doc_id,
                        'project_id': project_info['code'],
                        'filename': file,
                        'type': doc_type,
                        'path': rel_path,
                        'size': os.path.getsize(file_path),
                        'created': datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()
                    }
                    
                    # Extraction contenu selon type
                    if file_ext == 'pdf' and doc['size'] < 10_000_000:  # < 10MB
                        content = self.extract_pdf_text(file_path)
                        if content and len(content) > 100:
                            doc['content_preview'] = content
                            
                            # Générer exemple de formation
                            if doc_type == 'directive':
                                directive_match = DIRECTIVE_PATTERN.search(file)
                                if directive_match:
                                    training_example = self.generate_directive_training(
                                        project_info, directive_match.group(0), content
                                    )
                                    if training_example:
                                        project_training.append(training_example)
                                        
                    elif file_ext in ['xls', 'xlsx'] and doc['size'] < 5_000_000:
                        content = self.extract_excel_data(file_path)
                        if content:
                            doc['content_preview'] = content
                            
                    project_docs.append(doc)
                    
        return project_docs, project_training
        
    def generate_directive_training(self, project, directive_num, content):
        """Générer exemple de formation pour directive"""
        # Extraire infos clés du contenu
        montant_match = re.search(r'(\d{1,3}(?:\s?\d{3})*(?:[,\.]\d{2})?)\s*\$', content)
        montant = montant_match.group(1) if montant_match else "À déterminer"
        
        # Identifier type de changement
        keywords = {
            'ajout': ['ajout', 'supplémentaire', 'nouveau'],
            'modification': ['modifier', 'remplacer', 'changer'],
            'crédit': ['crédit', 'économie', 'retrait'],
            'urgence': ['urgent', 'immédiat', 'sécurité']
        }
        
        change_type = 'standard'
        for typ, words in keywords.items():
            if any(word in content.lower() for word in words):
                change_type = typ
                break
                
        example = {
            "messages": [
                {
                    "role": "system",
                    "content": "Tu es l'assistant PGI-IA spécialisé en gestion de projets électriques au Québec. Tu connais les procédures CCQ et les standards de l'industrie."
                },
                {
                    "role": "user",
                    "content": f"Comment gérer la directive {directive_num} sur le projet {project['name']}?"
                },
                {
                    "role": "assistant",
                    "content": f"Pour la directive {directive_num} du projet {project['code']} - {project['name']}:\n\n📋 **Type**: Changement {change_type}\n💰 **Impact estimé**: {montant}\n\n**Actions à prendre**:\n1. Documenter le changement dans le registre des directives\n2. Obtenir l'approbation écrite du client\n3. Mettre à jour le budget du projet\n4. Informer les équipes terrain concernées\n5. Ajuster le calendrier si nécessaire\n\n⚠️ Important: Selon les normes CCQ, toute directive doit être documentée dans les 48h et approuvée avant exécution."
                }
            ]
        }
        
        return example
        
    def generate_project_training(self, project_info, doc_count, doc_types):
        """Générer exemples de formation pour projet complet"""
        examples = []
        
        # Exemple 1: Vue d'ensemble projet
        examples.append({
            "messages": [
                {
                    "role": "system",
                    "content": "Tu es l'assistant PGI-IA pour la gestion de projets électriques québécois."
                },
                {
                    "role": "user", 
                    "content": f"Donne-moi le statut du projet {project_info['name']}"
                },
                {
                    "role": "assistant",
                    "content": f"**Projet {project_info['code']} - {project_info['name']}**\n\n📊 **Statut**: En cours\n📁 **Documents**: {doc_count} fichiers\n📋 **Types de documents**:\n" + "\n".join([f"  • {typ}: {count}" for typ, count in doc_types.items()]) + f"\n\n💡 **Points d'attention**:\n- Vérifier les directives récentes\n- S'assurer que les plans sont à jour\n- Valider les soumissions avec le client"
                }
            ]
        })
        
        # Exemple 2: Recherche spécifique
        if 'directive' in doc_types and doc_types['directive'] > 0:
            examples.append({
                "messages": [
                    {
                        "role": "system",
                        "content": "Tu es l'assistant PGI-IA expert en directives de changement."
                    },
                    {
                        "role": "user",
                        "content": f"Combien de directives pour {project_info['code']}?"
                    },
                    {
                        "role": "assistant",
                        "content": f"Le projet {project_info['code']} compte actuellement **{doc_types.get('directive', 0)} directives** documentées.\n\n📌 **Gestion des directives**:\n- Toutes les directives doivent être approuvées par écrit\n- Un registre chronologique est maintenu\n- L'impact budgétaire est évalué pour chaque changement\n- Les délais sont ajustés selon l'ampleur des modifications\n\nVoulez-vous voir le détail d'une directive spécifique?"
                    }
                ]
            })
            
        return examples
        
    def import_dataset(self):
        """Import principal du dataset"""
        print("🚀 IMPORT DATASET CONSTRUCTION ÉLECTRIQUE QUÉBEC")
        print("=" * 60)
        
        self.connect_db()
        
        # Explorer projets actifs
        active_projects_path = os.path.join(DATASET_BASE, "Contrats de Projets - En cours")
        
        if not os.path.exists(active_projects_path):
            print(f"❌ Erreur: {active_projects_path} n'existe pas")
            return
            
        # Lister tous les projets
        project_folders = [d for d in os.listdir(active_projects_path) 
                          if os.path.isdir(os.path.join(active_projects_path, d))]
        
        print(f"\n📁 Projets trouvés: {len(project_folders)}")
        
        # Traiter chaque projet
        for folder in sorted(project_folders):
            project_info = self.parse_project_folder(folder)
            
            if not project_info:
                print(f"  ⚠️ Format non reconnu: {folder}")
                continue
                
            project_path = os.path.join(active_projects_path, folder)
            
            # Focus sur Kahnawake et Alexis Nihon
            is_priority = ('kahnawake' in folder.lower() or 
                          'alexis' in folder.lower() or
                          'C24-060' in folder or 
                          'C24-048' in folder)
                          
            if is_priority:
                print(f"\n⭐ PROJET PRIORITAIRE: {project_info['code']}")
                
            # Créer projet dans DB
            self.cursor.execute('''
                INSERT OR REPLACE INTO projects (id, name, description, status)
                VALUES (?, ?, ?, ?)
            ''', (
                project_info['code'],
                project_info['name'],
                f"{project_info['full_name']} - Import: {datetime.now().strftime('%Y-%m-%d')}",
                'active'
            ))
            
            # Traiter documents
            docs, training = self.process_project_folder(project_path, project_info)
            
            # Insérer documents
            for doc in docs[:100]:  # Limiter à 100 docs par projet pour test
                self.cursor.execute('''
                    INSERT OR REPLACE INTO documents 
                    (id, project_id, filename, content, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    doc['id'],
                    doc['project_id'],
                    doc['filename'],
                    doc.get('content_preview', f"{doc['type']} - {doc['path']}"),
                    doc['created']
                ))
                
            # Ajouter training data
            self.training_data.extend(training)
            
            # Générer training général pour le projet
            doc_types = defaultdict(int)
            for doc in docs:
                doc_types[doc['type']] += 1
                
            project_training = self.generate_project_training(project_info, len(docs), dict(doc_types))
            self.training_data.extend(project_training)
            
            self.stats['projects'] += 1
            self.stats['documents'] += len(docs)
            self.stats['training_examples'] += len(training) + len(project_training)
            
            # Limiter pour test initial
            if self.stats['projects'] >= 5 and not is_priority:
                print("\n📊 Limite de test atteinte (5 projets)")
                break
                
        # Ajouter exemples de formation génériques Québec
        self.add_quebec_specific_training()
        
        # Sauvegarder
        self.conn.commit()
        self.save_training_data()
        
        # Afficher statistiques
        self.print_statistics()
        
    def add_quebec_specific_training(self):
        """Ajouter formation spécifique Québec"""
        quebec_examples = [
            {
                "messages": [
                    {"role": "system", "content": "Tu es PGI-IA, assistant expert en construction électrique au Québec."},
                    {"role": "user", "content": "Quelles sont les exigences CCQ pour un chantier?"},
                    {"role": "assistant", "content": "**Exigences CCQ pour chantiers électriques au Québec**:\n\n📋 **Documentation obligatoire**:\n• Cartes de compétence CCQ valides pour tous les travailleurs\n• Ratio compagnon/apprenti respecté (1:1 ou selon métier)\n• Registre des heures travaillées\n• Preuve d'assurance responsabilité\n\n👷 **Sur le chantier**:\n• Affichage du certificat de conformité CCQ\n• Respect des taux horaires selon la convention\n• Paiement des avantages sociaux (13-15%)\n• Formation SST à jour\n\n⚠️ **Inspections**:\n• L'inspecteur CCQ peut visiter sans préavis\n• Amendes de 1 029$ à 20 569$ par infraction\n• Vérification des qualifications et ratios\n\n💡 Conseil: Utilisez PGI-IA pour maintenir votre documentation CCQ à jour!"}
                ]
            },
            {
                "messages": [
                    {"role": "system", "content": "Tu es PGI-IA, spécialisé en permis Hydro-Québec."},
                    {"role": "user", "content": "Délais pour un branchement 600V triphasé?"},
                    {"role": "assistant", "content": "**Délais Hydro-Québec - Branchement 600V triphasé**:\n\n⏱️ **Délais standards**:\n• Demande initiale: 2-3 jours ouvrables\n• Étude technique: 15-20 jours\n• Approbation finale: 5-10 jours\n• Installation: 30-45 jours après paiement\n\n**Total: 8-12 semaines** en conditions normales\n\n📋 **Documents requis**:\n• Plan unifilaire signé par ingénieur\n• Calcul de charge détaillé\n• Plan d'implantation\n• Preuve d'assurance\n• Licence RBQ du maître électricien\n\n⚡ **Facteurs d'accélération**:\n• Dossier complet dès le départ (-2 semaines)\n• Paiement rapide des frais (-1 semaine)\n• Coordination avec ingénieur HQ\n\n🚨 **Attention**: Projets autochtones peuvent avoir des délais supplémentaires (2-4 semaines)"}
                ]
            },
            {
                "messages": [
                    {"role": "system", "content": "Tu es PGI-IA, expert en facturation First Nations."},
                    {"role": "user", "content": "Comment facturer à Kahnawake?"},
                    {"role": "assistant", "content": "**Facturation projets Kahnawake - Procédure spéciale**:\n\n💰 **Exemptions fiscales**:\n• Aucune TPS/TVQ sur travaux en territoire\n• Numéro d'exemption requis sur facture\n• Mention obligatoire: \"Projet en territoire Mohawk - Exempt de taxes\"\n\n📄 **Format de facture**:\n```\nDR ÉLECTRIQUE INC.\nFacture #2024-XXX\n\nClient: [Nom de l'organisation]\nProjet: C24-060 - Centre Culturel Kahnawake\nLieu: Territoire Mohawk de Kahnawake\n\nTravaux: [Description]\nMontant: 10 000.00$\nTPS: EXEMPT - Territoire autochtone\nTVQ: EXEMPT - Territoire autochtone\nTOTAL: 10 000.00$\n```\n\n⚠️ **Important**:\n• Conserver preuve de l'exemption\n• Main d'œuvre locale = priorité\n• Respecter Fair Wage Policy\n• Paiement souvent par chèque certifié"}
                ]
            }
        ]
        
        self.training_data.extend(quebec_examples)
        
    def save_training_data(self):
        """Sauvegarder données de formation"""
        print(f"\n💾 Sauvegarde de {len(self.training_data)} exemples...")
        
        with open(OUTPUT_JSONL, 'w', encoding='utf-8') as f:
            for example in self.training_data:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
                
        print(f"✅ Training data sauvegardé: {OUTPUT_JSONL}")
        
    def print_statistics(self):
        """Afficher statistiques d'import"""
        print("\n" + "=" * 60)
        print("📊 STATISTIQUES D'IMPORT")
        print("=" * 60)
        
        for key, value in sorted(self.stats.items()):
            print(f"{key}: {value:,}")
            
        print(f"\n✅ Import terminé avec succès!")
        print(f"🎯 Projets prioritaires traités: Kahnawake, Alexis Nihon")
        print(f"📚 Exemples de formation créés: {len(self.training_data)}")

if __name__ == "__main__":
    importer = QuebecDatasetImporter()
    importer.import_dataset()