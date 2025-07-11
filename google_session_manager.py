#!/usr/bin/env python3
"""
Google Session Manager pour PGI-IA
Utilise les cookies de session pour les requêtes authentifiées
ATTENTION: Ne jamais commiter ce fichier ou partager les cookies!
"""

import requests
import json
from datetime import datetime
import os

class GoogleSessionManager:
    def __init__(self):
        self.session = requests.Session()
        self.cookies_file = os.path.join(os.path.dirname(__file__), '.google_session', 'cookies.json')
        self.load_cookies()
    
    def set_cookies(self, cookies_dict):
        """Configure les cookies de session Google"""
        # Cookies critiques pour l'authentification
        critical_cookies = [
            '__Secure-1PAPISID',
            '__Secure-3PAPISID', 
            'SAPISID',
            '__Secure-1PSID',
            '__Secure-3PSID',
            'SID',
            'HSID',
            'SSID',
            'APISID',
            'NID'
        ]
        
        # Ajouter les cookies à la session
        for name, value in cookies_dict.items():
            if name in critical_cookies:
                self.session.cookies.set(
                    name=name,
                    value=value,
                    domain='.google.com',
                    path='/'
                )
        
        # Sauvegarder de façon sécurisée
        self.save_cookies(cookies_dict)
        print("✅ Cookies de session configurés")
    
    def save_cookies(self, cookies_dict):
        """Sauvegarde sécurisée des cookies"""
        os.makedirs(os.path.dirname(self.cookies_file), exist_ok=True)
        
        # Ajouter métadonnées
        data = {
            'cookies': cookies_dict,
            'created_at': datetime.now().isoformat(),
            'warning': 'CONFIDENTIEL - Ne jamais partager ces données'
        }
        
        with open(self.cookies_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Permissions restrictives
        os.chmod(self.cookies_file, 0o600)
    
    def load_cookies(self):
        """Charge les cookies sauvegardés"""
        if os.path.exists(self.cookies_file):
            with open(self.cookies_file, 'r') as f:
                data = json.load(f)
                if 'cookies' in data:
                    self.set_cookies(data['cookies'])
                    print("✅ Cookies chargés depuis le cache")
    
    def test_auth(self):
        """Teste si l'authentification fonctionne"""
        try:
            # Test avec Google Drive API
            response = self.session.get(
                'https://www.googleapis.com/drive/v3/about?fields=user',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            if response.status_code == 200:
                user_info = response.json()
                print(f"✅ Authentifié comme : {user_info.get('user', {}).get('emailAddress', 'Unknown')}")
                return True
            else:
                print(f"❌ Erreur d'authentification : {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erreur : {e}")
            return False
    
    def get_drive_files(self):
        """Exemple : Liste les fichiers Google Drive"""
        try:
            response = self.session.get(
                'https://www.googleapis.com/drive/v3/files',
                params={'pageSize': 10},
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            if response.status_code == 200:
                files = response.json().get('files', [])
                print(f"\n📁 Fichiers Google Drive ({len(files)} trouvés):")
                for file in files:
                    print(f"  - {file.get('name')} ({file.get('mimeType')})")
                return files
            else:
                print(f"❌ Erreur : {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []


# Script d'exemple d'utilisation
if __name__ == "__main__":
    print("🔐 Google Session Manager pour PGI-IA")
    print("=" * 50)
    
    manager = GoogleSessionManager()
    
    # Pour configurer les cookies la première fois :
    # Remplace ces valeurs par tes vrais cookies
    example_cookies = {
        '__Secure-1PAPISID': 'VALEUR_DE_TON_COOKIE',
        '__Secure-3PAPISID': 'VALEUR_DE_TON_COOKIE',
        'SAPISID': 'VALEUR_DE_TON_COOKIE',
        # Ajoute les autres cookies nécessaires...
    }
    
    print("\n⚠️ INSTRUCTIONS:")
    print("1. Remplace les valeurs dans example_cookies par tes vrais cookies")
    print("2. Décommente la ligne manager.set_cookies(example_cookies)")
    print("3. Lance le script pour sauvegarder les cookies")
    print("4. Les cookies seront réutilisés automatiquement")
    
    # manager.set_cookies(example_cookies)  # Décommente cette ligne
    
    # Test de l'authentification
    if manager.test_auth():
        manager.get_drive_files()
