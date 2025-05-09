import os
import importlib
import importlib.util
import json
import sys
from typing import Dict, List, Optional, Any, Set
import pkgutil

from amadeus.providers.base import Provider
from amadeus.providers.exceptions import ProviderNotFoundError

class ProviderRegistry:
    """
    Registre des providers disponibles dans l'application.
    Permet de découvrir, instancier et gérer les providers.
    """
    
    def __init__(self):
        """Initialise le registre des providers."""
        self._providers: Dict[str, type] = {}
        self._provider_configs: Dict[str, Dict[str, Any]] = {}
        self._discover_providers()
    
    def _discover_providers(self):
        """
        Découvre automatiquement tous les providers disponibles.
        Explore les sous-packages local/ et cloud/ pour trouver les providers.
        """
        try:
            # Import explicite des packages pour éviter les problèmes d'importation
            from amadeus.providers import local, cloud
            
            # Découvrir les providers locaux
            self._discover_package_providers(local, "local")
            
            # Découvrir les providers cloud
            self._discover_package_providers(cloud, "cloud")
            
        except ImportError as e:
            print(f"Erreur lors de l'import des packages providers: {e}")
    
    def _discover_package_providers(self, package, provider_type: str):
        """
        Découvre les providers dans un package spécifique.
        
        Args:
            package: Package à explorer (local ou cloud)
            provider_type: Type de provider ("local" ou "cloud")
        """
        try:
            package_path = os.path.dirname(package.__file__)
            
            # Explorer chaque sous-package (chaque dossier est un provider)
            for _, name, is_pkg in pkgutil.iter_modules([package_path]):
                if is_pkg:
                    # Vérifier s'il y a un module provider.py et un fichier config.json
                    provider_module_path = os.path.join(package_path, name, "provider.py")
                    config_path = os.path.join(package_path, name, "config.json")
                    
                    if os.path.exists(provider_module_path) and os.path.exists(config_path):
                        try:
                            # Charger la configuration
                            with open(config_path, 'r', encoding='utf-8') as f:
                                config = json.load(f)
                            
                            # Créer l'identifiant unique du provider
                            provider_id = f"{provider_type}.{name}"
                            
                            # Stocker la configuration même si l'import échoue
                            self._provider_configs[provider_id] = config
                            
                            # Charger dynamiquement le module provider.py
                            try:
                                module_name = f"amadeus.providers.{provider_type}.{name}.provider"
                                provider_module = importlib.import_module(module_name)
                                
                                # Chercher une classe qui hérite de Provider
                                for attr_name in dir(provider_module):
                                    attr = getattr(provider_module, attr_name)
                                    if (isinstance(attr, type) and 
                                        issubclass(attr, Provider) and 
                                        attr != Provider):
                                        self._providers[provider_id] = attr
                                        break
                                
                                if provider_id not in self._providers:
                                    print(f"Aucune classe Provider trouvée dans {module_name}")
                                    
                            except ImportError as e:
                                print(f"Erreur d'importation du module {module_name}: {e}")
                                
                        except Exception as e:
                            print(f"Erreur lors du chargement du provider {name}: {e}")
                    else:
                        # Informer quand un dossier est détecté mais pas les fichiers nécessaires
                        missing = []
                        if not os.path.exists(provider_module_path):
                            missing.append("provider.py")
                        if not os.path.exists(config_path):
                            missing.append("config.json")
                        print(f"Provider {name} incomplet, fichiers manquants: {', '.join(missing)}")
        
        except Exception as e:
            print(f"Erreur lors de la découverte des providers dans {provider_type}: {e}")
    
    def get_provider_class(self, provider_id: str) -> type:
        """
        Récupère la classe du provider spécifié.
        
        Args:
            provider_id: Identifiant du provider
            
        Returns:
            Classe du provider
            
        Raises:
            ProviderNotFoundError: Si le provider n'est pas trouvé
        """
        if provider_id not in self._providers:
            raise ProviderNotFoundError(f"Provider '{provider_id}' non trouvé")
        
        return self._providers[provider_id]
    
    def create_provider(self, provider_id: str) -> Provider:
        """
        Crée une instance du provider spécifié.
        
        Args:
            provider_id: Identifiant du provider
            
        Returns:
            Instance du provider
            
        Raises:
            ProviderNotFoundError: Si le provider n'est pas trouvé
        """
        provider_class = self.get_provider_class(provider_id)
        return provider_class(provider_id)
    
    def get_all_providers(self) -> Dict[str, Dict[str, Any]]:
        """
        Retourne tous les providers disponibles avec leur configuration.
        
        Returns:
            Dictionnaire des providers avec leurs configurations
        """
        return self._provider_configs
    
    def get_providers_by_type(self, provider_type: str) -> Dict[str, Dict[str, Any]]:
        """
        Retourne les providers du type spécifié avec leur configuration.
        
        Args:
            provider_type: Type de provider ("local" ou "cloud")
            
        Returns:
            Dictionnaire des providers du type spécifié avec leurs configurations
        """
        return {provider_id: config for provider_id, config in self._provider_configs.items() 
                if provider_id.startswith(provider_type)}
    
    def get_provider_config(self, provider_id: str) -> Dict[str, Any]:
        """
        Récupère la configuration d'un provider spécifique.
        
        Args:
            provider_id: Identifiant du provider
            
        Returns:
            Configuration du provider
            
        Raises:
            ProviderNotFoundError: Si le provider n'est pas trouvé
        """
        if provider_id not in self._provider_configs:
            raise ProviderNotFoundError(f"Provider '{provider_id}' non trouvé")
        
        return self._provider_configs[provider_id]
    
    def get_provider_names(self) -> List[str]:
        """
        Récupère la liste des noms de tous les providers disponibles.
        
        Returns:
            Liste des noms des providers
        """
        return [config.get("name", provider_id) 
                for provider_id, config in self._provider_configs.items()]
