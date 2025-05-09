"""
Menu principal de l'application Amadeus.
"""
from prompt_toolkit.application.current import get_app

from amadeus.i18n import get_translator
from amadeus.core.ui.screens.providers_menu import show_providers_menu

def show_main_menu(app):
    """Affiche le menu principal de l'application."""
    translator = get_translator()
    
    # Options du menu principal
    menu_options = [
        ("➤ Fine-tuning de modèles", lambda: show_training_menu(app)),
        ("🔍 Oracle (Agent IA)", lambda: show_oracle_menu(app)),
        ("⚙️ Configuration Providers", lambda: show_providers_menu(app)),
        ("📂 Gestion des Modèles", lambda: show_models_menu(app)),
        ("_t:language_settings", lambda: show_language_menu(app)),
        ("🚪 Quitter", lambda: get_app().exit())
    ]
    
    menu, kb = app.menu_manager.show_menu("_t:main_menu_title", menu_options, width=40)
    app.show_menu_container(menu, kb)

def show_training_menu(app):
    """Affiche le menu de formation des modèles."""
    submenu_options = [
        ("🔤 LLMs (texte)", lambda: app.show_training_options("llm")),
        ("🚀 vLLM (haute performance)", lambda: app.show_training_options("vllm")),
        ("🖼️ Génération d'images", lambda: app.show_training_options("image")),
        ("🔊 Synthèse vocale", lambda: app.show_training_options("tts")),
        ("🎵 Génération audio", lambda: app.show_training_options("audio")),
        ("↩️ Retour", lambda: show_main_menu(app))
    ]
    
    title = "Fine-tuning de modèles"
    menu, kb = app.menu_manager.show_menu(title, submenu_options, width=40)
    app.show_menu_container(menu, kb)

def show_oracle_menu(app):
    """Affiche le menu Oracle."""
    submenu_options = [
        ("🤖 Recommandation dataset/méthode", lambda: show_oracle_interface(app, "recommendation")),
        ("🛠️ Guide étape par étape", lambda: show_oracle_interface(app, "guide")),
        ("📊 Diagnostic erreurs", lambda: show_oracle_interface(app, "diagnostic")),
        ("↩️ Retour", lambda: show_main_menu(app))
    ]
    
    title = "Oracle (Agent IA)"
    menu, kb = app.menu_manager.show_menu(title, submenu_options, width=40)
    app.show_menu_container(menu, kb)

def show_models_menu(app):
    """Affiche le menu de gestion des modèles."""
    submenu_options = [
        ("📜 Lister tous les modèles", lambda: app.manage_model("list")),
        ("ℹ️ Détails d'un modèle", lambda: app.manage_model("details")),
        ("🧪 Tester un modèle", lambda: app.manage_model("test")),
        ("🗑️ Supprimer un modèle", lambda: app.manage_model("delete")),
        ("↩️ Retour", lambda: show_main_menu(app))
    ]
    
    title = "Gestion des Modèles"
    menu, kb = app.menu_manager.show_menu(title, submenu_options, width=40)
    app.show_menu_container(menu, kb)

def show_language_menu(app):
    """Affiche le menu de sélection de langue."""
    translator = get_translator()
    
    language_options = [
        ("_t:english", lambda: app.change_language("en")),
        ("_t:french", lambda: app.change_language("fr")),
    ]
    
    menu, kb = app.menu_manager.show_menu("_t:language_menu_title", language_options, width=30)
    app.show_menu_container(menu, kb)

def show_oracle_interface(app, oracle_mode):
    """Interface pour interagir avec Oracle."""
    options = [
        (f"🔮 Démarrer session Oracle ({oracle_mode})", lambda: None),
        ("↩️ Retour", lambda: show_oracle_menu(app))
    ]
    
    title = f"Oracle - {oracle_mode}"
    menu, kb = app.menu_manager.show_menu(title, options, width=40)
    app.show_menu_container(menu, kb)
