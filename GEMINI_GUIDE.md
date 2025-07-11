# 🤖 Guide Gemini pour PGI-IA

## 🚀 Installation Rapide

### 1. Obtenir une clé API GRATUITE
```bash
# Va sur : https://makersuite.google.com/app/apikey
# Connecte-toi avec ton compte Google
# Clique "Create API Key"
# Copie la clé (format : AIzaSy...)
```

### 2. Configuration automatique
```bash
cd /home/fvegi/dev/pgi-ia
./setup_gemini.sh
# Colle ta clé quand demandé
```

### 3. Test rapide
```bash
./gemini_integration_launcher.sh
# Choisis option 5 pour tester
```

## 📋 Fonctionnalités Disponibles

### 1. **Gemini Manager** (`gemini_manager.py`)
- Chat simple avec Gemini
- Analyse de contenu PDF
- Génération de code
- Analyse batch

### 2. **Intégration PGI-IA** (`gemini_pgi_integration.py`)
- Analyse spécialisée plans électriques
- Extraction composants et spécifications
- Génération d'estimations
- Chat contextuel avec Léa

### 3. **Gemini CLI** (optionnel)
- Terminal interactif
- Conversation continue
- Historique des chats

## 🎯 Cas d'Usage PGI-IA

### Analyser un plan PDF
```bash
python gemini_pgi_integration.py analyze plans_kahnawake/plan_001.pdf
```

### Analyser tous les PDFs d'un projet
```bash
python gemini_pgi_integration.py batch plans_kahnawake/
```

### Chat sur le projet
```bash
python gemini_pgi_integration.py chat "Quels sont les tableaux électriques du projet?"
```

## 🔧 Intégration avec le Backend Flask

```python
# Dans backend/main.py
from gemini_pgi_integration import GeminiPGIIntegration

gemini = GeminiPGIIntegration()

@app.route('/api/analyze-pdf', methods=['POST'])
def analyze_pdf():
    pdf_path = request.json['path']
    result = gemini.analyze_electrical_plan(pdf_path)
    return jsonify(result)
```

## 💰 Limites API Gratuite

- **Requêtes** : 60 par minute
- **Tokens** : 1 million par jour
- **Modèles** : gemini-1.5-flash (gratuit)
- **Taille** : 30k tokens par requête

## 🚀 Avantages vs Autres APIs

| Feature | Gemini | OpenAI | DeepSeek |
|---------|---------|---------|----------|
| **Prix** | GRATUIT* | Payant | Payant |
| **Limite** | 1M tokens/jour | Pay-per-use | Pay-per-use |
| **Vitesse** | Très rapide | Rapide | Moyen |
| **Qualité** | Excellent | Excellent | Bon |
| **PDF natif** | ✅ | ❌ | ❌ |

*Avec limites généreuses

## 🔄 Workflow Recommandé

1. **DeepSeek** : Orchestration principale (Léa)
2. **Gemini** : Analyse PDF et estimations
3. **Google Session** : Accès Drive/Gmail
4. **Multi-agents** : Validation croisée

## 🛠️ Dépannage

### "Gemini non configuré"
```bash
export GEMINI_API_KEY='AIzaSy...'
# Ou ajoute dans .env
```

### "Rate limit exceeded"
- Attendre 1 minute
- Utiliser gemini-1.5-flash (plus de quota)

### "Invalid API key"
- Vérifie le format (AIzaSy...)
- Réactive la clé sur Google AI Studio

## 📚 Ressources

- [Google AI Studio](https://makersuite.google.com/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
- [Prix et Limites](https://ai.google.dev/pricing)

---
*Gemini est GRATUIT pour PGI-IA avec des limites généreuses !*
