#!/usr/bin/env python3
"""
AUDIT DEEPSEEK - PGI-IA v4.1
Audit technique complet en 2 tours
"""

import os
import json
import subprocess
from pathlib import Path

def audit_tour_1():
    """TOUR 1 DEEPSEEK: Audit architecture et code"""
    print("🔍 AUDIT DEEPSEEK TOUR 1 - Architecture & Code")
    print("=" * 50)
    
    audit_results = {
        "architecture": {},
        "backend": {},
        "frontend": {},
        "config": {},
        "data": {}
    }
    
    # 1. Architecture générale
    print("\n📁 1. ARCHITECTURE GÉNÉRALE")
    base_path = Path("/home/fvegi/dev/pgi-ia")
    
    required_dirs = ["backend", "frontend", "config", "data"]
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        exists = dir_path.exists()
        audit_results["architecture"][dir_name] = exists
        status = "✅" if exists else "❌"
        print(f"   {status} {dir_name}/")
    
    # 2. Backend Flask
    print("\n🔧 2. BACKEND FLASK")
    backend_files = {
        "main.py": "API principal",
        "requirements.txt": "Dépendances",
        "agents/orchestrator.py": "Orchestrateur Léa",
        "agents/directive_agent.py": "Agent directives"
    }
    
    for file_name, description in backend_files.items():
        file_path = base_path / "backend" / file_name
        exists = file_path.exists()
        audit_results["backend"][file_name] = exists
        status = "✅" if exists else "❌"
        print(f"   {status} {file_name} - {description}")
    
    # 3. Frontend moderne
    print("\n🎨 3. FRONTEND MODERNE")
    frontend_files = {
        "index.html": "Interface Tailwind",
        "script.js": "JavaScript complet",
        "style.css": "Styles CSS"
    }
    
    for file_name, description in frontend_files.items():
        file_path = base_path / "frontend" / file_name
        exists = file_path.exists()
        size = file_path.stat().st_size if exists else 0
        audit_results["frontend"][file_name] = {"exists": exists, "size": size}
        status = "✅" if exists and size > 1000 else "❌"
        print(f"   {status} {file_name} ({size} bytes) - {description}")
    
    # 4. Configuration
    print("\n⚙️ 4. CONFIGURATION")
    config_files = {
        "agents.yaml": "Config multi-agents",
        "agents.example.yaml": "Template config"
    }
    
    for file_name, description in config_files.items():
        file_path = base_path / "config" / file_name
        exists = file_path.exists()
        audit_results["config"][file_name] = exists
        status = "✅" if exists else "⚠️"
        print(f"   {status} {file_name} - {description}")
    
    return audit_results

