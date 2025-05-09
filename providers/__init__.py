"""
Module de gestion des providers pour Amadeus.

Ce module contient les classes et fonctions pour gérer les différents
providers de modèles d'IA que ce soit en local ou sur le cloud.
"""

import os
import sys
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("providers")

# S'assurer que le package est importable
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, os.path.dirname(current_dir))

# Importation des modules nécessaires
try:
    from amadeus.providers.base import Provider
    from amadeus.providers.registry import ProviderRegistry
    from amadeus.providers.config import ProviderConfigManager
    from amadeus.providers.exceptions import (
        ProviderError, ProviderNotFoundError,
        ProviderConnectionError, ProviderAuthenticationError,
        ProviderConfigurationError
    )

    # Importation des sous-packages pour la découverte automatique
    try:
        from amadeus.providers import cloud, local
    except ImportError as e:
        logger.error(f"Erreur lors de l'import des sous-packages: {e}")
        # Créer des modules vides si l'import échoue
        import types
        if 'amadeus.providers.cloud' not in sys.modules:
            sys.modules['amadeus.providers.cloud'] = types.ModuleType('amadeus.providers.cloud')
            sys.modules['amadeus.providers.cloud'].__file__ = os.path.join(current_dir, 'cloud', '__init__.py')
        if 'amadeus.providers.local' not in sys.modules:
            sys.modules['amadeus.providers.local'] = types.ModuleType('amadeus.providers.local')
            sys.modules['amadeus.providers.local'].__file__ = os.path.join(current_dir, 'local', '__init__.py')

    # Initialiser le registre global des providers
    registry = ProviderRegistry()
    
    # Initialiser le gestionnaire de configuration global
    config_manager = ProviderConfigManager()

    # Fonction utilitaire pour obtenir tous les providers disponibles
    def get_all_providers():
        """Retourne tous les providers disponibles."""
        providers = registry.get_all_providers()
        logger.info(f"Providers disponibles: {list(providers.keys())}")
        return providers

    # Fonction utilitaire pour obtenir les providers par type
    def get_cloud_providers():
        """Retourne les providers cloud disponibles."""
        providers = registry.get_providers_by_type("cloud")
        logger.info(f"Providers cloud: {list(providers.keys())}")
        return providers

    def get_local_providers():
        """Retourne les providers locaux disponibles."""
        providers = registry.get_providers_by_type("local")
        logger.info(f"Providers locaux: {list(providers.keys())}")
        return providers

except ImportError as e:
    logger.error(f"Erreur critique lors de l'initialisation du package providers: {e}")
    # Créer des objets factices en cas d'erreur critique
    class DummyRegistry:
        def get_all_providers(self): return {}
        def get_providers_by_type(self, _): return {}
        def get_provider_config(self, _): raise Exception("Provider registry not available")
    registry = DummyRegistry()
    
    class DummyConfigManager:
        def get_all_providers(self): return []
        def get_provider_config(self, _): return {}
        def save_provider_config(self, _, __): pass
        def delete_provider_config(self, _): return False
    config_manager = DummyConfigManager()
    
    def get_all_providers(): return {}
    def get_cloud_providers(): return {}
    def get_local_providers(): return {}

__all__ = [
    'Provider', 'ProviderRegistry', 'ProviderConfigManager',
    'ProviderError', 'ProviderNotFoundError', 'ProviderConnectionError',
    'ProviderAuthenticationError', 'ProviderConfigurationError',
    'registry', 'config_manager', 'get_all_providers',
    'get_cloud_providers', 'get_local_providers'
]
