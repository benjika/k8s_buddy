import gradio as gr
from kubernetes import client, config, watch
import threading
import queue
import time
from typing import Optional, Dict, List

class LogViewer:
    def __init__(self):
        """Initialize the log viewer with Kubernetes client."""
        config.load_kube_config()
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.log_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.current_watch = None

    def get_namespaces(self) -> List[str]:
        """Get list of available namespaces."""
        try:
            namespaces = self.core_v1.list_namespace()
            return [ns.metadata.name for ns in namespaces.items]
        except Exception as e:
            return [f"Error: {str(e)}"]

    def get_pods(self, namespace: str) -> List[str]:
        """Get list of pods in a namespace."""
        try:
            pods = self.core_v1.list_namespaced_pod(namespace)
            return [pod.metadata.name for pod in pods.items]
        except Exception as e:
            return [f"Error: {str(e)}"]

    def get_containers(self, namespace: str, pod: str) -> List[str]:
        """Get list of containers in a pod."""
        try:
            pod_info = self.core_v1.read_namespaced_pod(pod, namespace)
            return [container.name for container in pod_info.spec.containers]
        except Exception as e:
            return [f"Error: {str(e)}"]

    def watch_logs(self, namespace: str, pod: str, container: str) -> None:
        """Watch logs from a specific pod and container."""
        try:
            self.stop_event.clear()
            self.current_watch = watch.Watch()
            
            for log in self.current_watch.stream(
                self.core_v1.read_namespaced_pod_log,
                name=pod,
                namespace=namespace,
                container=container,
                follow=True,
                tail_lines=100
            ):
                if self.stop_event.is_set():
                    break
                self.log_queue.put(log)
        except Exception as e:
            self.log_queue.put(f"Error watching logs: {str(e)}")

    def stop_watching(self) -> None:
        """Stop the current log watch."""
        self.stop_event.set()
        if self.current_watch:
            self.current_watch.stop()

def create_log_viewer_window():
    """Create the log viewer window."""
    log_viewer = LogViewer()
    
    with gr.Blocks(title="Kubernetes Log Viewer") as log_window:
        gr.Markdown("# Kubernetes Log Viewer")
        
        with gr.Row():
            with gr.Column(scale=1):
                namespace_dropdown = gr.Dropdown(
                    choices=log_viewer.get_namespaces(),
                    label="Namespace",
                    interactive=True
                )
            with gr.Column(scale=1):
                pod_dropdown = gr.Dropdown(
                    choices=[],
                    label="Pod",
                    interactive=True
                )
            with gr.Column(scale=1):
                container_dropdown = gr.Dropdown(
                    choices=[],
                    label="Container",
                    interactive=True
                )
        
        with gr.Row():
            with gr.Column(scale=1):
                start_button = gr.Button("Start Watching")
            with gr.Column(scale=1):
                stop_button = gr.Button("Stop Watching")
            with gr.Column(scale=1):
                clear_button = gr.Button("Clear Logs")
        
        log_output = gr.Textbox(
            label="Logs",
            lines=20,
            interactive=False,
            show_copy_button=True
        )
        
        def update_pods(namespace):
            return gr.Dropdown(choices=log_viewer.get_pods(namespace))
        
        def update_containers(namespace, pod):
            return gr.Dropdown(choices=log_viewer.get_containers(namespace, pod))
        
        def start_watching(namespace, pod, container):
            if not all([namespace, pod, container]):
                return "Please select namespace, pod, and container"
            
            # Start watching in a separate thread
            watch_thread = threading.Thread(
                target=log_viewer.watch_logs,
                args=(namespace, pod, container)
            )
            watch_thread.daemon = True
            watch_thread.start()
            
            # Start log processing
            def process_logs():
                while not log_viewer.stop_event.is_set():
                    try:
                        log = log_viewer.log_queue.get(timeout=1)
                        yield log
                    except queue.Empty:
                        continue
            
            return process_logs()
        
        def stop_watching():
            log_viewer.stop_watching()
            return ""
        
        def clear_logs():
            log_viewer.stop_watching()
            return ""
        
        # Set up event handlers
        namespace_dropdown.change(
            fn=update_pods,
            inputs=[namespace_dropdown],
            outputs=[pod_dropdown]
        )
        
        pod_dropdown.change(
            fn=update_containers,
            inputs=[namespace_dropdown, pod_dropdown],
            outputs=[container_dropdown]
        )
        
        start_button.click(
            fn=start_watching,
            inputs=[namespace_dropdown, pod_dropdown, container_dropdown],
            outputs=[log_output]
        )
        
        stop_button.click(
            fn=stop_watching,
            inputs=[],
            outputs=[log_output]
        )
        
        clear_button.click(
            fn=clear_logs,
            inputs=[],
            outputs=[log_output]
        )
    
    return log_window 