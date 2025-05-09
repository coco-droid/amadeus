from prompt_toolkit import Application
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, FloatContainer, Float
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.widgets import Box, Frame, Shadow
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.application.current import get_app
from shutil import get_terminal_size

from amadeus.core.ui.styles import AMADEUS_STYLE, COLORS
from amadeus.core.ui.components.menus import MenuManager
from amadeus.core.ui.screens.main_menu import show_main_menu, show_language_menu
from amadeus.i18n import get_translator, set_language

class AmadeusApp:
    def __init__(self, first_run=True):
        self.menu_manager = MenuManager()
        self.kb = KeyBindings()
        self.menu_kb = None
        self.first_run = first_run
        
        @self.kb.add('q')
        def _(event):
            """Quitter l'application avec 'q'"""
            event.app.exit()
            
        @self.kb.add('escape')
        def _(event):
            """Retour au menu précédent avec 'escape'"""
            menu, kb = self.menu_manager.back_to_previous_menu()
            if menu:
                self.show_menu_container(menu, kb)
            else:
                self.show_main_menu()
    
    def create_modern_header(self):
        """Crée un en-tête moderne et plus impressionnant pour Amadeus."""
        translator = get_translator()
        
        # Vérifier la largeur du terminal
        try:
            term_width, _ = get_terminal_size()
        except:
            # En cas d'erreur, utiliser une largeur par défaut
            term_width = 80
        
        # Version très compacte pour petites fenêtres
        compact_ascii_art = [
            "<primary>╔═╗╔╦╗╔═╗╔╦╗╔═╗╦ ╦╔═╗</primary>",
            "<accent>╠═╣║║║╠═╣ ║║║╣ ║ ║╚═╗</accent>",
            "<secondary>╩ ╩╩ ╩╩ ╩═╩╝╚═╝╚═╝╚═╝</secondary>"
        ]
        
        # Logo simple pour fenêtres moyennes
        medium_ascii_art = [
            "<primary>  █████╗ ███╗   ███╗ █████╗ ██████╗ ███████╗██╗   ██╗███████╗</primary>",
            "<secondary>  ╚════╝ ╚══╝   ╚══╝ ╚════╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝╚══════╝</secondary>"
        ]
        
        # Choisir la version appropriée selon la taille de la fenêtre
        if term_width < 50:
            ascii_art = compact_ascii_art
        else:
            ascii_art = medium_ascii_art
        
        # Titre sous le logo
        title = translator.get('app_title')
        if term_width < 60 and len(title) > term_width - 10:
            title = "Amadeus AI"
        
        ascii_art.append("")
        ascii_art.append(f"<secondary>{title}</secondary>")
        
        # Créer un contrôle de texte pour le logo
        logo_control = FormattedTextControl(HTML("\n".join(ascii_art)))
        
        # Créer une fenêtre pour le logo avec hauteur adaptative
        logo_window = Window(
            height=len(ascii_art),
            content=logo_control,
            align="center"
        )
        
        # Créer un conteneur pour le logo
        logo_container = Box(
            logo_window, 
            padding=1,
            style="class:dialog"
        )
        
        return logo_container
    
    def change_language(self, lang_code):
        """Change la langue de l'application."""
        set_language(lang_code)
        self.show_main_menu()
    
    def show_main_menu(self):
        """Affiche le menu principal de l'application."""
        show_main_menu(self)
    
    def show_menu_container(self, menu, kb):
        """Affiche un conteneur de menu avec le logo."""
        # Structure complète de l'interface
        root_container = HSplit([
            self.create_modern_header(),
            menu
        ])
        
        # Conteneur principal avec centrage mais dimensions flexibles
        main_container = Box(
            root_container,
            padding=1,
            style="class:dialog"
        )
        
        # Création du layout et de l'application
        layout = Layout(main_container)
        
        # Mise à jour des raccourcis clavier
        self.menu_kb = kb
        all_bindings = merge_key_bindings([self.kb, kb]) if kb else self.kb
        
        # Création ou mise à jour de l'application
        if not hasattr(self, 'app') or self.app is None:
            self.app = Application(
                layout=layout,
                full_screen=True,
                mouse_support=True,
                style=AMADEUS_STYLE,
                key_bindings=all_bindings
            )
        else:
            self.app.layout = layout
            self.app.key_bindings = all_bindings

    def show_form_container(self, form, kb):
        """Affiche un formulaire dans un conteneur flottant."""
        # Créer un conteneur flottant pour le formulaire
        float_container = FloatContainer(
            content=HSplit([
                self.create_modern_header(),
                Window()  # Fenêtre vide pour remplir l'espace
            ]),
            floats=[
                Float(
                    content=form,
                    top=2,
                    bottom=2,
                    left=2,
                    right=2
                )
            ]
        )
        
        # Création du layout et de l'application
        layout = Layout(float_container)
        
        # Mise à jour des raccourcis clavier
        all_bindings = merge_key_bindings([self.kb, kb]) if kb else self.kb
        
        # Mise à jour de l'application
        if hasattr(self, 'app') and self.app is not None:
            self.app.layout = layout
            self.app.key_bindings = all_bindings
        else:
            self.app = Application(
                layout=layout,
                full_screen=True,
                mouse_support=True,
                style=AMADEUS_STYLE,
                key_bindings=all_bindings
            )

    def show_dialog_container(self, dialog, kb):
        """Affiche un dialogue dans un conteneur flottant."""
        # Même implémentation que show_form_container, mais avec un style différent
        float_container = FloatContainer(
            content=HSplit([
                self.create_modern_header(),
                Window()  # Fenêtre vide pour remplir l'espace
            ]),
            floats=[
                Float(
                    content=dialog,
                    top=2,
                    bottom=2,
                    left=2,
                    right=2
                )
            ]
        )
        
        # Création du layout et de l'application
        layout = Layout(float_container)
        
        # Mise à jour des raccourcis clavier
        all_bindings = merge_key_bindings([self.kb, kb]) if kb else self.kb
        
        # Mise à jour de l'application
        if hasattr(self, 'app') and self.app is not None:
            self.app.layout = layout
            self.app.key_bindings = all_bindings
        else:
            self.app = Application(
                layout=layout,
                full_screen=True,
                mouse_support=True,
                style=AMADEUS_STYLE,
                key_bindings=all_bindings
            )

    def show_training_options(self, model_type):
        """Affiche les options de configuration pour l'entraînement d'un type de modèle."""
        # Cette fonction sera déplacée vers un module dédié ultérieurement
        options = [
            (f"📝 Configuration de {model_type}", lambda: None),
            (f"🔨 Mode interactif pour {model_type}", lambda: None),
            ("↩️ Retour", lambda: self.show_main_menu())
        ]
        
        title = f"Configuration {model_type}"
        menu, kb = self.menu_manager.show_menu(title, options, width=40)
        self.show_menu_container(menu, kb)

    def manage_model(self, action):
        """Gère les opérations sur les modèles."""
        # Cette fonction sera déplacée vers un module dédié ultérieurement
        options = [
            ("Cette fonctionnalité n'est pas encore implémentée", lambda: None),
            ("↩️ Retour", lambda: self.show_main_menu())
        ]
        
        title = f"Gestion des modèles - {action}"
        menu, kb = self.menu_manager.show_menu(title, options, width=50)
        self.show_menu_container(menu, kb)
    
    def run(self):
        """Lance l'application Amadeus."""
        if self.first_run:
            # Premier lancement : sélection de la langue
            show_language_menu(self)
        else:
            # Lancements suivants : menu principal directement
            self.show_main_menu()
        
        self.app.run()
