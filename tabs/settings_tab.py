import gradio as gr
from utils.env_utils import EnvFileHandler
from typing import Dict
from utils.json_utils import AIProviderConfig

# Initialize environment handler
env_handler = EnvFileHandler()
# Initialize AI provider config
ai_provider_config = AIProviderConfig()

# Define available AI providers and their models
AI_PROVIDERS = ai_provider_config.get_providers()

def show_popup(message: str):
    gr.Info(message)
    
def load_settings() -> Dict:
    """Load settings from environment variables."""
    settings = {
        "provider": env_handler.get_env("AI_PROVIDER", "OpenAI"),
        "model": env_handler.get_env("AI_MODEL", "gpt-3.5-turbo"),
        "api_key": env_handler.get_env("API_KEY", ""),
    }
    return settings

def save_settings(provider: str, model: str, api_key: str) -> str:
    """Save settings to environment variables."""
    env_handler.set_env("AI_PROVIDER", provider)
    env_handler.set_env("AI_MODEL", model)
    env_handler.set_env(f"{provider.upper()}_API_KEY", api_key)
    return "Settings saved successfully!"

def save_api_key(provider: str, api_key: str) -> str:
    """Save API key for the selected provider."""
    env_handler.set_env(f"{provider.upper()}_API_KEY", api_key)
    return "API key saved successfully!"

def update_api_key(provider: str) -> str:
    """Update API key based on selected provider."""
    return env_handler.get_env(f"{provider.upper()}_API_KEY", "")

def set_api_key(provider: str, api_key: str) -> str:
    """Set API key based on selected provider."""
    saved = env_handler.set_env(f"{provider.upper()}_API_KEY", api_key)
    if saved:
        show_popup(f"{provider} API Key saved successfully!")
    else:
        show_popup(f"{provider} API Key not saved")

def save_selected_model(provider: str, model: str) -> str:
    """Save selected provider and model."""
    env_handler.set_env("AI_PROVIDER", provider)
    env_handler.set_env("AI_MODEL", model)
    show_popup(f"Selected {provider} model {model} saved successfully!")
    return ""

def create_settings_window():
    """Create the settings window with provider, model, and API key inputs."""
    settings = load_settings()
    
    with gr.Blocks(title="AI Settings") as settings_window:
        gr.Markdown("# AI Settings Configuration")
        gr.Markdown("")
        gr.Markdown("## AI API Key Configuration")
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Row():
                    provider_api_dropdown = gr.Dropdown(
                        choices=list(AI_PROVIDERS.keys()),
                        value=settings["provider"],
                        label="AI Provider"
                    )
                    
                    api_key_input = gr.Textbox(
                        value=env_handler.get_env(f"{settings['provider'].upper()}_API_KEY", ""),
                        label="API Key",
                        type="password"
                    )
                with gr.Row():
                    save_api_keybutton = gr.Button("Save API Key")
            with gr.Column(scale=2):
                pass
            
            # Update API key input when provider changes
            provider_api_dropdown.change(
                fn=update_api_key,
                inputs=[provider_api_dropdown],
                outputs=[api_key_input]
            )
            
            # Save settings when button is clicked
            save_api_keybutton.click(
                fn=set_api_key,
                inputs=[provider_api_dropdown, api_key_input],
                outputs=[]
            )
        
        gr.Markdown("")
        gr.Markdown("## AI Model Configuration")
        with gr.Row():
            with gr.Column(scale=1):
                with gr.Row():
                    selected_provider_dropdown = gr.Dropdown(
                        choices=list(AI_PROVIDERS.keys()),
                        value=settings["provider"],
                        label="Selected AI Provider"
                    )
                    
                    selected_model_dropdown = gr.Dropdown(
                        choices=AI_PROVIDERS[settings["provider"]],
                        value=settings["model"],
                        label="Selected AI Model"
                    )
                with gr.Row():
                    save_selected_modelbutton = gr.Button("Save Selected Model")
                    
                # Update model choices when provider changes
                selected_provider_dropdown.change(
                    fn=lambda provider: gr.Dropdown(choices=AI_PROVIDERS[provider], 
                                                    value=settings["model"] 
                                                    if settings["model"] in AI_PROVIDERS[provider] 
                                                    else AI_PROVIDERS[provider][0]),
                    inputs=[selected_provider_dropdown],
                    outputs=[selected_model_dropdown]
                )
                
                # Save selected model when button is clicked
                save_selected_modelbutton.click(
                    fn=save_selected_model,
                    inputs=[selected_provider_dropdown, selected_model_dropdown],
                    outputs=[]
                )
            with gr.Column(scale=2):
                pass
    
    return settings_window 