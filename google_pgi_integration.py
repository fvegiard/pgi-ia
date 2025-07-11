#!/usr/bin/env python3
"""
Intégration Google Session avec PGI-IA
Permet d'utiliser l'API Google avec authentification par cookies
"""

from google_session_manager import GoogleSessionManager
import json

class GooglePGIIntegration:
    def __init__(self):
        self.session = GoogleSessionManager()
        
    def search_drive_for_pdfs(self, query=""):
        """Recherche des PDFs dans Google Drive"""
        try:
            params = {
                'q': f"mimeType='application/pdf' and name contains '{query}'",
                'pageSize': 100,
                'fields': 'files(id,name,mimeType,size,modifiedTime)'
            }
            
            response = self.session.session.get(
                'https://www.googleapis.com/drive/v3/files',
                params=params,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            if response.status_code == 200:
                files = response.json().get('files', [])
                print(f"\n📄 PDFs trouvés ({len(files)}):")
                for file in files:
                    size_mb = int(file.get('size', 0)) / 1024 / 1024
                    print(f"  - {file['name']} ({size_mb:.2f} MB)")
                return files
            else:
                print(f"❌ Erreur : {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
    
    def download_file(self, file_id, file_name):
        """Télécharge un fichier depuis Google Drive"""
        try:
            response = self.session.session.get(
                f'https://www.googleapis.com/drive/v3/files/{file_id}',
                params={'alt': 'media'},
                headers={'User-Agent': 'Mozilla/5.0'},
                stream=True
            )
            
            if response.status_code == 200:
                output_path = f"/home/fvegi/dev/pgi-ia/downloads/{file_name}"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
                
                print(f"✅ Téléchargé : {output_path}")
                return output_path
            else:
                print(f"❌ Erreur téléchargement : {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Erreur : {e}")
            return None
    
    def search_gmail(self, query):
        """Recherche dans Gmail"""
        try:
            # Utilise l'API Gmail via session
            response = self.session.session.get(
                'https://www.googleapis.com/gmail/v1/users/me/messages',
                params={'q': query, 'maxResults': 10},
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            if response.status_code == 200:
                messages = response.json().get('messages', [])
                print(f"\n📧 Emails trouvés ({len(messages)})")
                return messages
            else:
                print(f"❌ Erreur Gmail : {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []


# Exemple d'utilisation
if __name__ == "__main__":
    print("🔗 Intégration Google pour PGI-IA")
    print("=" * 50)
    
    google = GooglePGIIntegration()
    
    # Test authentification
    if google.session.test_auth():
        print("\n✅ Session Google active")
        
        # Rechercher des PDFs
        print("\n🔍 Recherche de plans PDF...")
        pdfs = google.search_drive_for_pdfs("plan")
        
        # Tu peux ajouter d'autres fonctionnalités ici
    else:
        print("\n❌ Session non configurée. Lance d'abord setup_google_session.py")
