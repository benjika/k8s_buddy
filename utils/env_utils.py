import os
from typing import Optional
from dotenv import load_dotenv, set_key, unset_key

class EnvFileHandler:
    """Handler for managing environment variables in .env file."""
    
    def __init__(self, env_file: str = ".env"):
        """Initialize the environment file handler.
        
        Args:
            env_file (str): Path to the .env file
        """
        self.env_file = env_file
        self._ensure_env_file()
        load_dotenv(self.env_file)
    
    def _ensure_env_file(self) -> None:
        """Ensure the .env file exists."""
        if not os.path.exists(self.env_file):
            with open(self.env_file, 'w') as f:
                f.write("# K8sBuddy Environment Variables\n")
    
    def get_env(self, key: str, default: str = "") -> str:
        """Get an environment variable value.
        
        Args:
            key (str): The environment variable key
            default (str): Default value if key not found
            
        Returns:
            str: The environment variable value
        """
        return os.getenv(key, default)
    
    def set_env(self, key: str, value: str) -> bool:
        """Set an environment variable value.
        
        Args:
            key (str): The environment variable key
            value (str): The value to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            set_key(self.env_file, key, value)
            os.environ[key] = value
            return True
        except Exception:
            return False
    
    def delete_env(self, key: str) -> bool:
        """Delete an environment variable.
        
        Args:
            key (str): The environment variable key to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            unset_key(self.env_file, key)
            if key in os.environ:
                del os.environ[key]
            return True
        except Exception:
            return False 