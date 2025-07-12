"""
Justina - Auditrice UX pour PGI-IA
Spécialisée dans la validation interface et expérience utilisateur
"""
import os
import re
from datetime import datetime
from typing import Dict, List, Any
import json

class JustinaUXAuditor:
    def __init__(self):
        self.audit_results = {
            "timestamp": datetime.now().isoformat(),
            "auditor": "Justina UX v1.0",
            "project": "PGI-IA v4.1",
            "interfaces": {},
            "global_score": 0,
            "recommendations": []
        }
        
        # Critères d'audit UX
        self.ux_criteria = {
            "accessibility": {
                "alt_texts": 0,
                "aria_labels": 0,
                "semantic_html": 0,
                "color_contrast": 0
            },
            "navigation": {
                "menu_clarity": 0,
                "breadcrumbs": 0,
                "links_working": 0,
                "mobile_responsive": 0
            },
            "interactivity": {
                "button_feedback": 0,
                "loading_states": 0,
                "error_handling": 0,
                "form_validation": 0
            },
            "performance": {
                "lazy_loading": 0,
                "optimized_assets": 0,
                "minimal_dependencies": 0,
                "fast_interactions": 0
            }
        }
    
    def audit_html_file(self, filepath: str) -> Dict[str, Any]:
        """Audite un fichier HTML spécifique"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            filename = os.path.basename(filepath)
            audit = {
                "file": filename,
                "size": len(content),
                "issues": [],
                "strengths": [],
                "elements": {
                    "buttons": self._count_elements(content, r'<button|<input[^>]*type=["\']button'),
                    "forms": self._count_elements(content, r'<form'),
                    "inputs": self._count_elements(content, r'<input'),
                    "links": self._count_elements(content, r'<a\s'),
                    "images": self._count_elements(content, r'<img'),
                    "scripts": self._count_elements(content, r'<script'),
                    "modals": self._count_elements(content, r'modal|dialog|popup'),
                }
            }
            
            # Vérifications d'accessibilité
            if audit["elements"]["images"] > 0:
                alt_count = len(re.findall(r'<img[^>]*alt=["\'][^"\']+["\']', content))
                if alt_count < audit["elements"]["images"]:
                    audit["issues"].append(f"❌ {audit['elements']['images'] - alt_count} images sans attribut alt")
                else:
                    audit["strengths"].append("✅ Toutes les images ont un attribut alt")
            
            # Vérifications des boutons
            button_matches = re.findall(r'<button[^>]*>(.*?)</button>', content, re.DOTALL)
            empty_buttons = sum(1 for btn in button_matches if not btn.strip())
            if empty_buttons > 0:
                audit["issues"].append(f"❌ {empty_buttons} boutons sans texte")
            
            # Vérifications aria-label
            aria_labels = len(re.findall(r'aria-label=["\'][^"\']+["\']', content))
            if aria_labels > 0:
                audit["strengths"].append(f"✅ {aria_labels} éléments avec aria-label")
            
            # Vérifications responsive
            if 'viewport' in content:
                audit["strengths"].append("✅ Meta viewport présent (mobile-friendly)")
            else:
                audit["issues"].append("❌ Meta viewport manquant")
            
            # Vérifications Tailwind CSS
            if 'tailwindcss' in content.lower():
                audit["strengths"].append("✅ Utilise Tailwind CSS (design moderne)")
                
                # Classes responsive
                responsive_classes = len(re.findall(r'(sm:|md:|lg:|xl:|2xl:)', content))
                if responsive_classes > 10:
                    audit["strengths"].append(f"✅ {responsive_classes} classes responsive détectées")
                else:
                    audit["issues"].append("⚠️ Peu de classes responsive Tailwind")
            
            # Vérifications JavaScript
            if 'addEventListener' in content:
                audit["strengths"].append("✅ Gestion d'événements JavaScript détectée")
            
            # Calcul du score
            audit["score"] = self._calculate_score(audit)
            
            return audit
            
        except Exception as e:
            return {"file": filepath, "error": str(e), "score": 0}
    
    def _count_elements(self, content: str, pattern: str) -> int:
        """Compte les occurrences d'un pattern"""
        return len(re.findall(pattern, content, re.IGNORECASE))
    
    def _calculate_score(self, audit: Dict) -> float:
        """Calcule un score UX de 0 à 100"""
        score = 100
        
        # Pénalités
        score -= len(audit["issues"]) * 5
        
        # Bonus
        score += len(audit["strengths"]) * 3
        
        # Ajustements basés sur les éléments
        if audit["elements"]["buttons"] == 0:
            score -= 10  # Pas d'interactivité
        if audit["elements"]["forms"] > 0 and audit["elements"]["inputs"] == 0:
            score -= 5  # Formulaire sans inputs
        
        return max(0, min(100, score))
    
    def audit_javascript(self, filepath: str) -> Dict[str, Any]:
        """Audite les fichiers JavaScript"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            audit = {
                "file": os.path.basename(filepath),
                "size": len(content),
                "features": [],
                "issues": []
            }
            
            # Détection de fonctionnalités
            if 'fetch(' in content or 'axios' in content:
                audit["features"].append("✅ Appels API détectés")
            
            if 'localStorage' in content or 'sessionStorage' in content:
                audit["features"].append("✅ Stockage local utilisé")
            
            if 'addEventListener' in content:
                audit["features"].append("✅ Gestion d'événements")
            
            if 'try' in content and 'catch' in content:
                audit["features"].append("✅ Gestion d'erreurs")
            else:
                audit["issues"].append("⚠️ Peu de gestion d'erreurs try/catch")
            
            if 'console.log' in content:
                audit["issues"].append("⚠️ console.log en production")
            
            return audit
            
        except Exception as e:
            return {"file": filepath, "error": str(e)}
    
    def generate_recommendations(self):
        """Génère des recommandations basées sur l'audit"""
        recommendations = []
        
        # Analyse globale des résultats
        total_issues = sum(len(iface.get("issues", [])) for iface in self.audit_results["interfaces"].values())
        
        if total_issues > 10:
            recommendations.append({
                "priority": "HIGH",
                "category": "Accessibilité",
                "action": "Corriger les problèmes d'accessibilité critiques (images sans alt, boutons vides)"
            })
        
        # Vérification mobile
        has_responsive = any("responsive" in str(iface.get("strengths", [])) 
                           for iface in self.audit_results["interfaces"].values())
        if not has_responsive:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Responsive",
                "action": "Améliorer l'adaptation mobile avec plus de classes responsive"
            })
        
        # Performance
        recommendations.append({
            "priority": "LOW",
            "category": "Performance",
            "action": "Considérer le lazy loading pour les images et composants lourds"
        })
        
        return recommendations
    
    def generate_report(self) -> str:
        """Génère un rapport complet"""
        report = []
        report.append("# 🎯 AUDIT UX COMPLET - PGI-IA v4.1")
        report.append(f"\n**Auditrice**: Justina UX v1.0")
        report.append(f"**Date**: {self.audit_results['timestamp']}")
        report.append(f"**Score Global**: {self.audit_results['global_score']:.1f}/100\n")
        
        report.append("## 📊 Résumé par Interface\n")
        for name, audit in self.audit_results["interfaces"].items():
            if "error" in audit:
                report.append(f"### ❌ {name}")
                report.append(f"Erreur: {audit['error']}\n")
                continue
                
            report.append(f"### {name} (Score: {audit.get('score', 0):.1f}/100)")
            if 'size' in audit:
                report.append(f"- **Taille**: {audit['size']:,} octets")
            if 'elements' in audit:
                report.append(f"- **Éléments**: {audit['elements']['buttons']} boutons, "
                             f"{audit['elements']['forms']} formulaires, "
                             f"{audit['elements']['links']} liens")
            
            if audit.get('strengths'):
                report.append("\n**Points forts**:")
                for strength in audit['strengths']:
                    report.append(f"  {strength}")
            
            if audit.get('issues'):
                report.append("\n**Problèmes détectés**:")
                for issue in audit['issues']:
                    report.append(f"  {issue}")
            
            report.append("")
        
        report.append("## 💡 Recommandations Prioritaires\n")
        for rec in self.audit_results["recommendations"]:
            emoji = "🔴" if rec["priority"] == "HIGH" else "🟡" if rec["priority"] == "MEDIUM" else "🟢"
            report.append(f"{emoji} **{rec['category']}** [{rec['priority']}]")
            report.append(f"   → {rec['action']}\n")
        
        return "\n".join(report)

