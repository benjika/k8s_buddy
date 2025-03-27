import os
from typing import Optional

class EnvFileHandler:
    """Handler for managing environment variables in .env file."""
    
    def __init__(self, env_file: str = ".env"):
        """Initialize the environment file handler.
        
        Args:
            env_file (str): Path to the .env file
        """
        self.env_file = env_file
        self._ensure_env_file()
    
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
        try:
            with open(self.env_file, 'r') as f:
                for line in f:
                    if line.startswith(f"{key}="):
                        return line.split('=')[1].strip()
        except Exception:
            pass
        return default
    
    def set_env(self, key: str, value: str) -> bool:
        """Set an environment variable value.
        
        Args:
            key (str): The environment variable key
            value (str): The value to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read existing variables
            env_vars = {}
            if os.path.exists(self.env_file):
                with open(self.env_file, 'r') as f:
                    for line in f:
                        if '=' in line:
                            k, v = line.split('=', 1)
                            env_vars[k.strip()] = v.strip()
            
            # Update the specified variable
            env_vars[key] = value
            
            # Write back all variables
            with open(self.env_file, 'w') as f:
                f.write("# K8sBuddy Environment Variables\n")
                for k, v in env_vars.items():
                    f.write(f"{k}={v}\n")
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
            # Read existing variables
            env_vars = {}
            if os.path.exists(self.env_file):
                with open(self.env_file, 'r') as f:
                    for line in f:
                        if '=' in line:
                            k, v = line.split('=', 1)
                            env_vars[k.strip()] = v.strip()
            
            # Remove the specified variable
            if key in env_vars:
                del env_vars[key]
            
            # Write back remaining variables
            with open(self.env_file, 'w') as f:
                f.write("# K8sBuddy Environment Variables\n")
                for k, v in env_vars.items():
                    f.write(f"{k}={v}\n")
            return True
        except Exception:
            return False 