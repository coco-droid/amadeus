import typer
import os
from typing import Optional
from rich.console import Console
from rich.panel import Panel

from amadeus.core.ui.application import AmadeusApp
from amadeus.i18n import get_translator, set_language

app = typer.Typer(help="Assistant de Fine-Tuning pour Modèles d'IA Générative")
console = Console()

# Fichier pour stocker la langue préférée
CONFIG_DIR = os.path.expanduser("~/.amadeus")
LANG_FILE = os.path.join(CONFIG_DIR, "language")

def get_saved_language():
    """Récupère la langue sauvegardée si elle existe."""
    try:
        if os.path.exists(LANG_FILE):
            with open(LANG_FILE, 'r') as f:
                return f.read().strip()
        return None
    except:
        return None

def save_language_preference(lang_code):
    """Sauvegarde la langue préférée."""
    try:
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        with open(LANG_FILE, 'w') as f:
            f.write(lang_code)
    except:
        pass

@app.command()
def main(
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="Afficher les informations détaillées"
    ),
    language: Optional[str] = typer.Option(
        None, "--lang", "-l", help="Langue (en, fr)"
    ),
    reset: Optional[bool] = typer.Option(
        False, "--reset", "-r", help="Réinitialiser les préférences"
    ),
):
    """
    Lance l'interface interactive d'Amadeus.
    """
    # Réinitialiser les préférences si demandé
    if reset and os.path.exists(LANG_FILE):
        os.remove(LANG_FILE)
    
    # Déterminer la langue à utiliser
    saved_lang = None if reset else get_saved_language()
    lang_to_use = language or saved_lang
    first_run = lang_to_use is None
    
    # Définir la langue si spécifiée
    if lang_to_use:
        set_language(lang_to_use)
        save_language_preference(lang_to_use)
    
    translator = get_translator()
    
    if verbose:
        console.print("[bold green]Démarrage d'Amadeus en mode verbose...[/bold green]")
    
    try:
        # Lancer l'application interactive
        amadeus_app = AmadeusApp(first_run=first_run)
        amadeus_app.run()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Opération annulée par l'utilisateur.[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Erreur: {str(e)}[/bold red]")
        if verbose:
            console.print_exception()
    finally:
        goodbye_msg = translator.get("goodbye_message", "Merci d'avoir utilisé Amadeus!")
        console.print(Panel(goodbye_msg, title="Au revoir"))

if __name__ == "__main__":
    app()
