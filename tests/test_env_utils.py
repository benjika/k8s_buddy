import os
import pytest
from utils.env_utils import EnvFileHandler

@pytest.fixture
def env_handler(tmp_path):
    """Create a temporary .env file for testing."""
    env_file = tmp_path / ".env"
    handler = EnvFileHandler(env_file)
    return handler

def test_env_file_creation(env_handler):
    """Test that .env file is created if it doesn't exist."""
    assert os.path.exists(env_handler.env_file)
    with open(env_handler.env_file, 'r') as f:
        content = f.read()
        assert "K8sBuddy Environment Variables" in content

def test_set_and_get_env(env_handler):
    """Test setting and getting environment variables."""
    # Test setting a variable
    assert env_handler.set_env("TEST_KEY", "test_value")
    
    # Test getting the variable
    assert env_handler.get_env("TEST_KEY") == "test_value"
    
    # Test getting non-existent variable
    assert env_handler.get_env("NON_EXISTENT") == ""

def test_delete_env(env_handler):
    """Test deleting environment variables."""
    # Set up a variable
    env_handler.set_env("DELETE_KEY", "delete_value")
    assert env_handler.get_env("DELETE_KEY") == "delete_value"
    
    # Delete the variable
    assert env_handler.delete_env("DELETE_KEY")
    assert env_handler.get_env("DELETE_KEY") == ""

def test_multiple_variables(env_handler):
    """Test handling multiple environment variables."""
    # Set multiple variables
    env_handler.set_env("KEY1", "value1")
    env_handler.set_env("KEY2", "value2")
    
    # Verify both variables
    assert env_handler.get_env("KEY1") == "value1"
    assert env_handler.get_env("KEY2") == "value2"
    
    # Delete one variable
    env_handler.delete_env("KEY1")
    assert env_handler.get_env("KEY1") == ""
    assert env_handler.get_env("KEY2") == "value2"

def test_update_existing_variable(env_handler):
    """Test updating an existing environment variable."""
    # Set initial value
    env_handler.set_env("UPDATE_KEY", "initial")
    assert env_handler.get_env("UPDATE_KEY") == "initial"
    
    # Update the value
    env_handler.set_env("UPDATE_KEY", "updated")
    assert env_handler.get_env("UPDATE_KEY") == "updated" 