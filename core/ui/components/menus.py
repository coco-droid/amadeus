from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.layout import HSplit, VSplit, Window, FormattedTextControl
from prompt_toolkit.layout.containers import FloatContainer, Float, ConditionalContainer
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.widgets import Box, Button, Frame, Label, Shadow
from prompt_toolkit.application.current import get_app
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from shutil import get_terminal_size

from amadeus.i18n import get_translator

class ModernButton(Button):
    """Un bouton moderne avec un meilleur rendu et support de navigation."""
    
    def __init__(self, text="", handler=None, width=None, key=None):
        super().__init__(text=text, handler=handler, width=width)
        self.key = key  # Pour permettre la navigation clavier
        
        # Style amélioré avec ombres et bordures
        style = "class:button"
        self.window.style = style
        
    def set_focus(self, focus):
        """Change l'état de focus du bouton."""
        self.control.focusable = focus

class MainMenu:
    def __init__(self, title="Menu Principal", options=None, width=40):
        self.title = title
        self.options = options or []
        self.selected_option = 0
        
        # Adapter la largeur au terminal de façon agressive pour éviter les erreurs
        try:
            term_width, _ = get_terminal_size()
            # Utiliser une largeur très contrainte si nécessaire
            self.width = min(width, max(20, term_width - 10))
        except:
            # Fallback avec largeur minimale
            self.width = min(width, 30)
            
        self.buttons = []
        self.kb = KeyBindings()
        
        # Raccourcis clavier pour la navigation dans le menu
        @self.kb.add('up')
        def _(event):
            self._select_previous()
            
        @self.kb.add('down')
        def _(event):
            self._select_next()
            
        @self.kb.add('enter', 'space')
        def _(event):
            self._activate_selected()
    
    def _select_previous(self):
        """Sélectionne l'option précédente dans le menu."""
        if self.buttons:
            self.selected_option = (self.selected_option - 1) % len(self.buttons)
            get_app().layout.focus(self.buttons[self.selected_option])
    
    def _select_next(self):
        """Sélectionne l'option suivante dans le menu."""
        if self.buttons:
            self.selected_option = (self.selected_option + 1) % len(self.buttons)
            get_app().layout.focus(self.buttons[self.selected_option])
    
    def _activate_selected(self):
        """Active l'option sélectionnée."""
        if self.buttons and 0 <= self.selected_option < len(self.buttons):
            button = self.buttons[self.selected_option]
            if button.handler:
                button.handler()
        
    def create_menu(self):
        """Crée un menu avec les options fournies."""
        translator = get_translator()
        menu_buttons = []
        self.buttons = []
        
        # Créer un Label avec une instruction pour la navigation, plus compact
        nav_help = Label(HTML(
            f'<info>↑↓: Nav</info> • <info>Enter: Select</info>'
        ))
        
        # Ajouter l'aide à la navigation
        menu_buttons.append(nav_help)
        
        # Ajouter les boutons du menu
        for i, (option_text, callback) in enumerate(self.options):
            # Si la clé est une chaîne de traduction, la traduire
            if option_text.startswith("_t:"):
                translation_key = option_text[3:]
                option_text = translator.get(translation_key, translation_key)
                
            button = ModernButton(
                text=f"{option_text}",
                handler=callback,
                width=self.width,
                key=str(i+1)
            )
            menu_buttons.append(button)
            self.buttons.append(button)
        
        # Conteneur des boutons avec espacement réduit
        menu_container = HSplit(menu_buttons, padding=0)
        
        # Traduire le titre si c'est une clé de traduction
        if self.title.startswith("_t:"):
            self.title = translator.get(self.title[3:], self.title[3:])
            
        # Ajouter un cadre au menu
        menu_frame = Frame(
            menu_container,
            title=self.title,
            style="class:frame"
        )
        
        # Wrap dans un Box pour le centrage et la largeur
        centered_menu = Box(
            menu_frame,
            padding=0,
            width=Dimension(preferred=self.width + 4, max=self.width + 6),
            style="class:dialog"
        )
        
        return centered_menu, self.kb

class MenuManager:
    def __init__(self):
        self.current_menu = None
        self.current_kb = None
        self.history = []
        
    def show_menu(self, title, options, width=40):
        """Affiche un menu avec les options spécifiées."""
        # Adapter la largeur au terminal de façon agressive
        try:
            term_width, _ = get_terminal_size()
            # Utiliser une largeur très contrainte si nécessaire
            menu_width = min(width, max(20, term_width - 10))
        except:
            # Fallback avec largeur minimale
            menu_width = min(width, 30)
            
        # Sauvegarder le menu actuel dans l'historique si existant
        if self.current_menu:
            self.history.append((self.current_menu, self.current_kb))
            
        menu = MainMenu(title=title, options=options, width=menu_width)
        self.current_menu, self.current_kb = menu.create_menu()
        return self.current_menu, self.current_kb
        
    def back_to_previous_menu(self):
        """Retourne au menu précédent."""
        if self.history:
            self.current_menu, self.current_kb = self.history.pop()
            return self.current_menu, self.current_kb
        return None, None
        
    def back_to_main_menu(self):
        """Retourne au menu principal."""
        self.history = []  # Effacer l'historique
        # Implémentation à compléter, pour l'instant on quitte
        get_app().exit()
