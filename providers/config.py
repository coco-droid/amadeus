import os
import json
import base64
from typing import Dict, Any, Optional, List
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class ProviderConfigManager:
    """
    Gestionnaire pour stocker et récupérer les configurations de provider.
    Gère le stockage sécurisé des informations d'authentification.
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialise le gestionnaire de configuration.
        
        Args:
            config_dir: Répertoire où sont stockées les configurations
        """
        self.config_dir = config_dir or os.path.expanduser("~/.amadeus")
        self.config_file = os.path.join(self.config_dir, "provider_config.secure")
        self._ensure_config_dir()
        
        # Une clé simple basée sur l'utilisateur, à améliorer pour la production
        self.key = self._derive_key()
        self.cipher = Fernet(self.key)
        self._config_cache = None
        
    def _ensure_config_dir(self):
        """S'assure que le répertoire de configuration existe."""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, exist_ok=True)
    
    def _derive_key(self) -> bytes:
        """
        Dérive une clé de chiffrement basée sur l'identité de l'utilisateur.
        Note: Pour une version de production, utilisez une méthode plus sécurisée.
        """
        # Utiliser un sel fixe par application et le nom d'utilisateur comme secret
        salt = b"AmadeusConfigManager"
        username = os.environ.get("USER") or os.environ.get("USERNAME") or "default_user"
        password = username.encode() + b"amadeus_salt_pepper"
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def _load_encrypted_config(self) -> Dict[str, Any]:
        """Charge la configuration chiffrée depuis le fichier."""
        if self._config_cache is not None:
            return self._config_cache
        
        if not os.path.exists(self.config_file):
            return {}
        
        try:
            with open(self.config_file, 'rb') as f:
                encrypted_data = f.read()
                if not encrypted_data:
                    return {}
                decrypted_data = self.cipher.decrypt(encrypted_data)
                self._config_cache = json.loads(decrypted_data.decode('utf-8'))
                return self._config_cache
        except Exception as e:
            print(f"Erreur lors du chargement des configurations: {e}")
            return {}
    
    def _save_encrypted_config(self, config: Dict[str, Any]):
        """Enregistre la configuration chiffrée dans le fichier."""
        try:
            self._config_cache = config
            serialized = json.dumps(config).encode('utf-8')
            encrypted_data = self.cipher.encrypt(serialized)
            
            with open(self.config_file, 'wb') as f:
                f.write(encrypted_data)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des configurations: {e}")
    
    def get_provider_config(self, provider_id: str) -> Dict[str, Any]:
        """
        Récupère la configuration d'un provider spécifique.
        
        Args:
            provider_id: Identifiant du provider
            
        Returns:
            Configuration du provider ou dictionnaire vide si non trouvée
        """
        config = self._load_encrypted_config()
        return config.get(provider_id, {})
    
    def get_all_providers(self) -> List[str]:
        """
        Récupère la liste de tous les providers configurés.
        
        Returns:
            Liste des identifiants des providers configurés
        """
        config = self._load_encrypted_config()
        return list(config.keys())
    
    def save_provider_config(self, provider_id: str, credentials: Dict[str, str]):
        """
        Sauvegarde la configuration d'un provider.
        
        Args:
            provider_id: Identifiant du provider
            credentials: Informations d'authentification à sauvegarder
        """
        config = self._load_encrypted_config()
        config[provider_id] = credentials
        self._save_encrypted_config(config)
    
    def delete_provider_config(self, provider_id: str) -> bool:
        """
        Supprime la configuration d'un provider.
        
        Args:
            provider_id: Identifiant du provider à supprimer
            
        Returns:
            True si la configuration a été supprimée, False sinon
        """
        config = self._load_encrypted_config()
        if provider_id in config:
            del config[provider_id]
            self._save_encrypted_config(config)
            return True
        return False
    
    def check_provider_configured(self, provider_id: str) -> bool:
        """
        Vérifie si un provider est configuré.
        
        Args:
            provider_id: Identifiant du provider
            
        Returns:
            True si le provider est configuré, False sinon
        """
        config = self._load_encrypted_config()
        return provider_id in config and bool(config[provider_id])
