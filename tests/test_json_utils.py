import os
import json
import pytest
from utils.json_utils import AIProviderConfig

@pytest.fixture
def config_handler(tmp_path):
    """Create a temporary config file for testing."""
    config_file = tmp_path / "ai_providers.json"
    handler = AIProviderConfig(config_file)
    return handler

def test_config_file_creation(config_handler):
    """Test that config file is created with default values."""
    assert os.path.exists(config_handler.config_file)
    with open(config_handler.config_file, 'r') as f:
        config = json.load(f)
        assert "OpenAI" in config
        assert "Anthropic" in config
        assert "models" in config["OpenAI"]
        assert "api_key_env" in config["OpenAI"]

def test_get_providers(config_handler):
    """Test getting all provider configurations."""
    providers = config_handler.get_providers()
    assert isinstance(providers, dict)
    assert "OpenAI" in providers
    assert "Anthropic" in providers

def test_get_provider_models(config_handler):
    """Test getting models for a specific provider."""
    # Test OpenAI models
    openai_models = config_handler.get_provider_models("OpenAI")
    assert isinstance(openai_models, list)
    assert "gpt-3.5-turbo" in openai_models
    
    # Test non-existent provider
    assert config_handler.get_provider_models("NonExistent") == []

def test_get_api_key_env(config_handler):
    """Test getting API key environment variable name."""
    # Test OpenAI
    assert config_handler.get_api_key_env("OpenAI") == "OPENAI_API_KEY"
    
    # Test non-existent provider
    assert config_handler.get_api_key_env("NonExistent") == "NONEXISTENT_API_KEY"

def test_add_provider(config_handler):
    """Test adding a new provider configuration."""
    new_provider = {
        "provider": "TestProvider",
        "models": ["model1", "model2"],
        "api_key_env": "TEST_API_KEY"
    }
    
    assert config_handler.add_provider(
        new_provider["provider"],
        new_provider["models"],
        new_provider["api_key_env"]
    )
    
    # Verify the provider was added
    providers = config_handler.get_providers()
    assert new_provider["provider"] in providers
    assert providers[new_provider["provider"]]["models"] == new_provider["models"]
    assert providers[new_provider["provider"]]["api_key_env"] == new_provider["api_key_env"]

def test_remove_provider(config_handler):
    """Test removing a provider configuration."""
    # Add a test provider
    config_handler.add_provider("TestProvider", ["model1"], "TEST_API_KEY")
    
    # Remove the provider
    assert config_handler.remove_provider("TestProvider")
    
    # Verify the provider was removed
    providers = config_handler.get_providers()
    assert "TestProvider" not in providers
    
    # Test removing non-existent provider
    assert not config_handler.remove_provider("NonExistent")

def test_persistence(config_handler):
    """Test that configurations persist between instances."""
    # Add a test provider
    config_handler.add_provider("TestProvider", ["model1"], "TEST_API_KEY")
    
    # Create a new instance
    new_handler = AIProviderConfig(config_handler.config_file)
    
    # Verify the provider exists in the new instance
    assert "TestProvider" in new_handler.get_providers() 