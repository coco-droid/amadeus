from typing import Dict, List, Any, Optional
import requests
import json

from amadeus.providers.base import Provider
from amadeus.providers.exceptions import (
    ProviderConnectionError, ProviderAuthenticationError
)

class AIStudioProvider(Provider):
    """
    Provider pour l'API Google AI Studio (Gemini).
    """
    
    def validate_credentials(self, credentials: Dict[str, str]) -> bool:
        """
        Valide les informations d'identification Google AI Studio.
        
        Args:
            credentials: Dictionnaire contenant la clé API
            
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
            response = requests.get(
                f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
            )
            
            if response.status_code == 200:
                return True
            elif response.status_code in (401, 403):
                return False
            else:
                response.raise_for_status()
                return False
                
        except Exception as e:
            print(f"Erreur lors de la validation des informations d'identification Google AI Studio: {e}")
            return False
    
    def get_connection(self, credentials: Dict[str, str]) -> Any:
        """
        Établit une connexion avec l'API Google AI Studio.
        
        Args:
            credentials: Dictionnaire contenant la clé API
            
        Returns:
            Client Google Generative AI
            
        Raises:
            ProviderAuthenticationError: Si l'authentification échoue
            ProviderConnectionError: Si la connexion échoue
        """
        try:
            import google.generativeai as genai
            
            if 'api_key' not in credentials or not credentials['api_key']:
                raise ProviderAuthenticationError("Clé API Google AI Studio manquante")
                
            genai.configure(api_key=credentials['api_key'])
            
            # Test de la connexion
            genai.list_models()
            
            return genai
            
        except ImportError:
            raise ProviderConnectionError("Le package google-generativeai n'est pas installé. Installez-le avec 'pip install google-generativeai'.")
        except Exception as e:
            if "Authentication" in str(e) or "Unauthorized" in str(e) or "permission" in str(e).lower():
                raise ProviderAuthenticationError(f"Échec d'authentification Google AI Studio: {str(e)}")
            else:
                raise ProviderConnectionError(f"Erreur de connexion Google AI Studio: {str(e)}")
    
    def list_available_models(self, credentials: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Liste les modèles disponibles sur Google AI Studio.
        
        Args:
            credentials: Dictionnaire contenant la clé API
            
        Returns:
            Liste des modèles disponibles avec leurs métadonnées
            
        Raises:
            ProviderConnectionError: Si la connexion échoue
        """
        try:
            genai = self.get_connection(credentials)
            models = genai.list_models()
            
            result = []
            for model in models:
                result.append({
                    "id": model.name.split('/')[-1],
                    "name": model.display_name or model.name.split('/')[-1],
                    "description": model.description
                })
            
            return result
            
        except Exception as e:
            if isinstance(e, (ProviderAuthenticationError, ProviderConnectionError)):
                raise
            else:
                raise ProviderConnectionError(f"Erreur lors de la récupération des modèles Google AI Studio: {str(e)}")
    
    def list_fine_tunable_models(self, credentials: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Liste les modèles qui peuvent être fine-tunés sur Google AI Studio.
        
        Args:
            credentials: Dictionnaire contenant la clé API
            
        Returns:
            Liste des modèles fine-tunables avec leurs métadonnées
        """
        try:
            # Google AI Studio n'expose pas encore d'API pour lister les modèles fine-tunables,
            # nous retournons donc une liste prédéfinie
            return [
                {
                    "id": "text-bison@002",
                    "name": "Text Bison",
                    "description": "Modèle de génération de texte à usage général"
                }
            ]
        except Exception as e:
            if isinstance(e, (ProviderAuthenticationError, ProviderConnectionError)):
                raise
            else:
                raise ProviderConnectionError(f"Erreur lors de la récupération des modèles fine-tunables Google AI Studio: {str(e)}")