# Exécution de l'audit
if __name__ == "__main__":
    auditor = JustinaUXAuditor()
    
    # Audit des interfaces HTML
    html_files = [
        "/mnt/c/Users/fvegi/dev/pgi-ia/frontend/index.html",
        "/mnt/c/Users/fvegi/dev/pgi-ia/frontend/dashboard.html",
        "/mnt/c/Users/fvegi/dev/pgi-ia/frontend/dashboard_v4.html"
    ]
    
    for html_file in html_files:
        if os.path.exists(html_file):
            result = auditor.audit_html_file(html_file)
            auditor.audit_results["interfaces"][os.path.basename(html_file)] = result
    
    # Audit des fichiers JavaScript
    js_files = [
        "/mnt/c/Users/fvegi/dev/pgi-ia/frontend/script.js",
        "/mnt/c/Users/fvegi/dev/pgi-ia/frontend/dashboard.js"
    ]
    
    for js_file in js_files:
        if os.path.exists(js_file):
            result = auditor.audit_javascript(js_file)
            auditor.audit_results["interfaces"][os.path.basename(js_file)] = result
    
    # Calcul du score global
    scores = [iface.get("score", 50) for iface in auditor.audit_results["interfaces"].values() 
              if "score" in iface]
    auditor.audit_results["global_score"] = sum(scores) / len(scores) if scores else 0
    
    # Génération des recommandations
    auditor.audit_results["recommendations"] = auditor.generate_recommendations()
    
    # Génération du rapport
    report = auditor.generate_report()
    
    # Sauvegarde
    with open("/mnt/c/Users/fvegi/dev/pgi-ia/AUDIT_JUSTINA_UX.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    with open("/mnt/c/Users/fvegi/dev/pgi-ia/audit_justina_results.json", "w", encoding="utf-8") as f:
        json.dump(auditor.audit_results, f, indent=2, ensure_ascii=False)
    
    print("✅ Audit Justina UX terminé!")
    print(f"📊 Score global: {auditor.audit_results['global_score']:.1f}/100")