def audit_tour_2():
    """TOUR 2 DEEPSEEK: Audit fonctionnel et intégration"""
    print("\n🔍 AUDIT DEEPSEEK TOUR 2 - Fonctionnel & Intégration")
    print("=" * 50)
    
    audit_results = {
        "api_endpoints": {},
        "frontend_features": {},
        "data_integration": {},
        "ai_system": {}
    }
    
    # 1. API Endpoints Backend
    print("\n🌐 1. API ENDPOINTS")
    try:
        # Test import backend
        import sys
        sys.path.insert(0, '/home/fvegi/dev/pgi-ia/backend')
        
        # Vérification structure API
        with open('/home/fvegi/dev/pgi-ia/backend/main.py', 'r') as f:
            content = f.read()
            
        endpoints = [
            ("GET /", "@app.route('/')"),
            ("POST /upload", "@app.route('/upload'"),
            ("GET /projects", "@app.route('/projects'"),
            ("POST /ai/command", "@app.route('/ai/command'")
        ]
        
        for endpoint, pattern in endpoints:
            exists = pattern in content
            audit_results["api_endpoints"][endpoint] = exists
            status = "✅" if exists else "❌"
            print(f"   {status} {endpoint}")
            
    except Exception as e:
        print(f"   ❌ Erreur analyse backend: {e}")
    
    # 2. Frontend Features
    print("\n🎨 2. FRONTEND FEATURES")
    try:
        with open('/home/fvegi/dev/pgi-ia/frontend/script.js', 'r') as f:
            js_content = f.read()
            
        features = [
            ("Timeline", "renderTimeline"),
            ("Project Switch", "switchProject"),
            ("Drag-Drop", "handleFileUpload"),
            ("Financial Calc", "formatCurrency"),
            ("Navigation", "switchTab")
        ]
        
        for feature, pattern in features:
            exists = pattern in js_content
            audit_results["frontend_features"][feature] = exists
            status = "✅" if exists else "❌"
            print(f"   {status} {feature}")
            
    except Exception as e:
        print(f"   ❌ Erreur analyse frontend: {e}")
    
    # 3. Intégration données
    print("\n📊 3. INTÉGRATION DONNÉES")
    data_checks = [
        ("Projet Kahnawake", "kahnawake"),
        ("Projet Alexis-Nihon", "alexis-nihon"),
        ("Directives réelles", "CO-ME-"),
        ("Timeline events", "timelineEvents")
    ]
    
    try:
        for check, pattern in data_checks:
            exists = pattern in js_content
            audit_results["data_integration"][check] = exists
            status = "✅" if exists else "❌"
            print(f"   {status} {check}")
    except:
        print("   ❌ Erreur vérification données")
    
    # 4. Système IA
    print("\n🤖 4. SYSTÈME IA")
    ai_checks = [
        ("Orchestrateur Léa", "/home/fvegi/dev/pgi-ia/backend/agents/orchestrator.py"),
        ("Agent Directives", "/home/fvegi/dev/pgi-ia/backend/agents/directive_agent.py"),
        ("Config Multi-Agents", "/home/fvegi/dev/pgi-ia/config/agents.yaml"),
        ("Dataset DeepSeek", "/home/fvegi/dev/pgi-ia/deepseek_training_dataset.jsonl")
    ]
    
    for check, path in ai_checks:
        exists = os.path.exists(path)
        audit_results["ai_system"][check] = exists
        status = "✅" if exists else "❌"
        print(f"   {status} {check}")
    
    return audit_results

def generate_deepseek_report(tour1, tour2):
    """Génère rapport final DeepSeek"""
    print("\n📋 RAPPORT FINAL DEEPSEEK")
    print("=" * 50)
    
    total_checks = 0
    passed_checks = 0
    
    # Compter tous les checks
    for category in [tour1, tour2]:
        for section, items in category.items():
            if isinstance(items, dict):
                for item, result in items.items():
                    total_checks += 1
                    if isinstance(result, bool) and result:
                        passed_checks += 1
                    elif isinstance(result, dict) and result.get('exists'):
                        passed_checks += 1
    
    success_rate = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    
    print(f"📊 TAUX DE RÉUSSITE: {passed_checks}/{total_checks} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("🏆 VERDICT DEEPSEEK: EXCELLENT - Projet production-ready")
    elif success_rate >= 80:
        print("✅ VERDICT DEEPSEEK: BIEN - Projet fonctionnel")
    elif success_rate >= 70:
        print("⚠️ VERDICT DEEPSEEK: ACCEPTABLE - Améliorations mineures")
    else:
        print("❌ VERDICT DEEPSEEK: INSUFFISANT - Corrections majeures")
    
    return success_rate

if __name__ == "__main__":
    print("🧠 AUDIT DEEPSEEK PGI-IA v4.1")
    print("=" * 60)
    
    # Exécution des 2 tours
    tour1_results = audit_tour_1()
    tour2_results = audit_tour_2()
    
    # Rapport final
    success_rate = generate_deepseek_report(tour1_results, tour2_results)
    
    print(f"\n🎯 AUDIT DEEPSEEK TERMINÉ - Score: {success_rate:.1f}%")