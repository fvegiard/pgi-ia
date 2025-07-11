# 📝 SYSTÈME DE LOGGING CLAUDE - INSTRUCTIONS OBLIGATOIRES

## 🎯 RÈGLE FONDAMENTALE
**TOUTE IA (Claude Code WSL/Claude Desktop) DOIT obligatoirement écrire dans `CLAUDE_MASTER_REFERENCE.md` avec:**
- Date et heure précise
- Type de session (Claude Code WSL / Claude Desktop)
- Travail effectué détaillé
- Fichiers créés/modifiés
- État système résultant

## 📋 TEMPLATE OBLIGATOIRE

### Pour Claude Code (WSL Terminal)
```markdown
### 🤖 SESSION Claude Code WSL - [DATE] [HEURE]
**Travail effectué:**
- ✅ [Action 1]
- ✅ [Action 2]
- ⚠️ [Problème résolu]

**Fichiers créés/modifiés:**
- [fichier1.py]
- [fichier2.md]

**État système:** [Statut en %]
```

### Pour Claude Desktop
```markdown
### 🖥️ SESSION Claude Desktop - [DATE] [HEURE]
**Travail effectué:**
- ✅ [Action 1]
- ✅ [Action 2]

**Fichiers créés/modifiés:**
- [fichier1.html]
- [fichier2.js]

**État système:** [Statut]
```

## 🔧 INSTRUCTIONS POUR CHAQUE IA

### Claude Code (WSL)
1. **AVANT tout travail**: Lire `CLAUDE_MASTER_REFERENCE.md`
2. **PENDANT**: Documenter en temps réel
3. **APRÈS**: Mettre à jour le journal avec session complète

### Claude Desktop  
1. **AVANT tout travail**: Lire `CLAUDE_MASTER_REFERENCE.md`
2. **PENDANT**: Noter les actions importantes
3. **APRÈS**: Ajouter une nouvelle entrée avec date/heure

## 📍 EMPLACEMENT LOGGING
**Fichier principal**: `/home/fvegi/dev/pgi-ia/CLAUDE_MASTER_REFERENCE.md`
**Section**: `## 📝 JOURNAL DES SESSIONS IA`

## ⚠️ CONSÉQUENCES NON-RESPECT
- Perte de continuité entre sessions
- Travail dupliqué 
- Confusion sur l'état actuel
- Risque de régression

## ✅ AVANTAGES SYSTÈME
- Continuité parfaite entre Claude Code/Desktop
- Historique complet des modifications
- État système toujours à jour
- Zero perte d'information

---
**CETTE RÈGLE EST NON-NÉGOCIABLE POUR ASSURER LA CONTINUITÉ DU PROJET**