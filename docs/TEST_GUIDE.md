# 🧪 TEST RAPIDE DU SYSTÈME PGI-IA

## 1️⃣ DÉMARRER LE BACKEND (2 min)

```bash
cd ~/dev/pgi-ia/backend

# Créer et activer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer dépendances minimales pour test
pip install fastapi uvicorn python-multipart PyPDF2

# Démarrer le serveur
uvicorn main:app --reload
```

✅ Le backend est prêt quand vous voyez:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

## 2️⃣ TESTER L'API (1 min)

### Test 1: Vérifier que ça marche
```bash
curl http://localhost:8000/
```

Réponse attendue:
```json
{
  "message": "PGI-IA API est opérationnelle! 🚀",
  "version": "0.1.0",
  "timestamp": "2025-07-09T..."
}
```

### Test 2: Upload d'un fichier
```bash
# Avec un PDF de test
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/chemin/vers/directive.pdf"
```

## 3️⃣ UTILISER LES VRAIS FICHIERS (5 min)

### Fichiers fournis à tester:
1. **Directives Kahnawake** (dans les documents fournis)
   - CO-ME-039
   - CO-ME-028
   - etc.

2. **Directives Alexis Nihon** (dans les documents fournis)
   - PCE-12
   - PCE-21
   - etc.

### Exemple avec un vrai fichier:
```bash
# Créer un PDF de test depuis le HTML
# (ou utiliser un PDF existant)

curl -X POST http://localhost:8000/api/upload \
  -F "file=@CO-ME-039.pdf"
```

## 4️⃣ VÉRIFIER LES RÉSULTATS

### Logs du serveur
Vous devriez voir:
```
📁 Fichier reçu: CO-ME-039.pdf (12345 bytes)
🎯 Nouveau fichier reçu: CO-ME-039.pdf
📁 Type identifié: directive
🔍 Traitement de la directive: CO-ME-039.pdf
✅ Directive CO-ME-039 extraite avec succès
```

### Fichier de tracking
Vérifier le fichier JSON créé:
```bash
cat backend/data/tracking_*.json
```

## 5️⃣ INTERFACE WEB RAPIDE

Pour tester avec une interface:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Test PGI-IA Upload</title>
</head>
<body>
    <h1>Test Upload PGI-IA</h1>
    <form id="uploadForm">
        <input type="file" id="fileInput" accept=".pdf">
        <button type="submit">Upload</button>
    </form>
    <div id="result"></div>

    <script>
    document.getElementById('uploadForm').onsubmit = async (e) => {
        e.preventDefault();
        const file = document.getElementById('fileInput').files[0];
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('http://localhost:8000/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        document.getElementById('result').innerHTML = 
            '<pre>' + JSON.stringify(result, null, 2) + '</pre>';
    };
    </script>
</body>
</html>
```

Sauvegarder comme `test.html` et ouvrir dans le navigateur.

## 🎯 RÉSULTATS ATTENDUS

Si tout fonctionne:
1. ✅ Upload accepté
2. ✅ Type "directive" identifié
3. ✅ Extraction des infos (numéro, date, etc.)
4. ✅ Fichier JSON de tracking créé
5. ✅ Réponse avec timeline event

## 🐛 TROUBLESHOOTING

### Erreur: Module not found
```bash
pip install [module_manquant]
```

### Erreur: Port already in use
```bash
# Changer le port
uvicorn main:app --reload --port 8001
```

### Erreur: PDF extraction failed
- Vérifier que le PDF n'est pas protégé
- Essayer avec un PDF plus simple

## 🚀 PROCHAINE ÉTAPE

Une fois que l'upload fonctionne:
1. Créer le frontend React
2. Intégrer l'interface des tableaux HTML fournis
3. Ajouter WebSocket pour temps réel

---

**Temps total estimé: 10 minutes** ⏱️