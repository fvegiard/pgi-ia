# 📋 Workflow Claude pour PGI-IA

## ⚡ Règles de sauvegarde OBLIGATOIRES

### 1. **Sauvegarde immédiate**
Après CHAQUE modification importante :
```bash
git add .
git commit -m "feat: [description]"
git push origin main
```

### 2. **Vérification avant fin de session**
TOUJOURS exécuter avant de terminer :
```bash
git status
git diff
```

### 3. **Structure des commits**
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `style:` Changements UI/CSS
- `docs:` Documentation

### 4. **Fichiers critiques à surveiller**
- `/frontend/*.html` - Interfaces
- `/frontend/*.js` - Logique
- `/backend/*.py` - API
- `*.md` - Documentation

## 🚨 Checklist fin de session

- [ ] Tous les fichiers créés sont dans Git ?
- [ ] Les modifications sont commitées ?
- [ ] Push effectué vers GitHub ?
- [ ] Documentation mise à jour ?

## 💡 Scripts helper

```bash
# Créer un alias pour sauvegarder rapidement
echo "alias pgi-save='cd ~/dev/pgi-ia && git add . && git commit -m \"wip: sauvegarde session Claude\" && git push'" >> ~/.bashrc
```

---
*Ce fichier DOIT être lu au début de chaque session Claude*
