#!/usr/bin/env python3
"""
Démonstration automatique : Comment les workers Docker accélèrent le traitement
"""

import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import threading

# Simulation d'un PDF à traiter
class PDF:
    def __init__(self, nom, taille_mb):
        self.nom = nom
        self.taille_mb = taille_mb
        self.status = "⏳ En attente"
        self.worker = None
        self.temps_traitement = random.uniform(2, 5)  # 2-5 secondes
        
# Liste des 10 PDFs de Kahnawake
pdfs_kahnawake = [
    PDF("EC-M-RC01-TELECOM-CONDUITS.pdf", 15.2),
    PDF("EC-E-01-POWER-DISTRIBUTION.pdf", 8.7),
    PDF("EC-M-02-LIGHTING-PLAN.pdf", 12.4),
    PDF("EC-E-03-EMERGENCY-SYSTEMS.pdf", 9.1),
    PDF("EC-M-04-HVAC-CONTROLS.pdf", 11.8),
    PDF("EC-E-05-GROUNDING-PLAN.pdf", 7.3),
    PDF("EC-M-06-FIRE-ALARM.pdf", 13.6),
    PDF("EC-E-07-PANELS-SCHEDULE.pdf", 10.2),
    PDF("EC-M-08-SECURITY-SYSTEMS.pdf", 14.9),
    PDF("EC-E-09-GENERATOR-LAYOUT.pdf", 16.5)
]

print("🏗️ DÉMONSTRATION: Workers Docker pour PGI-IA")
print("="*60)
print(f"📄 {len(pdfs_kahnawake)} Plans PDF du Centre Culturel Kahnawake à traiter")
print("="*60)

def traiter_pdf_simple(pdf):
    """Traite un PDF (simulation du travail réel)"""
    pdf.status = f"🔄 Traitement par {pdf.worker}"
    time.sleep(pdf.temps_traitement)
    pdf.status = "✅ Complété"
    return pdf

def afficher_status():
    """Affiche le statut en temps réel"""
    print("\n📊 STATUT EN TEMPS RÉEL:")
    for pdf in pdfs_kahnawake:
        print(f"  {pdf.nom:<35} {pdf.status}")
    
    completes = sum(1 for p in pdfs_kahnawake if "✅" in p.status)
    print(f"\n  Progression: {completes}/{len(pdfs_kahnawake)} PDFs traités")

# SCENARIO 1: Sans workers (1 seul processus)
print("\n🐌 SCENARIO 1: SANS WORKERS DOCKER (1 seul processus)")
print("-"*60)

debut = time.time()
for i, pdf in enumerate(pdfs_kahnawake):
    pdf.worker = "Worker-Unique"
    pdf.status = "⏳ En attente"

print("Démarrage du traitement séquentiel...")
afficher_status()

for pdf in pdfs_kahnawake:
    traiter_pdf_simple(pdf)
    afficher_status()

temps_total_solo = time.time() - debut

print(f"\n⏱️  Temps total SANS workers: {temps_total_solo:.1f} secondes")
print(f"   Soit environ {temps_total_solo/60:.1f} minutes pour 10 PDFs")
print(f"   📈 Estimation pour 300 PDFs: {temps_total_solo*30/60:.0f} minutes! 😱")

# Reset pour scenario 2
for pdf in pdfs_kahnawake:
    pdf.status = "⏳ En attente"
    pdf.worker = None

print("\n" + "="*60)
print("🔄 Passage au scénario avec 3 workers Docker...")
print("="*60)

# SCENARIO 2: Avec 3 workers Docker
print("\n🚀 SCENARIO 2: AVEC 3 WORKERS DOCKER (traitement parallèle)")
print("-"*60)

def worker_docker(worker_id, pdfs_queue):
    """Simule un worker Docker qui traite des PDFs"""
    while pdfs_queue:
        try:
            pdf = pdfs_queue.pop(0)
            pdf.worker = f"Worker-{worker_id}"
            traiter_pdf_simple(pdf)
        except IndexError:
            break

debut = time.time()
pdfs_queue = pdfs_kahnawake.copy()

print("🐳 Démarrage de 3 workers Docker...")
print("   Worker-1: Container Docker (OCR + IA)")
print("   Worker-2: Container Docker (OCR + IA)")  
print("   Worker-3: Container Docker (OCR + IA)")

afficher_status()

# Lancer 3 workers en parallèle
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = []
    for i in range(1, 4):
        future = executor.submit(worker_docker, i, pdfs_queue)
        futures.append(future)
    
    # Afficher le status pendant le traitement
    while any(not future.done() for future in futures):
        time.sleep(1)
        afficher_status()

temps_total_workers = time.time() - debut

print(f"\n⏱️  Temps total AVEC 3 workers: {temps_total_workers:.1f} secondes")
print(f"   Soit environ {temps_total_workers/60:.1f} minutes pour 10 PDFs")
print(f"   📈 Estimation pour 300 PDFs: {temps_total_workers*30/60:.0f} minutes! 🚀")

print(f"\n💡 GAIN DE PERFORMANCE: {temps_total_solo/temps_total_workers:.1f}x plus rapide!")
print(f"   Temps économisé: {(temps_total_solo-temps_total_workers)/60:.1f} minutes")

# Visualisation Docker Compose
print("\n" + "="*60)
print("🐳 CONFIGURATION DOCKER-COMPOSE POUR AJOUTER DES WORKERS:")
print("="*60)

docker_compose_example = """
# docker-compose.yml
version: '3.8'

services:
  # Backend principal
  backend:
    image: pgi-ia-backend
    ports:
      - "5000:5000"
    environment:
      - REDIS_URL=redis://redis:6379
  
  # Service Redis pour la queue de travail
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
  
  # Workers OCR/IA (scalable)
  worker:
    image: pgi-ia-worker
    deploy:
      replicas: 3  # 👈 ICI: Changer pour 5, 10, 20 workers!
    environment:
      - REDIS_URL=redis://redis:6379
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    depends_on:
      - redis
    command: python worker.py
"""

print(docker_compose_example)

print("\n📈 COMMANDES DOCKER POUR SCALER:")
print("-"*40)
print("# Démarrer avec 3 workers:")
print("docker-compose up -d")
print("\n# Augmenter à 10 workers en temps réel:")
print("docker-compose up -d --scale worker=10")
print("\n# Voir les workers actifs:")
print("docker ps | grep worker")

print("\n💰 VALEUR POUR LES ACTIONNAIRES:")
print("-"*40)
print("✅ Traitement 3x plus rapide = Plus de projets")
print("✅ Scalable à la demande = Croissance facilitée")
print("✅ Pas de refonte système = Économies")
print("✅ Utilisation optimale GPU = ROI maximisé")

print("\n🎯 DÉMONSTRATION TERMINÉE!")
print("="*60)