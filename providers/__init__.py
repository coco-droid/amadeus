"""
Module de gestion des providers pour Amadeus.

Ce module contient les classes et fonctions pour gérer les différents
providers de modèles d'IA que ce soit en local ou sur le cloud.
"""

from amadeus.providers.base import Provider
from amadeus.providers.registry import ProviderRegistry
from amadeus.providers.config import ProviderConfigManager
from amadeus.providers.exceptions import (
    ProviderError, ProviderNotFoundError,
    ProviderConnectionError, ProviderAuthenticationError,
    ProviderConfigurationError
)

# Initialiser le registre global des providers
registry = ProviderRegistry()
# Initialiser le gestionnaire de configuration global
config_manager = ProviderConfigManager()

# Fonction utilitaire pour obtenir tous les providers disponibles
def get_all_providers():
    return registry.get_all_providers()

# Fonction utilitaire pour obtenir les providers par type
def get_cloud_providers():
    return registry.get_providers_by_type("cloud")

def get_local_providers():
    return registry.get_providers_by_type("local")

__all__ = [
    'Provider', 'ProviderRegistry', 'ProviderConfigManager',
    'ProviderError', 'ProviderNotFoundError', 'ProviderConnectionError',
    'ProviderAuthenticationError', 'ProviderConfigurationError',
    'registry', 'config_manager', 'get_all_providers',
    'get_cloud_providers', 'get_local_providers'
]
