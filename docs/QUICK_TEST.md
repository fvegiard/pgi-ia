# 🧪 GUIDE DE TEST RAPIDE PGI-IA

## DÉMARRAGE RAPIDE (5 min)

### 1. Backend
```bash
cd ~/dev/pgi-ia/backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn python-multipart PyPDF2
uvicorn main:app --reload
```

### 2. Test API
```bash
# Vérifier que ça marche
curl http://localhost:8000/

# Upload test
curl -X POST http://localhost:8000/api/upload \
  -F "file=@test.pdf"
```

### 3. Interface test HTML
Créer `test.html`:
```html
<!DOCTYPE html>
<html>
<body>
    <h1>Test Upload</h1>
    <input type="file" id="file">
    <button onclick="upload()">Upload</button>
    <div id="result"></div>
    <script>
    async function upload() {
        const file = document.getElementById('file').files[0];
        const formData = new FormData();
        formData.append('file', file);
        const res = await fetch('http://localhost:8000/api/upload', {
            method: 'POST', body: formData
        });
        document.getElementById('result').innerText = 
            JSON.stringify(await res.json(), null, 2);
    }
    </script>
</body>
</html>
```

## RÉSULTATS ATTENDUS
✅ Upload → Type identifié → Extraction → JSON créé

## PROCHAINES ÉTAPES
1. Frontend React
2. Intégration tableaux
3. WebSocket temps réel