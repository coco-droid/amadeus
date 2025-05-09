from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import json
import os

class Provider(ABC):
    """
    Classe abstraite de base pour tous les providers.
    Chaque provider doit implémenter cette interface.
    """
    
    def __init__(self, provider_id: str, config_path: Optional[str] = None):
        """
        Initialise un provider avec son identifiant et son chemin de configuration.
        
        Args:
            provider_id: Identifiant unique du provider
            config_path: Chemin vers le fichier de configuration (config.json)
        """
        self.provider_id = provider_id
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        
    def _get_default_config_path(self) -> str:
        """Obtient le chemin par défaut du fichier de configuration."""
        module_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Déterminer le type (local/cloud) à partir de la structure du package
        if "local" in self.__module__:
            provider_type = "local"
        else:
            provider_type = "cloud"
            
        # Extraire le nom du provider à partir du nom du module
        provider_name = self.__module__.split('.')[-2]
        
        return os.path.join(module_dir, provider_type, provider_name, "config.json")
    
    def _load_config(self) -> Dict[str, Any]:
        """Charge la configuration du provider depuis le fichier config.json."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration non trouvée pour le provider {self.provider_id}")
        except json.JSONDecodeError:
            raise ValueError(f"Format de configuration invalide pour le provider {self.provider_id}")
    
    @property
    def name(self) -> str:
        """Retourne le nom du provider."""
        return self.config.get("name", self.provider_id)
    
    @property
    def description(self) -> str:
        """Retourne la description du provider."""
        return self.config.get("description", "")
    
    @property
    def provider_type(self) -> str:
        """Retourne le type de provider (cloud ou local)."""
        return self.config.get("provider_type", "unknown")
    
    @property
    def auth_requirements(self) -> List[Dict[str, Any]]:
        """Retourne la liste des exigences d'authentification."""
        return self.config.get("auth_requirements", [])
    
    @property
    def supported_features(self) -> Dict[str, Any]:
        """Retourne les fonctionnalités prises en charge par le provider."""
        return self.config.get("supported_features", {})
    
    @property
    def default_models(self) -> List[Dict[str, Any]]:
        """Retourne la liste des modèles par défaut du provider."""
        return self.config.get("default_models", [])
    
    @abstractmethod
    def validate_credentials(self, credentials: Dict[str, str]) -> bool:
        """
        Valide les informations d'identification pour ce provider.
        
        Args:
            credentials: Dictionnaire des informations d'identification
            
        Returns:
            True si les informations d'identification sont valides, False sinon
        """
        pass
    
    @abstractmethod
    def get_connection(self, credentials: Dict[str, str]) -> Any:
        """
        Établit une connexion avec le provider en utilisant les informations d'identification.
        
        Args:
            credentials: Dictionnaire des informations d'identification
            
        Returns:
            Objet de connexion spécifique au provider
        """
        pass
    
    @abstractmethod
    def list_available_models(self, credentials: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Liste les modèles disponibles pour ce provider.
        
        Args:
            credentials: Dictionnaire des informations d'identification
            
        Returns:
            Liste des modèles disponibles avec leurs métadonnées
        """
        pass
    
    @abstractmethod
    def list_fine_tunable_models(self, credentials: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Liste les modèles qui peuvent être fine-tunés sur ce provider.
        
        Args:
            credentials: Dictionnaire des informations d'identification
            
        Returns:
            Liste des modèles fine-tunables avec leurs métadonnées
        """
        pass
