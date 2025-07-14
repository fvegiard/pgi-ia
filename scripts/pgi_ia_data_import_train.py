#!/usr/bin/env python3
"""
PGI-IA Data Import & DeepSeek Training Script
Import des projets Kahnawake et Alexis Nihon + entrainement DeepSeek
"""

import os
import sys
import sqlite3
import json
import hashlib
import shutil
from datetime import datetime, timedelta
import random
from pathlib import Path
import PyPDF2

# Paths
DATASET_BASE = "/mnt/c/Users/fvegi/OneDrive/Desktop/dataset/Contrats de Projets - En cours"
KAHNAWAKE_PATH = os.path.join(DATASET_BASE, "C24-060 - Centre Culturel Kahnawake - Les Entreprises QMD")
ALEXIS_PATH = os.path.join(DATASET_BASE, "C24-048 - Place Alexis-Nihon")
DB_PATH = "/root/dev/pgi-ia/pgi_ia.db"
UPLOAD_DIR = "/root/dev/pgi-ia/uploads"
TRAINING_FILE = "/mnt/c/Users/fvegi/deepseek_training_dataset.jsonl"

class DataImporter:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.training_data = []
        self.ensure_upload_dir()
        
    def ensure_upload_dir(self):
        """Créer le dossier uploads si nécessaire"""
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
    def clear_existing_data(self):
        """Nettoyer les données existantes"""
        print("🧹 Nettoyage des données existantes...")
        tables = ['documents', 'projects', 'notes', 'agents', 'system_logs']
        for table in tables:
            self.cursor.execute(f"DELETE FROM {table}")
        self.conn.commit()
        print("✅ Base de données nettoyée")
        
    def import_projects(self):
        """Importer les projets Kahnawake et Alexis Nihon"""
        print("\n📁 Import des projets...")
        
        projects = [
            {
                'id': 'C24-060',
                'name': 'Centre Culturel Kahnawake',
                'client': 'Les Entreprises QMD',
                'status': 'Construction',
                'budget': 1250000.00,
                'start_date': '2024-03-15',
                'end_date': '2025-09-30',
                'completion': 35,
                'path': KAHNAWAKE_PATH
            },
            {
                'id': 'C24-048',
                'name': 'Place Alexis-Nihon Phase 3',
                'client': 'Cominar REIT',
                'status': 'Estimation',
                'budget': 850000.00,
                'start_date': '2024-06-01',
                'end_date': '2025-12-15',
                'completion': 15,
                'path': ALEXIS_PATH
            }
        ]
        
        for project in projects:
            # Compter les PDFs
            pdf_count = len(list(Path(project['path']).rglob('*.pdf')))
            
            # Adapter au schéma existant
            metadata = {
                'client': project['client'],
                'budget': project['budget'],
                'start_date': project['start_date'],
                'end_date': project['end_date'],
                'completion': project['completion'],
                'pdf_count': pdf_count,
                'source_path': project['path']
            }
            
            self.cursor.execute('''
                INSERT OR REPLACE INTO projects 
                (id, name, description, status)
                VALUES (?, ?, ?, ?)
            ''', (
                project['id'],
                project['name'],
                f"{project['client']} - Budget: ${project['budget']:,.0f}",
                project['status']
            ))
            
            print(f"✅ Projet {project['id']}: {project['name']} ({pdf_count} PDFs)")
            
            # Données pour entrainement DeepSeek
            self.training_data.append({
                "messages": [
                    {"role": "system", "content": "Tu es un assistant IA spécialisé en gestion de projets de construction électrique."},
                    {"role": "user", "content": f"Quel est le statut du projet {project['name']}?"},
                    {"role": "assistant", "content": f"Le projet {project['name']} (code {project['id']}) pour {project['client']} est actuellement en phase de {project['status']}. Budget: {project['budget']:,.2f}$ CAD, Avancement: {project['completion']}%. Période: {project['start_date']} à {project['end_date']}. Nous avons {pdf_count} documents PDF associés à ce projet."}
                ]
            })
            
        self.conn.commit()
        
    def import_sample_documents(self, limit_per_project=50):
        """Importer un échantillon de documents PDF"""
        print(f"\n📄 Import de {limit_per_project} documents par projet...")
        
        for project_id, project_path in [('C24-060', KAHNAWAKE_PATH), ('C24-048', ALEXIS_PATH)]:
            # Trouver tous les PDFs
            pdf_files = list(Path(project_path).rglob('*.pdf'))
            
            # Prioriser les fichiers importants
            priority_keywords = ['plan', 'devis', 'directive', 'soumission', 'facture', 'rapport']
            
            # Trier par priorité
            priority_pdfs = []
            other_pdfs = []
            
            for pdf in pdf_files:
                if any(keyword in pdf.name.lower() for keyword in priority_keywords):
                    priority_pdfs.append(pdf)
                else:
                    other_pdfs.append(pdf)
            
            # Sélectionner les PDFs à importer
            selected_pdfs = priority_pdfs[:limit_per_project//2] + other_pdfs[:limit_per_project//2]
            
            for idx, pdf_path in enumerate(selected_pdfs[:limit_per_project]):
                try:
                    # Calculer hash
                    with open(pdf_path, 'rb') as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                    
                    # Copier vers uploads
                    dest_name = f"{project_id}_{idx:03d}_{pdf_path.name}"
                    dest_path = os.path.join(UPLOAD_DIR, dest_name)
                    shutil.copy2(pdf_path, dest_path)
                    
                    # Extraire metadata
                    file_size = os.path.getsize(pdf_path)
                    relative_path = str(pdf_path).replace(project_path, '')
                    
                    # Déterminer le type de document
                    doc_type = 'Autre'
                    for keyword in priority_keywords:
                        if keyword in pdf_path.name.lower():
                            doc_type = keyword.capitalize()
                            break
                    
                    # Insérer dans la base
                    self.cursor.execute('''
                        INSERT INTO documents 
                        (project_id, name, type, file_path, file_size, hash, upload_date, analyzed, metadata)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        project_id,
                        pdf_path.name,
                        doc_type,
                        dest_name,
                        file_size,
                        file_hash,
                        datetime.now().isoformat(),
                        0,  # Non analysé
                        json.dumps({
                            'original_path': str(pdf_path),
                            'relative_path': relative_path,
                            'pages': self.get_pdf_pages(pdf_path)
                        })
                    ))
                    
                    # Données pour entrainement
                    self.training_data.append({
                        "messages": [
                            {"role": "system", "content": "Tu es un assistant IA expert en analyse de documents de construction électrique."},
                            {"role": "user", "content": f"J'ai un document {doc_type} nommé '{pdf_path.name}' pour le projet {project_id}. Que peux-tu me dire?"},
                            {"role": "assistant", "content": f"Ce document '{pdf_path.name}' est un {doc_type} du projet {project_id}. Il fait {file_size/1024:.1f} KB et contient des informations importantes pour le projet. Le chemin relatif est: {relative_path}. Je peux analyser son contenu pour extraire les informations clés comme les spécifications techniques, les coûts, ou les directives de construction."}
                        ]
                    })
                    
                    if idx % 10 == 0:
                        print(f"  → {idx+1}/{limit_per_project} documents importés pour {project_id}")
                        
                except Exception as e:
                    print(f"  ⚠️ Erreur import {pdf_path.name}: {str(e)}")
                    
        self.conn.commit()
        print("✅ Documents importés")
        
    def get_pdf_pages(self, pdf_path):
        """Obtenir le nombre de pages d'un PDF"""
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                return len(reader.pages)
        except:
            return 0
            
    def generate_sample_notes(self):
        """Générer des notes terrain réalistes"""
        print("\n📝 Génération de notes terrain...")
        
        note_templates = [
            {
                'type': 'Déficience',
                'templates': [
                    "Panneau {location} non conforme - manque identification circuits",
                    "Conduits {location} mal fixés - refaire supports",
                    "Boîte jonction {location} sans couvercle - sécurité",
                    "Câblage {location} non protégé - ajouter gaine"
                ]
            },
            {
                'type': 'Directive',
                'templates': [
                    "Installer {count} prises {type} au {location}",
                    "Déplacer panneau de {old_location} vers {new_location}",
                    "Ajouter éclairage d'urgence {location}",
                    "Remplacer disjoncteur {size}A par {new_size}A panneau {panel}"
                ]
            },
            {
                'type': 'Inspection',
                'templates': [
                    "Installation {location} complétée - conforme plans",
                    "Test continuité circuits {panel} - OK",
                    "Vérification mise à terre {location} - résistance {ohms}Ω",
                    "Inspection finale {area} - {count} déficiences mineures"
                ]
            }
        ]
        
        locations = ['local 101', 'corridor 2e', 'salle mécanique', 'bureau admin', 'entrepôt', 'cafétéria']
        
        for project_id in ['C24-060', 'C24-048']:
            for i in range(30):  # 30 notes par projet
                note_type = random.choice(note_templates)
                template = random.choice(note_type['templates'])
                
                # Remplir le template
                note_text = template.format(
                    location=random.choice(locations),
                    count=random.randint(2, 10),
                    type=random.choice(['duplex', 'GFCI', 'USB', '20A']),
                    old_location='local ' + str(random.randint(100, 200)),
                    new_location='local ' + str(random.randint(201, 300)),
                    size=random.choice([15, 20, 30]),
                    new_size=random.choice([20, 30, 40]),
                    panel='P' + str(random.randint(1, 5)),
                    ohms=round(random.uniform(0.1, 2.0), 1),
                    area=random.choice(['étage 1', 'étage 2', 'sous-sol'])
                )
                
                # Note reformulée par IA
                reformulated = f"**{note_type['type']} - {datetime.now().strftime('%Y-%m-%d')}**\n\n"
                reformulated += f"Projet: {project_id}\n"
                reformulated += f"Observation: {note_text}\n\n"
                reformulated += f"Action requise: " + random.choice([
                    "Correction immédiate requise pour conformité",
                    "À compléter avant inspection",
                    "Suivi avec sous-traitant nécessaire",
                    "Documentation à mettre à jour"
                ])
                
                # Insérer dans la base
                self.cursor.execute('''
                    INSERT INTO notes 
                    (project_id, date, author, category, original_note, reformulated_note, 
                     confidence_score, metadata, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    project_id,
                    (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
                    random.choice(['Jean Tremblay', 'Marc Dubois', 'Pierre Lavoie']),
                    note_type['type'],
                    note_text,
                    reformulated,
                    round(random.uniform(0.85, 0.98), 2),
                    json.dumps({'auto_generated': True, 'template': template}),
                    datetime.now().isoformat()
                ))
                
                # Entrainement DeepSeek
                self.training_data.append({
                    "messages": [
                        {"role": "system", "content": "Tu es un assistant IA qui reformule les notes de terrain en français professionnel pour les rapports de construction électrique."},
                        {"role": "user", "content": f"Reformule cette note de terrain: {note_text}"},
                        {"role": "assistant", "content": reformulated}
                    ]
                })
                
        self.conn.commit()
        print("✅ 60 notes terrain générées")
        
    def save_training_data(self):
        """Sauvegarder les données d'entrainement pour DeepSeek"""
        print(f"\n💾 Sauvegarde des données d'entrainement...")
        
        with open(TRAINING_FILE, 'w', encoding='utf-8') as f:
            for item in self.training_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
                
        print(f"✅ {len(self.training_data)} exemples sauvegardés dans {TRAINING_FILE}")
        
        # Créer aussi un fichier de métadonnées
        metadata = {
            'created_at': datetime.now().isoformat(),
            'total_examples': len(self.training_data),
            'projects': ['C24-060 - Kahnawake', 'C24-048 - Alexis Nihon'],
            'categories': {
                'project_info': sum(1 for d in self.training_data if 'statut du projet' in str(d)),
                'document_analysis': sum(1 for d in self.training_data if 'document' in str(d)),
                'note_reformulation': sum(1 for d in self.training_data if 'Reformule' in str(d))
            }
        }
        
        with open(TRAINING_FILE.replace('.jsonl', '_metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
            
    def generate_summary(self):
        """Générer un résumé de l'import"""
        print("\n📊 RÉSUMÉ DE L'IMPORT")
        print("=" * 50)
        
        # Compter les enregistrements
        tables = ['projects', 'documents', 'notes']
        for table in tables:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cursor.fetchone()[0]
            print(f"{table.capitalize()}: {count}")
            
        # Statistiques par projet
        print("\nPar projet:")
        self.cursor.execute('''
            SELECT p.id, p.name, 
                   COUNT(DISTINCT d.id) as doc_count,
                   COUNT(DISTINCT n.id) as note_count
            FROM projects p
            LEFT JOIN documents d ON p.id = d.project_id
            LEFT JOIN notes n ON p.id = n.project_id
            GROUP BY p.id
        ''')
        
        for row in self.cursor.fetchall():
            print(f"  {row[0]} - {row[1]}: {row[2]} docs, {row[3]} notes")
            
    def run(self):
        """Exécuter l'import complet"""
        print("🚀 DÉMARRAGE IMPORT PGI-IA")
        print(f"Kahnawake: {KAHNAWAKE_PATH}")
        print(f"Alexis Nihon: {ALEXIS_PATH}")
        
        self.clear_existing_data()
        self.import_projects()
        self.import_sample_documents(limit_per_project=50)
        self.generate_sample_notes()
        self.save_training_data()
        self.generate_summary()
        
        self.conn.close()
        print("\n✅ IMPORT TERMINÉ!")
        print(f"🎓 Données d'entrainement DeepSeek: {TRAINING_FILE}")
        
if __name__ == "__main__":
    importer = DataImporter()
    importer.run()