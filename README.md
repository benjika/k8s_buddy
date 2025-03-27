# K8sBuddy

K8sBuddy is an AI-powered Kubernetes assistant that helps you manage and troubleshoot your Kubernetes clusters through a user-friendly interface.

> 🤖 Your intelligent Kubernetes companion - powered by AI to help you navigate the complexities of Kubernetes management and troubleshooting.

## Features

- 🤖 AI-powered Kubernetes assistance
- 💬 Interactive chat interface
- 🔧 Kubernetes cluster monitoring
- ⚙️ Configurable AI provider settings
- 🔑 Secure API key management
- 📊 Real-time cluster information

## Prerequisites

- Python 3.8+
- Kubernetes cluster (local or remote)
- OpenAI API key (or other supported AI provider)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/benjika/K8sBuddy.git
cd K8sBuddy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to the provided URL (typically http://localhost:7860)

3. Configure your AI provider settings in the Settings tab

4. Start chatting with the AI about your Kubernetes needs!

## Project Structure

```
K8sBuddy/
├── app.py                 # Main application entry point
├── tabs/                  # Tab components
│   ├── chat_tab.py       # Chat interface
│   ├── settings_tab.py   # Settings management
├── utils/                # Utility modules
│   ├── env_utils.py      # Environment management
│   └── json_utils.py     # JSON configuration
└── requirements.txt      # Project dependencies
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 