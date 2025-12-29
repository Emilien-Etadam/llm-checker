# LLM Checker GUI - Build Instructions

Ce guide vous explique comment créer un fichier .exe Windows standalone à partir du code Python.

## 📋 Prérequis

### Sur Windows (Recommandé pour créer le .exe)

1. **Python 3.8 ou supérieur**
   - Télécharger depuis: https://www.python.org/downloads/
   - ✅ Cocher "Add Python to PATH" lors de l'installation

2. **Vérifier l'installation Python**
   ```cmd
   python --version
   pip --version
   ```

## 🔧 Installation des Dépendances

1. **Ouvrir un Terminal/Command Prompt**
   - Appuyez sur `Win + R`, tapez `cmd`, puis Entrée

2. **Naviguer vers le dossier python_gui**
   ```cmd
   cd chemin\vers\llm-checker\python_gui
   ```

3. **Installer les dépendances**
   ```cmd
   pip install -r requirements.txt
   ```

   Cela installera:
   - `psutil` - Pour la détection hardware
   - `pyinstaller` - Pour créer le .exe

## 🚀 Test de l'Application (Avant Build)

Avant de créer le .exe, testez que l'application fonctionne:

```cmd
python llm_checker_gui.py
```

L'application devrait se lancer et détecter automatiquement votre hardware.

## 📦 Création du Fichier .exe

### Méthode 1: Utiliser le fichier .spec (Recommandé)

```cmd
pyinstaller llm_checker.spec
```

### Méthode 2: Ligne de commande complète

```cmd
pyinstaller --onefile --windowed --name "LLM_Checker" ^
  --exclude-module matplotlib ^
  --exclude-module numpy ^
  --exclude-module pandas ^
  --upx-dir="C:\upx" ^
  llm_checker_gui.py
```

**Options expliquées:**
- `--onefile` : Crée un seul fichier .exe
- `--windowed` : Pas de console (GUI uniquement)
- `--name` : Nom de l'exécutable
- `--exclude-module` : Exclut des modules inutiles pour réduire la taille
- `--upx-dir` : Compression UPX (optionnel)

## 📁 Localisation du .exe

Après la compilation:

```
python_gui/
├── dist/
│   └── LLM_Checker.exe  ← Votre fichier .exe est ICI !
├── build/              (dossier temporaire, peut être supprimé)
└── llm_checker.spec
```

## 🎯 Utilisation du .exe

1. **Copier le .exe**
   - Allez dans le dossier `dist/`
   - Copiez `LLM_Checker.exe` où vous voulez

2. **Double-cliquer sur LLM_Checker.exe**
   - L'application se lance immédiatement
   - Détecte votre hardware automatiquement
   - Affiche les 5 meilleurs modèles Ollama pour votre système

3. **Fonctionnalités:**
   - Change le "Use Case" (general, coding, reasoning, chat, etc.)
   - Cliquez sur "🔄 Refresh Detection" pour relancer la détection
   - Copier les commandes `ollama pull` pour installer les modèles

## 🔍 Taille du Fichier

Le .exe devrait faire environ:
- **Sans compression UPX:** ~15-25 MB
- **Avec compression UPX:** ~8-15 MB

### Optimisation de la Taille (Optionnel)

1. **Installer UPX (compresseur)**
   - Télécharger: https://github.com/upx/upx/releases
   - Extraire dans `C:\upx\`
   - Relancer PyInstaller avec `--upx-dir=C:\upx`

2. **Exclure plus de modules**
   - Éditez `llm_checker.spec`
   - Ajoutez des modules à la liste `excludes`

## 🐛 Résolution de Problèmes

### Problème: "python n'est pas reconnu"
**Solution:** Réinstaller Python et cocher "Add to PATH"

### Problème: "ModuleNotFoundError: No module named 'psutil'"
**Solution:**
```cmd
pip install psutil
```

### Problème: Le .exe ne se lance pas
**Solutions:**
1. Vérifier dans `dist/LLM_Checker/` si compilation en mode `--onedir`
2. Regarder les erreurs dans le terminal lors de la compilation
3. Essayer sans `--windowed` pour voir les messages d'erreur:
   ```cmd
   pyinstaller --onefile llm_checker_gui.py
   ```

### Problème: Antivirus bloque le .exe
**Solution:** C'est normal pour les .exe créés avec PyInstaller
- Ajoutez une exception dans votre antivirus
- Ou signez le .exe avec un certificat code signing

### Problème: Le .exe est trop gros (>50 MB)
**Solutions:**
1. Utiliser UPX compression
2. Vérifier que les excludes fonctionnent dans le .spec
3. Utiliser Python 3.8 au lieu de 3.11+ (versions plus récentes = plus gros)

## 📊 Tests

Après création du .exe, testez sur différentes machines Windows:

1. **Windows 10/11 - CPU uniquement**
2. **Windows avec GPU NVIDIA**
3. **Windows avec GPU AMD**

## 🎨 Personnalisation

### Ajouter une Icône

1. Créer ou télécharger un fichier `icon.ico`
2. Le placer dans le dossier `python_gui/`
3. Modifier `llm_checker.spec`:
   ```python
   icon='icon.ico'
   ```
4. Recompiler avec `pyinstaller llm_checker.spec`

### Modifier les Couleurs/Style

Éditez `llm_checker_gui.py`:
```python
# Cherchez ces lignes et modifiez les couleurs
self.bg_color = "#f0f0f0"
self.header_bg = "#2c3e50"
self.accent_color = "#3498db"
```

## 📝 Notes Importantes

1. **Le .exe doit être compilé sur Windows** - PyInstaller crée des .exe spécifiques à l'OS
2. **Pas besoin de Python installé** pour exécuter le .exe final
3. **Toutes les dépendances sont incluses** dans le .exe
4. **Taille optimale:** 10-20 MB avec compression
5. **Compatible:** Windows 7, 8, 10, 11 (64-bit)

## 🚢 Distribution

Pour distribuer votre .exe:

1. **Copier uniquement `LLM_Checker.exe`** du dossier `dist/`
2. Optionnel: Créer un fichier README.txt avec instructions
3. Optionnel: Créer un installateur avec Inno Setup ou NSIS

## 📞 Support

Si vous rencontrez des problèmes:
1. Vérifiez que Python et pip sont bien installés
2. Vérifiez que toutes les dépendances sont installées
3. Testez l'application Python avant de créer le .exe
4. Regardez les logs de PyInstaller pour des erreurs

---

**Bonne compilation! 🎉**
