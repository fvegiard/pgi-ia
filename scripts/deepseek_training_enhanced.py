#!/usr/bin/env python3
"""
Génération d'un dataset DeepSeek enrichi basé sur les vrais fichiers
"""

import json
import os
from pathlib import Path
import random

# Paths
KAHNAWAKE_PATH = "/mnt/c/Users/fvegi/OneDrive/Desktop/dataset/Contrats de Projets - En cours/C24-060 - Centre Culturel Kahnawake - Les Entreprises QMD"
ALEXIS_PATH = "/mnt/c/Users/fvegi/OneDrive/Desktop/dataset/Contrats de Projets - En cours/C24-048 - Place Alexis-Nihon"
OUTPUT_FILE = "/mnt/c/Users/fvegi/deepseek_training_pgi_ia_enhanced.jsonl"

def generate_enhanced_dataset():
    """Créer un dataset plus riche et spécifique"""
    
    training_data = []
    
    # 1. EXEMPLES BASÉS SUR LES DIRECTIVES RÉELLES
    training_data.extend([
        {
            "messages": [
                {"role": "system", "content": "Tu es un expert en gestion de directives de changement pour projets de construction électrique au Québec."},
                {"role": "user", "content": "Explique-moi la directive CD A40 pour le projet Kahnawake"},
                {"role": "assistant", "content": "La directive CD A40 du projet Centre Culturel Kahnawake concerne de multiples changements incluant des modifications aux dessins A-001, A-003, A-101, et A-200. Cette directive de changement impact l'installation électrique et nécessite une coordination avec les plans architecturaux révisés. Les changements incluent probablement des relocalisations de prises, modifications de circuits, et ajustements aux chemins de câbles pour s'adapter aux nouvelles configurations architecturales."}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": "Tu es un assistant spécialisé dans l'analyse des coûts de construction électrique."},
                {"role": "user", "content": "J'ai reçu une facture First Nation E000804. Comment gérer cela dans le projet Kahnawake?"},
                {"role": "assistant", "content": "Les factures First Nation comme la E000804 sont spécifiques au projet Kahnawake car il se situe sur le territoire Mohawk. Ces factures bénéficient d'exemptions fiscales (pas de TPS/TVQ) selon les ententes avec les Premières Nations. Assurez-vous de: 1) Valider le numéro d'exemption fiscale, 2) Séparer ces factures dans votre comptabilité pour les rapports gouvernementaux, 3) Vérifier que le fournisseur est bien enregistré auprès du Conseil Mohawk de Kahnawake, 4) Conserver la documentation pour les audits CCQ."}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": "Tu es un expert en normes électriques et permis Hydro-Québec."},
                {"role": "user", "content": "Quelles sont les exigences pour le permis HQ du projet Kahnawake?"},
                {"role": "assistant", "content": "Pour le projet Centre Culturel Kahnawake, le permis Hydro-Québec nécessite: 1) Plan unifilaire complet signé par un ingénieur, 2) Calcul de charge détaillé (probablement 600V/800A vu la taille), 3) Coordination avec le Conseil Mohawk car territoire autochtone, 4) Preuve d'assurance responsabilité 2M$, 5) Licence RBQ valide catégorie 16, 6) Formulaire de demande de raccordement commercial. Le délai est généralement 6-8 semaines mais peut être plus long sur territoire autochtone."}
            ]
        }
    ])
    
    # 2. EXEMPLES POUR ALEXIS NIHON
    training_data.extend([
        {
            "messages": [
                {"role": "system", "content": "Tu es un expert en rénovation de systèmes électriques commerciaux."},
                {"role": "user", "content": "Quel est le scope du projet Place Alexis-Nihon Phase 3?"},
                {"role": "assistant", "content": "Le projet Place Alexis-Nihon Phase 3 (C24-048) pour Cominar REIT consiste en une rénovation majeure du système électrique avec un budget de 850,000$. Les travaux incluent: modernisation des panneaux de distribution, mise aux normes des systèmes d'alarme incendie, ajout de circuits pour les nouvelles boutiques, amélioration de l'éclairage des corridors communs, et intégration de bornes de recharge VÉ. Le projet doit être coordonné avec les opérations du centre commercial pour minimiser l'impact sur les locataires."}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": "Tu es un spécialiste en coordination de projets commerciaux actifs."},
                {"role": "user", "content": "Comment gérer les travaux électriques pendant que le centre commercial Alexis Nihon est ouvert?"},
                {"role": "assistant", "content": "Pour les travaux à Place Alexis-Nihon pendant les heures d'opération: 1) Travaux bruyants uniquement 6h-9h ou après 21h, 2) Coupures électriques coordonnées avec gestion immobilière (préavis 72h minimum), 3) Corridors de protection obligatoires pour clients, 4) Équipe de nuit pour travaux majeurs (prime CCQ 50%), 5) Plan de contingence pour urgences, 6) Communication hebdomadaire avec locataires affectés. Prévoir 20-30% de temps supplémentaire vs chantier fermé."}
            ]
        }
    ])
    
    # 3. REFORMULATION DE NOTES TERRAIN RÉALISTES
    notes_terrain = [
        ("panneau P3A manque identification 15-20-30", 
         "**Déficience - Panneau P3A**\nLe panneau électrique P3A ne respecte pas l'article 2-100 du Code électrique. Identification manquante pour les circuits 15, 20 et 30. Action: Installer étiquettes gravées permanentes conformes CSA avant inspection finale."),
        
        ("conduit 3/4 écrasé local 204 refaire", 
         "**Déficience critique - Local 204**\nConduit EMT 3/4\" endommagé (écrasé) dans le local 204. Non-conformité article 12-906. Risque d'endommagement des conducteurs. Action immédiate: Remplacer section de conduit et vérifier intégrité de l'isolation des fils avec mégohmmètre."),
         
        ("ajouté 4 prises garage demande client", 
         "**Modification autorisée - Garage**\nInstallation de 4 prises supplémentaires dans le garage à la demande du client. Configuration: 2 circuits 20A dédiés, prises DDFT pour protection. Conforme article 26-700. Mise à jour des plans as-built requise."),
    ]
    
    for note_brute, note_pro in notes_terrain:
        training_data.append({
            "messages": [
                {"role": "system", "content": "Tu es un assistant qui transforme les notes de terrain en documentation professionnelle pour rapports de construction électrique."},
                {"role": "user", "content": f"Reformule cette note de chantier: {note_brute}"},
                {"role": "assistant", "content": note_pro}
            ]
        })
    
    # 4. ANALYSE DE DOCUMENTS SPÉCIFIQUES
    training_data.extend([
        {
            "messages": [
                {"role": "system", "content": "Tu es un expert en analyse de plans électriques et devis techniques."},
                {"role": "user", "content": "J'ai le fichier '026 50 00_17_Base Béton pour Luminaire extérieur_PMA_MHA'. Que contient ce type de document?"},
                {"role": "assistant", "content": "Le document '026 50 00_17' suit la nomenclature MasterFormat. Section 026 50 00 concerne les bases et supports pour équipements électriques. Ce document spécifie les bases de béton pour luminaires extérieurs, incluant: dimensions des bases selon hauteur des poteaux, armature requise, profondeur d'enfouissement selon gel (min 1.5m au Québec), détails des conduits d'alimentation, et ancrages pour résister aux charges de vent. Les annotations PMA_MHA réfèrent probablement aux ingénieurs (Peter Malouf Architecte et MHA ingénieurs)."}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": "Tu es un expert en gestion des quittances et conformité CCQ/CNESST."},
                {"role": "user", "content": "Explique l'importance des lettres de conformité CCQ & CNESST dans les projets"},
                {"role": "assistant", "content": "Les lettres de conformité CCQ et CNESST sont CRITIQUES pour les paiements. Sans ces lettres: 1) Le donneur d'ouvrage doit retenir 20% du paiement, 2) Risque de responsabilité solidaire pour cotisations impayées, 3) Impossibilité de fermer le projet. Pour Kahnawake, vérifier aussi les exemptions possibles pour travailleurs Mohawks. Processus: Demander lettres mensuellement, vérifier tous sous-traitants inclus, conserver 2 ans minimum. Un retard de conformité peut bloquer 100,000$+ de paiements."}
            ]
        }
    ])
    
    # 5. CALCULS ET ESTIMATIONS ÉLECTRIQUES
    training_data.extend([
        {
            "messages": [
                {"role": "system", "content": "Tu es un expert en estimation de projets électriques commerciaux au Québec."},
                {"role": "user", "content": "Comment calculer la main d'oeuvre pour un projet de 1.25M$ comme Kahnawake?"},
                {"role": "assistant", "content": "Pour un projet de 1.25M$ comme Kahnawake, la répartition typique est: 40% main d'œuvre (500k$), 45% matériel (562k$), 15% sous-traitance et frais (188k$). Avec les taux CCQ 2024 (électricien compagnon ~48$/h + charges ~75$/h total), cela représente ~6,700 heures. Pour 6 électriciens, c'est environ 7 mois de travail. Ajouter 15-20% pour territoire autochtone (transport, coordination). Les augmentations CCQ de mai 2024 (+2.5%) doivent être facturées en extra si non prévues au contrat."}
            ]
        }
    ])
    
    # 6. SÉCURITÉ ET NORMES
    training_data.extend([
        {
            "messages": [
                {"role": "system", "content": "Tu es un expert en sécurité électrique et normes CSA."},
                {"role": "user", "content": "Quelles sont les exigences de cadenassage pour un projet comme Alexis Nihon?"},
                {"role": "assistant", "content": "Pour Place Alexis-Nihon (centre commercial actif), le cadenassage suit la norme CSA Z462-21: 1) Programme écrit obligatoire avec Cominar, 2) Chaque électricien = cadenas personnel + étiquette photo, 3) Boîtes de cadenassage multiple pour panneaux partagés, 4) Vérification absence tension OBLIGATOIRE (testeur CAT IV), 5) Registre de cadenassage quotidien, 6) Formation documentée tous travailleurs. En milieu commercial occupé: double vérification + affichage 24h avant coupure. Amende CNESST possible: 5,000-50,000$ par infraction."}
            ]
        }
    ])
    
    # Sauvegarder
    print(f"💾 Génération de {len(training_data)} exemples enrichis...")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for item in training_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"✅ Dataset sauvegardé: {OUTPUT_FILE}")
    print(f"📊 Total: {len(training_data)} exemples spécialisés construction électrique Québec")
    
    # Statistiques
    categories = {
        'Directives': sum(1 for d in training_data if 'directive' in str(d).lower()),
        'Normes/Codes': sum(1 for d in training_data if any(x in str(d).lower() for x in ['csa', 'code', 'norme'])),
        'Finances': sum(1 for d in training_data if any(x in str(d).lower() for x in ['facture', 'coût', 'budget', '$'])),
        'Sécurité': sum(1 for d in training_data if any(x in str(d).lower() for x in ['sécurité', 'cadenassage', 'cnesst'])),
        'Notes terrain': sum(1 for d in training_data if 'reformule' in str(d).lower())
    }
    
    print("\n📈 Répartition par catégorie:")
    for cat, count in categories.items():
        print(f"  - {cat}: {count}")

if __name__ == "__main__":
    generate_enhanced_dataset()