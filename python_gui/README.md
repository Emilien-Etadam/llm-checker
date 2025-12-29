# 🚀 LLM Checker GUI - Standalone Windows Application

Application Windows standalone qui détecte votre hardware et recommande les meilleurs modèles Ollama LLM pour votre système.

## 🎯 Fonctionnalités

- ✅ **Détection Hardware Automatique**
  - CPU (marque, cœurs, instructions SIMD)
  - GPU NVIDIA (via nvidia-smi)
  - GPU AMD (via rocm-smi)
  - Mémoire système et VRAM

- ✅ **Recommandations Intelligentes**
  - Score multi-dimensionnel (Quality, Speed, Fit, Context)
  - Top 5 modèles adaptés à votre hardware
  - Estimation de vitesse (tokens/seconde)
  - Vérification de compatibilité mémoire

- ✅ **Interface Utilisateur Simple**
  - Tkinter GUI propre et lisible
  - 7 use cases : general, coding, reasoning, chat, creative, fast, quality
  - Bouton Refresh pour relancer la détection
  - Affichage des commandes `ollama pull` à copier

- ✅ **100% Standalone**
  - Un seul fichier .exe
  - Pas besoin de Python installé
  - Toutes les dépendances incluses
  - Taille optimisée (10-20 MB)

## 📸 Capture d'Écran

```
┌─────────────────────────────────────────────────────┐
│   🚀 LLM Checker - Ollama Model Recommender         │
├─────────────────────────────────────────────────────┤
│                                                      │
│  💻 Hardware Detected                               │
│  ╔═══════════════════════════════════════════════╗ │
│  ║ System: NVIDIA RTX 4090 (24GB VRAM) + 16 cores║ │
│  ║ Tier: VERY HIGH                                ║ │
│  ║ Backend: NVIDIA CUDA                           ║ │
│  ║ Max Model Size: 22.0 GB                        ║ │
│  ╚═══════════════════════════════════════════════╝ │
│                                                      │
│  ⭐ Top 5 Recommended Models                        │
│  ╔═══════════════════════════════════════════════╗ │
│  ║ 1. qwen2.5-coder:14b-instruct-q8_0            ║ │
│  ║    Score: 98/100 ⭐                            ║ │
│  ║    Quality: 95 | Speed: 100 | Fit: 98         ║ │
│  ║    ~125 tokens/sec                             ║ │
│  ║    ollama pull qwen2.5-coder:14b-instruct-q8_0║ │
│  ║                                                 ║ │
│  ║ 2. llama3.3:70b-instruct-q4_k_m               ║ │
│  ║    ...                                          ║ │
│  ╚═══════════════════════════════════════════════╝ │
│                                                      │
│  Use Case: [coding ▼]  [🔄 Refresh Detection]      │
│                                         ✅ Ready     │
└─────────────────────────────────────────────────────┘
```

## 🏃 Quick Start (Pour Utilisateurs)

1. **Télécharger `LLM_Checker.exe`**
2. **Double-cliquer** sur le fichier
3. **Voir les résultats** immédiatement !

C'est tout ! Aucune installation requise.

## 🛠️ Build Instructions (Pour Développeurs)

Voir [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) pour compiler le .exe depuis les sources.

**Résumé rapide:**
```bash
# Installer les dépendances
pip install -r requirements.txt

# Tester l'application
python llm_checker_gui.py

# Créer le .exe
pyinstaller llm_checker.spec

# Le .exe sera dans dist/LLM_Checker.exe
```

## 📁 Structure du Projet

```
python_gui/
├── llm_checker_gui.py       # Application principale (GUI)
├── hardware_detector.py     # Module de détection hardware
├── model_scorer.py          # Moteur de scoring des modèles
├── model_database.py        # Base de données des modèles Ollama
├── requirements.txt         # Dépendances Python
├── llm_checker.spec         # Configuration PyInstaller
├── README.md                # Ce fichier
└── BUILD_INSTRUCTIONS.md    # Instructions de build détaillées
```

## 🎮 Utilisation

### Use Cases Disponibles

- **general** : Usage général, équilibré
- **coding** : Optimisé pour la programmation
- **reasoning** : Modèles de raisonnement avancé
- **chat** : Conversation fluide et rapide
- **creative** : Écriture créative
- **fast** : Vitesse maximale
- **quality** : Qualité maximale

### Comprendre les Scores

Chaque modèle reçoit 4 scores (0-100):

- **Quality (Q)** : Qualité du modèle (famille, paramètres, quantization)
- **Speed (S)** : Vitesse estimée en tokens/seconde
- **Fit (F)** : Utilisation optimale de la mémoire disponible
- **Context (C)** : Longueur du contexte supporté

**Score Final** = Moyenne pondérée selon le use case

### Exemple de Résultats

Pour un système avec RTX 3060 (12GB VRAM):

```
Top 5 for 'coding':
1. qwen2.5-coder:7b-instruct-q8_0 - Score: 100/100
2. qwen2.5-coder:7b-instruct-q6_k - Score: 98/100
3. deepseek-coder-v2:16b-q4_k_m - Score: 95/100
4. llama3.1:8b-instruct-q8_0 - Score: 92/100
5. phi4:14b-q6_k - Score: 90/100
```

## 🔧 Modules Python

### 1. Hardware Detector (`hardware_detector.py`)

Détecte:
- CPU (marque, cœurs, fréquence, SIMD)
- GPU NVIDIA (via `nvidia-smi`)
- GPU AMD (via `rocm-smi`)
- Mémoire système
- Calcule le backend optimal et la taille max de modèle

### 2. Model Scorer (`model_scorer.py`)

Implémente:
- Système de scoring multi-dimensionnel
- Pondération par use case
- Estimation de tokens/seconde
- Filtrage par compatibilité mémoire

### 3. Model Database (`model_database.py`)

Contient:
- 80+ variantes de modèles Ollama populaires
- Qwen 2.5, Llama 3.x, DeepSeek, Phi, Gemma, Mistral, etc.
- Différentes quantizations (Q8_0, Q6_K, Q4_K_M, etc.)

## 📊 Compatibilité

### Hardware Supporté

- ✅ **CPU uniquement** (n'importe quel processeur moderne)
- ✅ **NVIDIA GPU** (GTX 1000+, RTX 2000+, Data Center)
- ✅ **AMD GPU** (RX 6000+, RX 7000+, avec ROCm)
- ✅ **Intel GPU** (détection basique)

### OS Supporté

- ✅ **Windows 7/8/10/11** (64-bit)
- ⚠️ Linux/Mac : Peut fonctionner avec Python, mais .exe est Windows-only

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Basé sur

Ce projet est une version GUI standalone du projet [llm-checker](https://github.com/Pavelevich/llm-checker) qui est un outil CLI Node.js.

**Différences:**
- ✅ GUI Windows au lieu de CLI
- ✅ Python au lieu de Node.js
- ✅ .exe standalone (pas besoin d'installation)
- ✅ Base de modèles simplifiée et embarquée
- ⚠️ Moins de modèles que la version complète (80 vs 6900+)

## 📄 License

MIT License - voir le fichier LICENSE du projet principal

## 🙏 Remerciements

- [Pavelevich](https://github.com/Pavelevich) pour le projet [llm-checker](https://github.com/Pavelevich/llm-checker) original
- [Ollama](https://ollama.ai) pour les modèles LLM
- Communauté Python pour psutil et PyInstaller

---

**Fait avec ❤️ et Python**
