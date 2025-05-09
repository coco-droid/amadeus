from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, FloatContainer, Float
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.widgets import Button, Box, Frame, Label, TextArea, Dialog
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import Condition
from prompt_toolkit.validation import Validator
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.layout.margins import ScrollbarMargin

class Field:
    """Représente un champ dans un formulaire."""
    
    def __init__(self, name, label, default="", secret=False, required=False,
                 description=None, validator=None):
        self.name = name
        self.label = label
        self.default = default
        self.secret = secret
        self.required = required
        self.description = description or ""
        self.validator = validator
        self.value = default
        
    def create_control(self, width=40):
        """Crée un contrôle pour ce champ."""
        # Créer un label pour le champ
        field_label = Label(HTML(
            f"<info>{self.label}</info>{' *' if self.required else ''}: "
        ))
        
        # Créer un TextArea pour ce champ
        text_area = TextArea(
            text=self.default,
            password=self.secret,
            multiline=False,
            width=width,
            height=1,
            style="class:input-field",
            validator=self.validator,
            wrap_lines=False
        )
        
        # Stocker le TextArea pour récupérer la valeur plus tard
        self.text_area = text_area
        
        # Décrire le champ si une description est fournie
        if self.description:
            description_label = Label(HTML(f"<secondary>{self.description}</secondary>"))
            return VSplit([
                field_label,
                text_area
            ]), description_label
        
        return VSplit([field_label, text_area]), None
    
    @property
    def current_value(self):
        """Renvoie la valeur actuelle du champ."""
        if hasattr(self, 'text_area'):
            return self.text_area.text
        return self.value

class Form:
    """Un formulaire interactif pour saisir des données."""
    
    def __init__(self, title, fields=None, on_submit=None, on_cancel=None, width=60):
        self.title = title
        self.fields = fields or []
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        self.width = width
        self.kb = KeyBindings()
        
        # Navigation dans le formulaire
        @self.kb.add('tab')
        def _(event):
            event.app.layout.focus_next()
            
        @self.kb.add('s-tab')
        def _(event):
            event.app.layout.focus_previous()
            
        @self.kb.add('escape')
        def _(event):
            if self.on_cancel:
                self.on_cancel()
            event.app.exit()
    
    def add_field(self, name, label, default="", secret=False, required=False, 
                  description=None, validator=None):
        """Ajoute un champ au formulaire."""
        field = Field(name, label, default, secret, required, description, validator)
        self.fields.append(field)
        return field
    
    def create_form(self):
        """Crée un conteneur de formulaire."""
        form_items = []
        
        # Ajouter des instructions en haut du formulaire
        form_items.append(Label(HTML(
            "<info>Utilisez Tab/Shift+Tab pour naviguer, "
            "Entrée pour soumettre, Echap pour annuler</info>"
        )))
        form_items.append(Window(height=1))  # Espaceur
        
        # Ajouter les champs
        for field in self.fields:
            field_control, description_control = field.create_control(width=self.width-20)
            form_items.append(field_control)
            if description_control:
                form_items.append(description_control)
            form_items.append(Window(height=1))  # Espaceur
        
        # Ajouter les boutons de soumission
        buttons = [
            Button("Soumettre", handler=self._handle_submit),
            Button("Annuler", handler=self._handle_cancel),
        ]
        
        form_items.append(VSplit(buttons, padding=2))
        
        # Construire le conteneur final
        form_container = HSplit(form_items)
        
        # Créer un cadre autour du formulaire
        form_frame = Frame(form_container, title=self.title)
        
        # Centrer le formulaire avec une largeur fixe
        centered_form = Box(
            form_frame,
            padding=1,
            width=Dimension(preferred=self.width + 4),
            height=Dimension(min=len(self.fields) * 3 + 6),
            style="class:dialog"
        )
        
        return centered_form, self.kb
    
    def _handle_submit(self):
        """Récupère les valeurs du formulaire et appelle le callback on_submit."""
        values = {field.name: field.current_value for field in self.fields}
        if self.on_submit:
            self.on_submit(values)
    
    def _handle_cancel(self):
        """Annule le formulaire et appelle le callback on_cancel."""
        if self.on_cancel:
            self.on_cancel()

class NotificationDialog:
    """Dialogue simple pour afficher des notifications."""
    
    def __init__(self, title, text, buttons=None):
        self.title = title
        self.text = text
        self.buttons = buttons or [("OK", lambda: None)]
        self.kb = KeyBindings()
        
        @self.kb.add('escape')
        def _(event):
            self.buttons[0][1]()  # Exécuter le callback du premier bouton (généralement OK ou Fermer)
            event.app.exit()
    
    def create_dialog(self):
        """Crée un dialogue de notification."""
        # Créer les boutons
        button_widgets = []
        for label, callback in self.buttons:
            button_widgets.append(Button(label, handler=callback))
        
        # Créer le contenu du dialogue
        content = HSplit([
            Label(HTML(self.text)),
            Window(height=1),  # Espaceur
            VSplit(button_widgets, padding=2)
        ])
        
        # Construire le dialogue
        dialog_frame = Frame(content, title=self.title)
        
        # Centrer le dialogue
        centered_dialog = Box(
            dialog_frame,
            padding=1,
            width=Dimension(preferred=len(self.text) + 10, max=80),
            style="class:dialog"
        )
        
        return centered_dialog, self.kb
