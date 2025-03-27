import gradio as gr
import time
from openai import OpenAI
from utils.env_utils import EnvFileHandler
from tabs.settings_tab import load_settings
from kubernetes import client, config
import yaml

# Initialize environment handler
env_handler = EnvFileHandler()

def get_k8s_context():
    """Get local Kubernetes cluster context."""
    try:
        # Load local kubeconfig
        config.load_kube_config()
        v1 = client.CoreV1Api()
        
        # Get cluster info
        cluster_info = v1.list_namespace()
        nodes = v1.list_node()
        
        context = f"""Local Kubernetes Cluster Information:
        - Namespaces: {[ns.metadata.name for ns in cluster_info.items]}
        - Nodes: {[node.metadata.name for node in nodes.items]}
        - Node Status: {[node.status.conditions[-1].type for node in nodes.items]}
        """
        return context
    except Exception as e:
        return f"Error connecting to Kubernetes: {str(e)}"

def chat_response(message, history, context):
    """Handle chat responses using OpenAI.
    
    Args:
        message (str): The user's message
        history (list): List of previous message pairs (user, assistant)
        context (str): User's Kubernetes context and environment details
        
    Returns:
        str: The assistant's response
    """
    settings = load_settings()
    api_key = env_handler.get_env(f"{settings['provider'].upper()}_API_KEY")
    
    if not api_key:
        return "Error: API key not found. Please set your API key in Settings."
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Convert history to messages format
        messages = []
        for user_msg, assistant_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})
        messages.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model=settings['model'],
            messages=[
                {"role": "system", "content": f"""You are a Kubernetes expert that helps users with their specific K8s issues. 
                The user's Kubernetes context is:
                {context}
                
                Provide detailed explanations with code and YAML examples when relevant. 
                Focus on solutions specific to the user's environment."""},
                *messages
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def create_chat_window():
    """Create the chat application window."""
    with gr.Blocks(title="AI Chat") as chat_window:
        gr.Markdown("# AI Chat Interface")
        
        # Show current settings
        current_settings = load_settings()
        gr.Markdown(f"""
        ### Current Settings
        - Provider: {current_settings['provider']}
        - Model: {current_settings['model']}
        """)
        
        # Get and display Kubernetes context
        k8s_context = get_k8s_context()
        gr.Markdown("### Kubernetes Cluster Information")
        gr.Markdown(k8s_context)
        
        # Add additional context input
        with gr.Row():
            with gr.Column(scale=1):
                context = gr.Textbox(
                    label="Additional Context",
                    placeholder="Add any additional context about your specific issues or requirements...",
                    lines=3
                )
        
        # Create chat interface
        chatbot = gr.ChatInterface(
            fn=chat_response,
            additional_inputs=[context],
            type="messages"
        )
       
    return chat_window 