#!/usr/bin/env python3
"""
PGI-IA Import Simple - Adapté aux schémas existants
"""

import os
import sqlite3
import json
import hashlib
import shutil
import uuid
from datetime import datetime, timedelta
import random
from pathlib import Path

# Paths
DATASET_BASE = "/mnt/c/Users/fvegi/OneDrive/Desktop/dataset/Contrats de Projets - En cours"
KAHNAWAKE_PATH = os.path.join(DATASET_BASE, "C24-060 - Centre Culturel Kahnawake - Les Entreprises QMD")
ALEXIS_PATH = os.path.join(DATASET_BASE, "C24-048 - Place Alexis-Nihon")
DB_PATH = "/root/dev/pgi-ia/pgi_ia.db"
UPLOAD_DIR = "/root/dev/pgi-ia/uploads"
TRAINING_FILE = "/mnt/c/Users/fvegi/deepseek_training_construction.jsonl"

class SimpleImporter:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.training_data = []
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
    def import_projects(self):
        """Importer les projets avec le schéma existant"""
        print("\n📁 Import des projets...")
        
        projects = [
            {
                'id': 'C24-060',
                'name': 'Centre Culturel Kahnawake',
                'description': 'Les Entreprises QMD - Budget: $1,250,000 - Construction électrique complète',
                'status': 'active'
            },
            {
                'id': 'C24-048', 
                'name': 'Place Alexis-Nihon Phase 3',
                'description': 'Cominar REIT - Budget: $850,000 - Rénovation système électrique',
                'status': 'active'
            }
        ]
        
        for project in projects:
            self.cursor.execute('''
                INSERT OR REPLACE INTO projects (id, name, description, status)
                VALUES (?, ?, ?, ?)
            ''', (project['id'], project['name'], project['description'], project['status']))
            
            print(f"✅ {project['id']}: {project['name']}")
            
            # Training data
            self.training_data.append({
                "messages": [
                    {"role": "system", "content": "Tu es un assistant spécialisé en gestion de projets de construction électrique au Québec."},
                    {"role": "user", "content": f"Parle-moi du projet {project['name']}"},
                    {"role": "assistant", "content": f"Le projet {project['name']} (code {project['id']}) est {project['description']}. C'est un projet majeur actuellement actif dans notre système de gestion."}
                ]
            })
            
        self.conn.commit()
        
    def import_documents(self, limit=30):
        """Importer des documents avec le schéma existant"""
        print(f"\n📄 Import de {limit} documents par projet...")
        
        for project_id, project_path, project_name in [
            ('C24-060', KAHNAWAKE_PATH, 'Kahnawake'),
            ('C24-048', ALEXIS_PATH, 'Alexis Nihon')
        ]:
            pdf_files = list(Path(project_path).rglob('*.pdf'))[:limit]
            
            for idx, pdf_path in enumerate(pdf_files):
                try:
                    # Générer ID unique
                    doc_id = str(uuid.uuid4())
                    
                    # Hash du fichier
                    with open(pdf_path, 'rb') as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                    
                    # Copier vers uploads
                    dest_name = f"{project_id}_{idx:03d}_{pdf_path.name}"
                    dest_path = os.path.join(UPLOAD_DIR, dest_name)
                    shutil.copy2(pdf_path, dest_path)
                    
                    # Insérer dans DB
                    self.cursor.execute('''
                        INSERT INTO documents 
                        (id, filename, project_id, upload_date, status, file_hash, file_size)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        doc_id,
                        dest_name,
                        project_id,
                        datetime.now().isoformat(),
                        'analyzed' if idx < 5 else 'pending',  # Simuler quelques analysés
                        file_hash,
                        os.path.getsize(pdf_path)
                    ))
                    
                    # Si analysé, ajouter un résultat
                    if idx < 5:
                        analysis = f"Document analysé: {pdf_path.name} contient des plans électriques pour le projet {project_name}."
                        self.cursor.execute(
                            "UPDATE documents SET analysis_result = ? WHERE id = ?",
                            (analysis, doc_id)
                        )
                        
                        # Training data pour analyse
                        self.training_data.append({
                            "messages": [
                                {"role": "system", "content": "Tu es un expert en analyse de documents techniques de construction électrique."},
                                {"role": "user", "content": f"Analyse ce document: {pdf_path.name}"},
                                {"role": "assistant", "content": analysis + " Les éléments clés incluent les spécifications de câblage, les panneaux de distribution et les normes CSA à respecter."}
                            ]
                        })
                    
                    if idx % 10 == 0:
                        print(f"  → {project_name}: {idx+1}/{limit} documents")
                        
                except Exception as e:
                    print(f"  ⚠️ Erreur: {str(e)[:50]}...")
                    
        self.conn.commit()
        print("✅ Documents importés")
        
    def generate_notes(self):
        """Générer des notes avec le schéma existant"""
        print("\n📝 Génération de notes terrain...")
        
        templates = [
            "Panneau {} non conforme - refaire identification",
            "Installation {} complétée selon plans",
            "Problème {} - intervention requise",
            "Test {} réussi - conforme CSA",
            "Directive: installer {} au local {}"
        ]
        
        elements = ['P1A', 'P2B', 'éclairage corridor', 'prises USB', 'disjoncteur 20A']
        locaux = ['101', '205', 'mécanique', 'électrique', 'entrepôt']
        
        for project_id in ['C24-060', 'C24-048']:
            for i in range(20):
                template = random.choice(templates)
                element = random.choice(elements)
                local = random.choice(locaux)
                
                # Compter les placeholders
                placeholder_count = template.count('{}')
                if placeholder_count == 2:
                    content = template.format(element, local)
                else:
                    content = template.format(element)
                
                # Version reformulée
                reformulated = f"**Note technique #{i+1}**\n\n"
                reformulated += f"Projet: {project_id}\n"
                reformulated += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n"
                reformulated += f"Observation: {content}\n\n"
                reformulated += "Action requise: " + random.choice([
                    "Correction immédiate pour conformité CSA",
                    "Documentation à mettre à jour",
                    "Aucune action - conforme"
                ])
                
                # Insérer
                self.cursor.execute('''
                    INSERT INTO notes (id, project_id, content, ai_reformulated, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    str(uuid.uuid4()),
                    project_id,
                    content,
                    reformulated,
                    'completed',
                    datetime.now().isoformat()
                ))
                
                # Training
                self.training_data.append({
                    "messages": [
                        {"role": "system", "content": "Tu es un assistant qui reformule les notes de terrain en documentation technique professionnelle pour la construction électrique au Québec."},
                        {"role": "user", "content": f"Reformule cette note: {content}"},
                        {"role": "assistant", "content": reformulated}
                    ]
                })
                
        self.conn.commit()
        print("✅ 40 notes générées")
        
    def save_training_data(self):
        """Sauvegarder le dataset d'entrainement"""
        print(f"\n💾 Sauvegarde dataset DeepSeek...")
        
        # Ajouter des exemples spécifiques construction électrique Québec
        self.training_data.extend([
            {
                "messages": [
                    {"role": "system", "content": "Tu es un expert en normes électriques du Québec."},
                    {"role": "user", "content": "Quelle est la hauteur standard pour les prises électriques?"},
                    {"role": "assistant", "content": "Selon le Code de construction du Québec, chapitre V - Électricité (basé sur CSA C22.1), les prises de courant standards doivent être installées à une hauteur de 300 mm (12 pouces) du plancher fini au centre de la boîte. Pour les comptoirs de cuisine, c'est 1060 mm (42 pouces), et pour l'accessibilité universelle, entre 400 mm et 1200 mm."}
                ]
            },
            {
                "messages": [
                    {"role": "system", "content": "Tu es un expert en estimation de projets électriques commerciaux."},
                    {"role": "user", "content": "Comment calculer le coût d'installation électrique par pied carré?"},
                    {"role": "assistant", "content": "Pour un bâtiment commercial au Québec, le coût moyen d'installation électrique varie entre 8$ et 15$ du pied carré, incluant: distribution (3-5$/pi²), éclairage (2-4$/pi²), prises et circuits (2-3$/pi²), et systèmes spéciaux (1-3$/pi²). Ces prix incluent matériaux et main-d'œuvre selon les taux CCQ 2024."}
                ]
            }
        ])
        
        with open(TRAINING_FILE, 'w', encoding='utf-8') as f:
            for item in self.training_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
                
        print(f"✅ {len(self.training_data)} exemples sauvegardés")
        print(f"📍 Fichier: {TRAINING_FILE}")
        
    def show_summary(self):
        """Afficher résumé"""
        print("\n📊 RÉSUMÉ IMPORT")
        print("=" * 40)
        
        for table in ['projects', 'documents', 'notes']:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cursor.fetchone()[0]
            print(f"{table}: {count}")
            
    def run(self):
        """Exécuter l'import"""
        print("🚀 DÉMARRAGE IMPORT SIMPLE PGI-IA")
        
        # Clear first
        for table in ['documents', 'notes']:
            self.cursor.execute(f"DELETE FROM {table}")
        self.conn.commit()
        
        self.import_projects()
        self.import_documents(30)
        self.generate_notes()
        self.save_training_data()
        self.show_summary()
        
        self.conn.close()
        print("\n✅ IMPORT TERMINÉ!")

if __name__ == "__main__":
    importer = SimpleImporter()
    importer.run()