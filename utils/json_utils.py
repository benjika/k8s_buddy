import json
from typing import Dict, List

class AIProviderConfig:
    """Handler for managing AI provider configurations."""
    
    def __init__(self, config_file: str = "config/ai_providers.json"):
        """Initialize the AI provider configuration handler.
        
        Args:
            config_file (str): Path to the configuration file
        """
        self.config_file = config_file
        self._ensure_config_file()
    
    def _ensure_config_file(self) -> None:
        """Ensure the configuration file exists with default values."""
        default_config = {
            "OpenAI": {
                "models": [
                    "gpt-3.5-turbo",
                    "gpt-4",
                    "gpt-4-turbo-preview"
                ],
                "api_key_env": "OPENAI_API_KEY"
            },
            "Anthropic": {
                "models": [
                    "claude-3-opus-20240229",
                    "claude-3-sonnet-20240229",
                    "claude-2.1"
                ],
                "api_key_env": "ANTHROPIC_API_KEY"
            }
        }
        
        try:
            with open(self.config_file, 'r') as f:
                json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
    
    def get_providers(self) -> Dict[str, Dict]:
        """Get all AI provider configurations.
        
        Returns:
            Dict[str, Dict]: Dictionary of provider configurations
        """
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def get_provider_models(self, provider: str) -> List[str]:
        """Get available models for a specific provider.
        
        Args:
            provider (str): The AI provider name
            
        Returns:
            List[str]: List of available model names
        """
        providers = self.get_providers()
        return providers.get(provider, {}).get("models", [])
    
    def get_api_key_env(self, provider: str) -> str:
        """Get the environment variable name for a provider's API key.
        
        Args:
            provider (str): The AI provider name
            
        Returns:
            str: The environment variable name
        """
        providers = self.get_providers()
        return providers.get(provider, {}).get("api_key_env", f"{provider.upper()}_API_KEY")
    
    def add_provider(self, provider: str, models: List[str], api_key_env: str) -> bool:
        """Add a new AI provider configuration.
        
        Args:
            provider (str): The AI provider name
            models (List[str]): List of available model names
            api_key_env (str): Environment variable name for API key
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            providers = self.get_providers()
            providers[provider] = {
                "models": models,
                "api_key_env": api_key_env
            }
            with open(self.config_file, 'w') as f:
                json.dump(providers, f, indent=4)
            return True
        except Exception:
            return False
    
    def remove_provider(self, provider: str) -> bool:
        """Remove an AI provider configuration.
        
        Args:
            provider (str): The AI provider name to remove
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            providers = self.get_providers()
            if provider in providers:
                del providers[provider]
                with open(self.config_file, 'w') as f:
                    json.dump(providers, f, indent=4)
                return True
            return False
        except Exception:
            return False 