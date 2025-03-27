import gradio as gr
from tabs.settings_tab import create_settings_window
from tabs.chat_tab import create_chat_window
from tabs.log_viewer_tab import create_log_viewer_window

# Create the main application
demo = gr.Blocks(title="K8s Buddy")

with demo:
    gr.Markdown("# AI Application with Settings")
    
    # Create tabs for main window and settings
    with gr.Tabs():
        with gr.TabItem("Chat"):
            chat_window = create_chat_window()

        with gr.TabItem("Log Viewer"):
            log_window = create_log_viewer_window()

        with gr.TabItem("Settings"):
            settings_window = create_settings_window()

if __name__ == "__main__":
    demo.launch() 