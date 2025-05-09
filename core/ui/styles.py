from prompt_toolkit.styles import Style

# Styles pour l'application - Version moderne
AMADEUS_STYLE = Style.from_dict({
    # Interface générale
    '': '#f8f8f2 bg:#191622',  # Couleur de fond plus sombre et moderne
    'frame.border': '#ff79c6',  # Rose vif pour les bordures
    'frame.label': 'bold #bd93f9',  # Violet vif pour les titres
    
    # Boutons et menus
    'button.focused': 'bg:#44475a #8be9fd',  # Bleu clair sur fond gris pour focus
    'button': '#f8f8f2 bg:#282a36',  # Texte clair sur fond sombre pour les boutons
    'button.arrow': '#50fa7b',  # Vert vif pour les flèches
    
    # Autres éléments
    'dialog': 'bg:#191622',
    'dialog.body': 'bg:#191622 #f8f8f2',
    'dialog.border': '#ff79c6',
    
    # Texte de statut
    'status': 'bg:#191622 #8be9fd',
    'status.key': 'bg:#191622 #ff79c6 bold',
    'status.position': 'bg:#191622 #50fa7b',
    'status.prefix': 'bg:#191622 #bd93f9',
    
    # Headers et sections importantes
    'header': 'bold #ff79c6',
    'secondary': 'bold #bd93f9',
    'success': 'bold #50fa7b',
    'error': 'bold #ff5555',
    'warning': 'bold #f1fa8c',
    'info': 'bold #8be9fd',
    
    # Séparateurs et décorations
    'separator': '#bd93f9',
    'footer': 'bg:#191622 #6272a4',
})

# Palette de couleurs accessible par nom - Version moderne
COLORS = {
    'background': '#191622',       # Fond sombre
    'background_alt': '#282a36',   # Fond alternatif
    'foreground': '#f8f8f2',       # Texte principal
    'primary': '#bd93f9',          # Violet principal
    'secondary': '#ff79c6',        # Rose
    'accent': '#8be9fd',           # Bleu clair
    'success': '#50fa7b',          # Vert
    'warning': '#f1fa8c',          # Jaune
    'error': '#ff5555',            # Rouge
    'info': '#8be9fd',             # Bleu info
    'disabled': '#6272a4',         # Gris désactivé
}
