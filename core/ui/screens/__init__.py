"""
Package contenant les différents écrans et menus de l'application Amadeus.
"""

from amadeus.core.ui.screens.main_menu import (
    show_main_menu,
    show_language_menu,
    show_training_menu,
    show_oracle_menu,
    show_models_menu,
    show_oracle_interface
)

from amadeus.core.ui.screens.providers_menu import (
    show_providers_menu,
    manage_provider,
    configure_provider,
    list_configured_providers,
    show_provider_details,
    delete_provider_menu,
    delete_provider
)

__all__ = [
    'show_main_menu',
    'show_language_menu',
    'show_training_menu',
    'show_oracle_menu',
    'show_models_menu',
    'show_oracle_interface',
    'show_providers_menu',
    'manage_provider',
    'configure_provider',
    'list_configured_providers',
    'show_provider_details',
    'delete_provider_menu',
    'delete_provider'
]
