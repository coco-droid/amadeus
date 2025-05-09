# Amadeus-Projects

# 🎻 AMADEUS - Cheatsheet Complet

**Assistant de Fine-Tuning pour Modèles d'IA Générative**

## Structure du Projet

```
amadeus/
├── cli.py                  # Point d'entrée principal
├── __init__.py             # Expose l'API publique
├── __main__.py             # Pour exécution avec python -m amadeus
│
├── install/                # Scripts d'installation cross-platform
│   ├── install.ps1         # Installation PowerShell (Windows)
│   ├── install.sh          # Installation Bash (Mac/Linux)
│   └── requirements.txt    # Dépendances Python
│
├── core/                   # Fonctionnalités de base
│   ├── config.py           # Gestion de configuration
│   ├── ui.py               # Interface utilisateur CLI
│   ├── oracle.py           # Assistant IA intégré
│   ├── plugin_manager.py   # Système de plugins
│   └── utils.py            # Utilitaires communs
│
├── providers/              # Adaptateurs pour différents fournisseurs
│   ├── base.py             # Classe abstraite de base
│   ├── google.py           # Support Google Gemini
│   ├── openai.py           # Support OpenAI
│   ├── anthropic.py        # Support Claude
│   └── local.py            # Support modèles locaux (Unsloth, etc.)
│
├── training/               # Méthodes d'entraînement
│   ├── standard.py         # Fine-tuning standard
│   ├── lora.py             # Support LoRA/QLoRA
│   └── dpo.py              # Direct Preference Optimization
│
├── data/                   # Gestion des données
│   ├── processor.py        # Traitement des différents formats
│   ├── validator.py        # Validation de dataset
│   └── converters.py       # Conversion entre formats
│
└── tests/                  # Tests unitaires et d'intégration
    ├── test_providers.py
    ├── test_core.py
    └── fixtures/           # Données de test

```

## Installation Rapide

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/username/amadeus/main/install.ps1 | iex

```

### Mac/Linux

```bash
curl -fsSL https://raw.githubusercontent.com/username/amadeus/main/install.sh | bash

```

### Python (toutes plateformes)

```bash
# Installation de base
pip install amadeus-finetuning

# Avec support OpenAI
pip install "amadeus-finetuning[openai]"

# Avec support pour tous les fournisseurs
pip install "amadeus-finetuning[all]"

```

## Utilisation de Base

### Démarrer Amadeus

```bash
# Lancer l'interface interactive
amadeus

# Directement avec un provider spécifique
amadeus --provider openai

# Mode verbose pour le débogage
amadeus --verbose

```

## Fournisseurs de LLM Supportés

| Provider | Command | Features | Installation |
| --- | --- | --- | --- |
| Google Gemini | `--provider google` | Standard fine-tuning | `pip install "amadeus-finetuning[google]"` |
| OpenAI | `--provider openai` | Fine-tuning, RLHF | `pip install "amadeus-finetuning[openai]"` |
| Anthropic | `--provider anthropic` | Constitutional AI | `pip install "amadeus-finetuning[anthropic]"` |
| Local Models | `--provider local` | LoRA, QLoRA | `pip install "amadeus-finetuning[local]"` |

## Préparation des Données

### Formats Supportés

- CSV (colonnes: `input`, `output`)
- JSONL (clés: `text_input`, `output`)
- YAML
- Datasets Hugging Face

### Exemples de Structure

```
input,output
"Comment fonctionne X?","X fonctionne de la manière Y..."
"Qu'est-ce que Z?","Z est un concept qui..."

```

```
{"text_input": "Comment fonctionne X?", "output": "X fonctionne de la manière Y..."}
{"text_input": "Qu'est-ce que Z?", "output": "Z est un concept qui..."}

```

### Validation des Données

```bash
# Valider un dataset avant entraînement
amadeus validate path/to/dataset.csv

# Analyser la qualité avec Oracle
amadeus oracle analyze path/to/dataset.csv

```

## Méthodes de Fine-Tuning

| Méthode | Providers | Caractéristiques | Commande |
| --- | --- | --- | --- |
| Standard | Tous | Fine-tuning classique | `--method standard` |
| LoRA | Local | Adapters à faible rang | `--method lora` |
| QLoRA | Local | Version quantisée de LoRA | `--method qlora` |
| DPO | OpenAI, Local | Direct Preference Optimization | `--method dpo` |
| RLHF | OpenAI | Apprentissage par renforcement | `--method rlhf` |

## Commandes et Fonctionnalités

### Menu principal

- `1` → Créer un nouveau modèle
- `2` → Lister/Gérer les modèles existants
- `3` → 🔮 Oracle - Assistant IA
- `4` → Quitter

### Création de modèle

```bash
# Mode interactif
amadeus create

# Mode direct
amadeus create --provider google \
               --model-id mon-modele-v1 \
               --data path/to/dataset.csv \
               --epochs 200 \
               --batch-size 4 \
               --learning-rate 0.0005

```

### Paramètres d'Entraînement

| Paramètre | Description | Valeur typique | Flag CLI |
| --- | --- | --- | --- |
| Model ID | Identifiant unique | `assistant-fr-v1` | `--model-id` |
| Epochs | Nb d'itérations | 100-300 | `--epochs` |
| Batch Size | Taille des lots | 4-8 | `--batch-size` |
| Learning Rate | Vitesse d'apprentissage | 0.0001-0.001 | `--learning-rate` |
| Temperature | Créativité | 0.7-1.0 | `--temperature` |
| Top P | Diversité de tokens | 0.9-0.95 | `--top-p` |
| Top K | Nb de tokens considérés | 40-64 | `--top-k` |

### Gestion des modèles

```bash
# Lister tous les modèles
amadeus list

# Informations détaillées sur un modèle
amadeus info mon-modele-v1

# Tester un modèle
amadeus test mon-modele-v1

# Supprimer un modèle
amadeus delete mon-modele-v1

```

### Oracle - Assistant IA

```bash
# Lancer Oracle
amadeus oracle

# Demander des recommandations
amadeus oracle recommend --data path/to/dataset.csv

# Guide pour débutants
amadeus oracle guide --topic "lora-vs-qlora"

```

## Configuration

### Fichier de configuration

Emplacement: `~/.config/amadeus/config.yaml` (Linux/Mac) ou `%APPDATA%\amadeus\config.yaml` (Windows)
