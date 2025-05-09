import os
import json
from typing import Dict, Optional

# Singleton pour le traducteur actif
_current_translator = None

def get_translator() -> 'Translator':
    """Retourne l'instance du traducteur actif."""
    global _current_translator
    if _current_translator is None:
        _current_translator = Translator()
    return _current_translator

def set_language(language_code: str) -> None:
    """Change la langue active du traducteur."""
    translator = get_translator()
    translator.set_language(language_code)

class Translator:
    """Gère les traductions pour l'application Amadeus."""
    
    def __init__(self, language: str = "en"):
        self.translations: Dict[str, Dict[str, str]] = {}
        self.current_language = language
        self.load_translations()
    
    def load_translations(self) -> None:
        """Charge les fichiers de traduction."""
        # Chemin du dossier des traductions
        i18n_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Chargement des traductions EN (langue par défaut)
        en_path = os.path.join(i18n_dir, 'en.json')
        if os.path.exists(en_path):
            with open(en_path, 'r', encoding='utf-8') as f:
                self.translations['en'] = json.load(f)
        else:
            # Définir des traductions par défaut si le fichier n'existe pas encore
            self.translations['en'] = self.get_default_english()
        
        # Chargement des traductions FR
        fr_path = os.path.join(i18n_dir, 'fr.json')
        if os.path.exists(fr_path):
            with open(fr_path, 'r', encoding='utf-8') as f:
                self.translations['fr'] = json.load(f)
        else:
            # Définir des traductions par défaut si le fichier n'existe pas encore
            self.translations['fr'] = self.get_default_french()
    
    def get_default_english(self) -> Dict[str, str]:
        """Fournit les traductions anglaises par défaut."""
        return {
            "app_title": "Amadeus - Fine-Tuning Assistant for Generative AI Models",
            "main_menu_title": "Main Menu",
            "standard_fine_tuning": "🔧 Standard Fine-Tuning",
            "lora_fine_tuning": "🚀 LoRA Fine-Tuning",
            "dpo_optimization": "🎯 Direct Preference Optimization (DPO)",
            "provider_config": "⚙️ Provider Configuration",
            "data_preparation": "📊 Data Preparation",
            "language_settings": "🌐 Language Settings",
            "quit": "🚪 Quit",
            "welcome_message": "Welcome to Amadeus!",
            "goodbye_message": "Thank you for using Amadeus!",
            "language_menu_title": "Language Selection",
            "english": "🇬🇧 English",
            "french": "🇫🇷 Français",
            "back": "⬅️ Back"
        }
    
    def get_default_french(self) -> Dict[str, str]:
        """Fournit les traductions françaises par défaut."""
        return {
            "app_title": "Amadeus - Assistant de Fine-Tuning pour Modèles d'IA Générative",
            "main_menu_title": "Menu Principal",
            "standard_fine_tuning": "🔧 Fine-tuning standard",
            "lora_fine_tuning": "🚀 Fine-tuning avec LoRA",
            "dpo_optimization": "🎯 Direct Preference Optimization (DPO)",
            "provider_config": "⚙️ Configuration des fournisseurs",
            "data_preparation": "📊 Préparation des données",
            "language_settings": "🌐 Paramètres de langue",
            "quit": "🚪 Quitter",
            "welcome_message": "Bienvenue sur Amadeus !",
            "goodbye_message": "Merci d'avoir utilisé Amadeus !",
            "language_menu_title": "Sélection de la langue",
            "english": "🇬🇧 Anglais",
            "french": "🇫🇷 Français",
            "back": "⬅️ Retour"
        }
    
    def save_translations(self) -> None:
        """Sauvegarde les traductions dans des fichiers JSON."""
        i18n_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Sauvegarde des traductions EN
        en_path = os.path.join(i18n_dir, 'en.json')
        with open(en_path, 'w', encoding='utf-8') as f:
            json.dump(self.translations['en'], f, ensure_ascii=False, indent=2)
        
        # Sauvegarde des traductions FR
        fr_path = os.path.join(i18n_dir, 'fr.json')
        with open(fr_path, 'w', encoding='utf-8') as f:
            json.dump(self.translations['fr'], f, ensure_ascii=False, indent=2)
    
    def set_language(self, language_code: str) -> None:
        """Change la langue active."""
        if language_code in self.translations:
            self.current_language = language_code
            
    def get(self, key: str, default: Optional[str] = None) -> str:
        """Récupère une traduction par sa clé."""
        # Essayer d'obtenir la traduction dans la langue actuelle
        if key in self.translations.get(self.current_language, {}):
            return self.translations[self.current_language][key]
        
        # Fallback sur l'anglais
        if key in self.translations.get('en', {}):
            return self.translations['en'][key]
        
        # Retourner la clé elle-même ou la valeur par défaut
        return default or key
