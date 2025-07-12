#!/usr/bin/env python3
"""
Update Dashboard Plan Integration Script
Adds zoom/pan functionality to the existing dashboard
"""

import re
from pathlib import Path

def update_dashboard_with_plan_viewer():
    """Add plan viewer functionality to dashboard.html"""
    
    dashboard_path = Path("/home/fvegi/dev/pgi-ia/frontend/dashboard.html")
    
    if not dashboard_path.exists():
        print("❌ Dashboard.html not found!")
        return False
    
    # Read current dashboard
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if plan viewer script is already included
    if 'plan-viewer.js' in content:
        print("✅ Plan viewer already integrated!")
        return True
    
    # Add plan viewer script before closing body tag
    script_tag = '''
    <!-- Plan Viewer Integration -->
    <script src="assets/js/plan-viewer.js"></script>
    <script>
        // Initialize plan viewer when DOM is ready
        document.addEventListener('DOMContentLoaded', function() {
            // Find the plan container
            const planContainer = document.querySelector('#plan .relative.bg-gray-900');
            if (planContainer && planContainer.id !== 'planViewerContainer') {
                planContainer.id = 'planViewerContainer';
                
                // Initialize the plan viewer
                const viewer = new PlanViewer('planViewerContainer');
                
                // Handle zoom buttons
                const zoomInBtn = document.querySelector('[data-lucide="zoom-in"]')?.closest('button');
                const zoomOutBtn = document.querySelector('[data-lucide="layers"]')?.closest('button');
                
                if (zoomInBtn) {
                    zoomInBtn.addEventListener('click', () => viewer.zoomIn());
                }
                
                if (zoomOutBtn) {
                    // Repurpose layers button as zoom out
                    zoomOutBtn.innerHTML = '<i data-lucide="zoom-out" class="w-4 h-4 inline mr-1"></i>Zoom -';
                    zoomOutBtn.addEventListener('click', () => viewer.zoomOut());
                }
                
                // Update zoom level display
                viewer.container.addEventListener('zoomchange', (e) => {
                    const zoomText = zoomInBtn?.parentElement?.querySelector('.text-sm');
                    if (zoomText) {
                        zoomText.textContent = `Zoom: ${e.detail.percentage}%`;
                    }
                });
                
                // Add reset view functionality
                document.addEventListener('keydown', (e) => {
                    if (e.key === 'r' && e.ctrlKey) {
                        e.preventDefault();
                        viewer.resetView();
                    }
                });
                
                console.log('✅ Plan viewer initialized successfully');
            }
        });
    </script>
'''
    
    # Insert before closing body tag
    updated_content = content.replace('</body>', script_tag + '\n</body>')
    
    # Write updated content
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ Dashboard updated with plan viewer functionality!")
    print("📝 Features added:")
    print("   - Mouse drag to pan")
    print("   - Mouse wheel to zoom")
    print("   - Touch support for mobile devices")
    print("   - Zoom buttons integration")
    print("   - Ctrl+R to reset view")
    
    return True


def create_plan_info_json():
    """Create a JSON file with plan information"""
    import json
    
    plan_info = {
        "current_plan": {
            "file": "EC-M-RC01-TELECOM-CONDUITS-PATH---GROUND-LEVEL-Rev.1",
            "title": "PLAN EC-M-RC01",
            "description": "Centre Culturel Kahnawake - Conduits Télécom/Chemin de câbles - Rez-de-chaussée Rev.1",
            "project": "C24-060",
            "client": "Centre Culturel Kahnawake",
            "contractor": "Les Entreprises QMD",
            "date": "16 Juin 2025",
            "discipline": "Electrical",
            "extracted": {
                "png": "assets/plans/EC-M-RC01-TELECOM-CONDUITS-PATH---GROUND-LEVEL-Rev.1_page_1.png",
                "web_jpg": "assets/plans/EC-M-RC01-TELECOM-CONDUITS-PATH---GROUND-LEVEL-Rev.1_page_1_web.jpg",
                "dimensions": {
                    "original": {"width": 9362, "height": 6623},
                    "web": {"width": 2000, "height": 1414}
                }
            }
        },
        "markers": [
            {
                "id": 1,
                "type": "electrical",
                "x_percent": 25,
                "y_percent": 30,
                "title": "Panneaux électriques",
                "description": "Installation panneaux électriques - Salle mécanique",
                "status": "active",
                "color": "blue"
            },
            {
                "id": 2,
                "type": "photo",
                "x_percent": 60,
                "y_percent": 45,
                "title": "Photo géolocalisée",
                "description": "Photo: Conduits principaux - 10/07/2025 14:23",
                "photo_id": "IMG_2025_07_10_142300",
                "color": "green"
            },
            {
                "id": 3,
                "type": "issue",
                "x_percent": 40,
                "y_percent": 65,
                "title": "Zone problème",
                "description": "Conflit: Conduits vs structure acier - 2e étage",
                "severity": "high",
                "color": "orange"
            },
            {
                "id": 4,
                "type": "qrt",
                "x_percent": 75,
                "y_percent": 20,
                "title": "QRT Active",
                "description": "QRT #361: Luminaire L3 et K - En attente",
                "qrt_number": "361",
                "status": "pending",
                "color": "red"
            }
        ]
    }
    
    json_path = Path("/home/fvegi/dev/pgi-ia/frontend/assets/plans/current_plan_info.json")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(plan_info, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Plan info JSON created: {json_path}")
    return json_path


if __name__ == "__main__":
    print("🚀 Mise à jour du dashboard avec le visualiseur de plan")
    print("=" * 60)
    
    # Update dashboard
    if update_dashboard_with_plan_viewer():
        # Create plan info JSON
        create_plan_info_json()
        
        print("\n✅ Intégration complète!")
        print("\n📌 Pour tester:")
        print("1. Ouvrir le dashboard dans un navigateur")
        print("2. Aller à l'onglet 'Plan Principal'")
        print("3. Utiliser la souris pour naviguer dans le plan")
        print("4. Utiliser la molette pour zoomer/dézoomer")