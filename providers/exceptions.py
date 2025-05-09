class ProviderError(Exception):
    """Classe de base pour toutes les erreurs liées aux providers."""
    pass

class ProviderNotFoundError(ProviderError):
    """Levée quand un provider n'est pas trouvé."""
    pass

class ProviderConnectionError(ProviderError):
    """Levée quand une erreur de connexion survient avec un provider."""
    pass

class ProviderAuthenticationError(ProviderError):
    """Levée quand l'authentification échoue avec un provider."""
    pass

class ProviderConfigurationError(ProviderError):
    """Levée quand la configuration d'un provider est invalide."""
    pass
