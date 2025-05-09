from typing import Dict, List, Any, Optional
import requests
import json

from amadeus.providers.base import Provider
from amadeus.providers.exceptions import (
    ProviderConnectionError, ProviderAuthenticationError
)

class OpenAIProvider(Provider):
    """
    Provider pour l'API OpenAI.
    """
    
    def validate_credentials(self, credentials: Dict[str, str]) -> bool:
        """
        Valide les informations d'identification OpenAI.
        
        Args:
            credentials: Dictionnaire contenant la clé API OpenAI
            
        Returns:
            True si les informations d'identification sont valides, False sinon
        """
        if 'api_key' not in credentials:
            return False
        
        api_key = credentials['api_key']
        
        if not api_key:
            return False
            
        # Test de la clé API en faisant une requête simple
        try:
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            
            if 'organization_id' in credentials and credentials['organization_id']:
                headers["OpenAI-Organization"] = credentials['organization_id']
                
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers=headers
            )
            
            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                return False
            else:
                response.raise_for_status()
                return False
                
        except Exception as e:
            print(f"Erreur lors de la validation des informations d'identification OpenAI: {e}")
            return False
    
    def get_connection(self, credentials: Dict[str, str]) -> Any:
        """
        Établit une connexion avec l'API OpenAI.
        
        Args:
            credentials: Dictionnaire contenant la clé API OpenAI
            
        Returns:
            Client OpenAI
            
        Raises:
            ProviderAuthenticationError: Si l'authentification échoue
            ProviderConnectionError: Si la connexion échoue
        """
        try:
            from openai import OpenAI
            
            if 'api_key' not in credentials or not credentials['api_key']:
                raise ProviderAuthenticationError("Clé API OpenAI manquante")
                
            client_args = {"api_key": credentials['api_key']}
            
            if 'organization_id' in credentials and credentials['organization_id']:
                client_args["organization"] = credentials['organization_id']
                
            client = OpenAI(**client_args)
            
            # Test de la connexion
            client.models.list()
            
            return client
            
        except ImportError:
            raise ProviderConnectionError("Le package OpenAI n'est pas installé. Installez-le avec 'pip install openai'.")
        except Exception as e:
            if "Authentication" in str(e) or "Unauthorized" in str(e):
                raise ProviderAuthenticationError(f"Échec d'authentification OpenAI: {str(e)}")
            else:
                raise ProviderConnectionError(f"Erreur de connexion OpenAI: {str(e)}")
    
    def list_available_models(self, credentials: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Liste les modèles disponibles sur OpenAI.
        
        Args:
            credentials: Dictionnaire contenant la clé API OpenAI
            
        Returns:
            Liste des modèles disponibles avec leurs métadonnées
            
        Raises:
            ProviderConnectionError: Si la connexion échoue
        """
        try:
            client = self.get_connection(credentials)
            models = client.models.list()
            
            result = []
            for model in models.data:
                result.append({
                    "id": model.id,
                    "name": model.id,  # OpenAI n'a pas de nom distinctif
                    "created": model.created
                })
            
            return result
            
        except Exception as e:
            if isinstance(e, (ProviderAuthenticationError, ProviderConnectionError)):
                raise
            else:
                raise ProviderConnectionError(f"Erreur lors de la récupération des modèles OpenAI: {str(e)}")
    
    def list_fine_tunable_models(self, credentials: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Liste les modèles qui peuvent être fine-tunés sur OpenAI.
        
        Args:
            credentials: Dictionnaire contenant la clé API OpenAI
            
        Returns:
            Liste des modèles fine-tunables avec leurs métadonnées
        """
        try:
            # OpenAI n'a pas d'API spécifique pour lister les modèles fine-tunables,
            # nous retournons donc une liste prédéfinie
            return [
                {
                    "id": "gpt-3.5-turbo",
                    "name": "GPT-3.5 Turbo",
                    "description": "Modèle conversationnel optimisé pour le chat"
                },
                {
                    "id": "babbage-002",
                    "name": "Babbage",
                    "description": "Modèle capable pour de nombreuses tâches"
                },
                {
                    "id": "davinci-002",
                    "name": "Davinci",
                    "description": "Modèle le plus capable pour des tâches complexes"
                }
            ]
        except Exception as e:
            if isinstance(e, (ProviderAuthenticationError, ProviderConnectionError)):
                raise
            else:
                raise ProviderConnectionError(f"Erreur lors de la récupération des modèles fine-tunables OpenAI: {str(e)}")
