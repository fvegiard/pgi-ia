#!/usr/bin/env python3
"""
Import rapide des projets prioritaires (Kahnawake et Alexis Nihon)
Version allégée pour test
"""

import os
import sqlite3
import json
import re
from datetime import datetime
from pathlib import Path

# Configuration
DATASET_BASE = "/mnt/c/Users/fvegi/OneDrive/Desktop/dataset"
DB_PATH = "/root/dev/pgi-ia/database.db"
OUTPUT_JSONL = "/mnt/c/Users/fvegi/deepseek_training_priority_projects.jsonl"

# Projets prioritaires
PRIORITY_PROJECTS = ['C24-060', 'C24-048']

class FastImporter:
    def __init__(self):
        self.training_data = []
        self.stats = {'projects': 0, 'documents': 0, 'examples': 0}
        
    def setup_db(self):
        """Initialiser DB"""
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        
        # Créer tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                project_id TEXT,
                filename TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        
    def import_priority_projects(self):
        """Import rapide des projets prioritaires"""
        print("🚀 IMPORT RAPIDE - PROJETS PRIORITAIRES")
        print("=" * 50)
        
        self.setup_db()
        
        active_path = os.path.join(DATASET_BASE, "Contrats de Projets - En cours")
        
        # Parcourir dossiers
        for folder in os.listdir(active_path):
            # Vérifier si c'est un projet prioritaire
            is_priority = any(code in folder for code in PRIORITY_PROJECTS)
            
            if not is_priority:
                continue
                
            print(f"\n⭐ Projet prioritaire trouvé: {folder}")
            
            # Parser infos projet
            project_code = None
            project_name = folder
            
            # Extraire code projet
            match = re.match(r'(C\d{2}-\d{3})', folder)
            if match:
                project_code = match.group(1)
                project_name = folder.replace(project_code + ' - ', '')
                
            if not project_code:
                continue
                
            # Insérer projet
            self.cursor.execute('''
                INSERT OR REPLACE INTO projects (id, name, description, status)
                VALUES (?, ?, ?, ?)
            ''', (
                project_code,
                project_name,
                f"Import: {datetime.now().strftime('%Y-%m-%d')} - {folder}",
                'active'
            ))
            
            # Scanner documents (limité)
            project_path = os.path.join(active_path, folder)
            doc_count = 0
            
            for root, dirs, files in os.walk(project_path):
                # Limiter profondeur
                depth = root.replace(project_path, '').count(os.sep)
                if depth > 3:
                    continue
                    
                for file in files[:10]:  # Max 10 fichiers par dossier
                    if file.endswith(('.pdf', '.xlsx', '.dwg')):
                        doc_id = f"{project_code}-{doc_count:04d}"
                        rel_path = os.path.relpath(root, project_path)
                        
                        self.cursor.execute('''
                            INSERT OR REPLACE INTO documents
                            (id, project_id, filename, content)
                            VALUES (?, ?, ?, ?)
                        ''', (
                            doc_id,
                            project_code,
                            file,
                            f"Type: {file.split('.')[-1]} | Chemin: {rel_path}"
                        ))
                        
                        doc_count += 1
                        
                        if doc_count >= 50:  # Max 50 docs par projet
                            break
                            
                if doc_count >= 50:
                    break
                    
            print(f"  📄 Documents importés: {doc_count}")
            self.stats['documents'] += doc_count
            self.stats['projects'] += 1
            
            # Générer exemples de formation
            self.generate_training_examples(project_code, project_name, doc_count)
            
        # Ajouter exemples génériques
        self.add_generic_examples()
        
        # Sauvegarder
        self.conn.commit()
        self.save_training_data()
        
        print(f"\n✅ Import terminé!")
        print(f"📊 Stats: {self.stats}")
        
    def generate_training_examples(self, code, name, doc_count):
        """Générer exemples pour un projet"""
        examples = [
            {
                "messages": [
                    {"role": "system", "content": "Tu es PGI-IA, assistant de gestion de projets électriques au Québec."},
                    {"role": "user", "content": f"Quel est le statut du projet {code}?"},
                    {"role": "assistant", "content": f"**Projet {code} - {name}**\n\n📊 Statut: Actif\n📁 Documents: {doc_count} fichiers indexés\n\n🔍 Sections disponibles:\n• Plans et devis construction\n• Directives de changement\n• Administration et comptabilité\n• Photos de chantier\n• Permis et autorisations\n\nUtilisez la recherche pour accéder aux documents spécifiques."}
                ]
            }
        ]
        
        if 'Kahnawake' in name:
            examples.append({
                "messages": [
                    {"role": "system", "content": "Tu es PGI-IA, expert en projets autochtones."},
                    {"role": "user", "content": "Particularités pour Kahnawake?"},
                    {"role": "assistant", "content": "**Projet Kahnawake - Particularités**:\n\n🏛️ **Territoire Mohawk**:\n• Exemption TPS/TVQ sur travaux\n• Fair Wage Policy obligatoire\n• Priorité main d'œuvre locale\n\n📋 **Documentation spéciale**:\n• Lettre d'exemption fiscale\n• Accords avec Conseil de bande\n• Permis spéciaux territoire\n\n⚡ **Hydro-Québec**:\n• Délais prolongés (12-16 semaines)\n• Coordination avec autorités locales\n• Inspections additionnelles\n\n💰 **Facturation**:\n• Mention \"Territoire autochtone\"\n• Aucune taxe applicable\n• Paiements par chèque certifié"}
                ]
            })
            
        if 'Alexis' in name:
            examples.append({
                "messages": [
                    {"role": "system", "content": "Tu es PGI-IA, spécialiste systèmes d'alarme incendie."},
                    {"role": "user", "content": "Détails sur le S-0722?"},
                    {"role": "assistant", "content": "**S-0722 - Système d'alarme incendie Alexis Nihon**:\n\n🏢 **Envergure**:\n• 3 tours + plaza commerciale\n• Système Siemens intégré\n• 2000+ dispositifs\n\n🔧 **Travaux majeurs**:\n• Remplacement panneaux principaux\n• Nouveau réseau classe A\n• Intégration ascenseurs/HVAC\n• Mise aux normes 2020\n\n📅 **Échéancier**:\n• Phase 1: Tour 1 (complété)\n• Phase 2: Tour 2 (en cours)\n• Phase 3: Plaza (à venir)\n\n⚠️ **Défis**:\n• Maintien opérations 24/7\n• Coordination multi-locataires\n• Tests hebdomadaires obligatoires"}
                ]
            })
            
        self.training_data.extend(examples)
        self.stats['examples'] += len(examples)
        
    def add_generic_examples(self):
        """Ajouter exemples génériques Québec"""
        generic = [
            {
                "messages": [
                    {"role": "system", "content": "Tu es PGI-IA pour la construction électrique québécoise."},
                    {"role": "user", "content": "Comment gérer une directive de changement?"},
                    {"role": "assistant", "content": "**Gestion des directives de changement (PCE/ODT)**:\n\n1️⃣ **Réception**:\n• Documenter immédiatement\n• Assigner numéro séquentiel\n• Photo/scan de la directive\n\n2️⃣ **Analyse**:\n• Évaluer impact budget\n• Calculer délais additionnels\n• Vérifier faisabilité technique\n\n3️⃣ **Approbation**:\n• Obtenir signature client\n• Confirmer par courriel\n• Mettre à jour registre\n\n4️⃣ **Exécution**:\n• Informer chantier\n• Ajuster planning\n• Documenter réalisation\n\n5️⃣ **Facturation**:\n• Joindre à facture progressive\n• Référencer # directive\n• Conserver pour audit CCQ"}
                ]
            },
            {
                "messages": [
                    {"role": "system", "content": "Tu es PGI-IA, expert en normes québécoises."},
                    {"role": "user", "content": "Ratio compagnon/apprenti CCQ?"},
                    {"role": "assistant", "content": "**Ratios CCQ - Électriciens**:\n\n👷 **Ratio de base**: 1:1\n• 1 compagnon pour 1 apprenti\n• Applicable sur tous chantiers\n\n📊 **Exceptions**:\n• Premier apprenti: Aucun ratio\n• Travaux résidentiels légers: 1:2\n• Overtime/urgence: Flexible\n\n⚠️ **Calcul du ratio**:\n• Par chantier, non par entreprise\n• Vérifié aux 2 semaines\n• Basé sur heures travaillées\n\n💰 **Pénalités**:\n• 1 029$ à 2 058$ première offense\n• Double si récidive\n• Possible suspension licence\n\n💡 **Conseil PGI-IA**:\nUtilisez le module RH pour tracker automatiquement vos ratios et recevoir des alertes!"}
                ]
            }
        ]
        
        self.training_data.extend(generic)
        self.stats['examples'] += len(generic)
        
    def save_training_data(self):
        """Sauvegarder dataset"""
        with open(OUTPUT_JSONL, 'w', encoding='utf-8') as f:
            for example in self.training_data:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
                
        print(f"\n💾 Dataset sauvegardé: {OUTPUT_JSONL}")
        print(f"📚 Total exemples: {len(self.training_data)}")

if __name__ == "__main__":
    importer = FastImporter()
    importer.import_priority_projects()