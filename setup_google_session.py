#!/usr/bin/env python3
"""
Script d'import des cookies Google depuis le navigateur
USAGE: python setup_google_session.py
"""

import json
import sqlite3
import os
from pathlib import Path
import shutil
from google_session_manager import GoogleSessionManager

def get_chrome_cookies():
    """Extrait les cookies Google depuis Chrome/Edge"""
    # Chemins possibles pour les cookies
    cookie_paths = [
        # Chrome
        Path("/mnt/c/Users/fvegi/AppData/Local/Google/Chrome/User Data/Default/Cookies"),
        # Edge
        Path("/mnt/c/Users/fvegi/AppData/Local/Microsoft/Edge/User Data/Default/Cookies"),
        # Brave
        Path("/mnt/c/Users/fvegi/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Cookies")
    ]
    
    for cookie_db in cookie_paths:
        if cookie_db.exists():
            print(f"✅ Base de cookies trouvée : {cookie_db}")
            
            # Copier la DB pour éviter les locks
            temp_db = "/tmp/cookies_temp.db"
            shutil.copy2(str(cookie_db), temp_db)
            
            try:
                conn = sqlite3.connect(temp_db)
                cursor = conn.cursor()
                
                # Récupérer les cookies Google
                cursor.execute("""
                    SELECT name, value FROM cookies 
                    WHERE host_key LIKE '%.google.com'
                    AND name IN ('__Secure-1PAPISID', '__Secure-3PAPISID', 
                                 'SAPISID', '__Secure-1PSID', '__Secure-3PSID',
                                 'SID', 'HSID', 'SSID', 'APISID', 'NID')
                """)
                
                cookies = {}
                for name, value in cursor.fetchall():
                    # Les cookies peuvent être chiffrés dans certains navigateurs
                    cookies[name] = value
                
                conn.close()
                os.remove(temp_db)
                
                if cookies:
                    return cookies
                    
            except Exception as e:
                print(f"❌ Erreur lecture cookies : {e}")
                if os.path.exists(temp_db):
                    os.remove(temp_db)
    
    return None

def setup_from_manual_input():
    """Configuration manuelle des cookies"""
    print("\n📋 CONFIGURATION MANUELLE DES COOKIES")
    print("Copie les valeurs depuis l'inspecteur Chrome (F12 > Application > Cookies)")
    print("=" * 60)
    
    cookies = {}
    
    # Cookies essentiels
    cookie_names = [
        '__Secure-1PAPISID',
        '__Secure-3PAPISID',
        'SAPISID',
        '__Secure-1PSID',
        'SID',
        'HSID',
        'NID'
    ]
    
    for name in cookie_names:
        value = input(f"\n{name}: ").strip()
        if value:
            cookies[name] = value
    
    return cookies

def main():
    print("🔐 Configuration Google Session pour PGI-IA")
    print("=" * 60)
    
    # Essayer d'abord l'extraction automatique
    print("\n🔍 Tentative d'extraction automatique des cookies...")
    cookies = get_chrome_cookies()
    
    if not cookies:
        print("\n⚠️ Extraction automatique échouée (cookies peut-être chiffrés)")
        print("Passage en mode manuel...")
        cookies = setup_from_manual_input()
    
    if cookies:
        print(f"\n✅ {len(cookies)} cookies récupérés")
        
        # Configurer le manager
        manager = GoogleSessionManager()
        manager.set_cookies(cookies)
        
        # Tester
        print("\n🧪 Test de l'authentification...")
        if manager.test_auth():
            print("\n✅ Configuration réussie ! Les cookies sont sauvegardés.")
            print("Tu peux maintenant utiliser google_session_manager.py")
        else:
            print("\n❌ L'authentification a échoué. Vérifie les cookies.")
    else:
        print("\n❌ Aucun cookie configuré")

if __name__ == "__main__":
    main()
