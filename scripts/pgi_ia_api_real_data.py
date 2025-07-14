#!/usr/bin/env python3
"""
Test rapide API avec vraies données
"""

import requests
import json

# Test nouveaux endpoints
print("🔍 TEST API PGI-IA - DONNÉES RÉELLES")
print("=" * 50)

# 1. Projets de la DB
print("\n📊 PROJETS EN BASE:")
try:
    resp = requests.get('http://localhost:5000/api/db/projects')
    if resp.status_code == 200:
        projects = resp.json()
        for p in projects:
            print(f"  • {p['id']} - {p['name']} ({p['status']})")
    else:
        print(f"  ❌ Erreur: {resp.status_code}")
except Exception as e:
    print(f"  ❌ Exception: {e}")

# 2. Documents par projet
print("\n📄 DOCUMENTS PAR PROJET:")
for project_id in ['C24-048', 'C24-060']:
    try:
        resp = requests.get(f'http://localhost:5000/api/db/project/{project_id}/documents')
        if resp.status_code == 200:
            docs = resp.json()
            print(f"\n  {project_id}: {len(docs)} documents")
            if docs:
                for doc in docs[:3]:  # Premiers 3
                    print(f"    - {doc['filename']}")
        else:
            print(f"  ❌ {project_id}: Erreur {resp.status_code}")
    except Exception as e:
        print(f"  ❌ {project_id}: Exception {e}")

# 3. Recherche
print("\n🔍 TEST RECHERCHE:")
queries = ['directive', 'Kahnawake', 'Alexis', 'plan']
for query in queries:
    try:
        resp = requests.get(f'http://localhost:5000/api/db/search?q={query}')
        if resp.status_code == 200:
            results = resp.json()
            print(f"  '{query}': {len(results)} résultats")
    except:
        print(f"  '{query}': Erreur")

print("\n✅ Tests terminés!")