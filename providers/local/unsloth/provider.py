from typing import Dict, List, Any, Optional
import os
import json

from amadeus.providers.base import Provider
from amadeus.providers.exceptions import (
    ProviderConnectionError, ProviderAuthenticationError
)

class UnslothProvider(Provider):
    """
    Provider pour Unsloth (fine-tuning local optimisé).
    """
    
    def validate_credentials(self, credentials: Dict[str, str]) -> bool:
        """
        Valide les informations d'identification pour Unsloth.
        Unsloth étant local, il faut surtout vérifier que les dépendances sont installées.
        
        Args:
            credentials: Dictionnaire contenant éventuellement un token HuggingFace
            
        Returns:
            True si la configuration est valide, False sinon
        """
        try:
            # Vérifier que unsloth est installé
            import unsloth
            
            # Si un token HuggingFace est fourni, on peut tenter une validation basique
            if credentials.get('huggingface_token'):
                import huggingface_hub
                try:
                    huggingface_hub.whoami(token=credentials['huggingface_token'])
                    return True
                except Exception:
                    return False
            
            return True
        except ImportError:
            return False
    
    def get_connection(self, credentials: Dict[str, str]) -> Any:
        """
        "Établit une connexion" avec Unsloth.
        Dans ce cas, il s'agit principalement de configurer l'environnement.
        
        Args:
            credentials: Dictionnaire contenant éventuellement un token HuggingFace
            
        Returns:
            Module unsloth
            
        Raises:
            ProviderConnectionError: Si les dépendances ne sont pas installées
            ProviderAuthenticationError: Si l'authentification HuggingFace échoue
        """
        try:
            import unsloth
            
            # Configurer le token HuggingFace si fourni
            if credentials.get('huggingface_token'):
                os.environ["HUGGING_FACE_HUB_TOKEN"] = credentials['huggingface_token']
                
                # Vérifier que le token est valide
                import huggingface_hub
                try:
                    huggingface_hub.whoami(token=credentials['huggingface_token'])
                except Exception as e:
                    raise ProviderAuthenticationError(f"Token HuggingFace invalide: {str(e)}")
            
            return unsloth
            
        except ImportError:
            raise ProviderConnectionError("Le package unsloth n'est pas installé. Installez-le avec 'pip install unsloth'.")
    
    def list_available_models(self, credentials: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Liste les modèles disponibles pour Unsloth.
        
        Args:
            credentials: Dictionnaire contenant éventuellement un token HuggingFace
            
        Returns:
            Liste des modèles supportés par unsloth
        """
        try:
            # Pour Unsloth, nous retournons une liste statique de modèles courants
            # qui sont connus pour fonctionner bien avec unsloth
            models = [
                {
                    "id": "mistralai/Mistral-7B-v0.1",
                    "name": "Mistral 7B v0.1",
                    "size": "7B",
                    "context_length": 8192
                },
                {
                    "id": "meta-llama/Llama-2-7b-hf",
                    "name": "Llama 2 7B",
                    "size": "7B",
                    "context_length": 4096
                },
                {
                    "id": "microsoft/phi-2",
                    "name": "Phi-2",
                    "size": "2.7B",
                    "context_length": 2048
                },
                {
                    "id": "NousResearch/Nous-Hermes-2-Yi-34B",
                    "name": "Nous Hermes 2 Yi 34B",
                    "size": "34B",
                    "context_length": 4096
                },
                {
                    "id": "teknium/OpenHermes-2.5-Mistral-7B",
                    "name": "OpenHermes 2.5 Mistral 7B",
                    "size": "7B",
                    "context_length": 8192
                }
            ]
            
            return models
            
        except Exception as e:
            raise ProviderConnectionError(f"Erreur lors de la récupération des modèles Unsloth: {str(e)}")
    
    def list_fine_tunable_models(self, credentials: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Liste les modèles qui peuvent être fine-tunés avec Unsloth.
        Dans le cas d'Unsloth, c'est la même liste que list_available_models.
        
        Args:
            credentials: Dictionnaire contenant éventuellement un token HuggingFace
            
        Returns:
            Liste des modèles fine-tunables
        """
        return self.list_available_models(credentials)
