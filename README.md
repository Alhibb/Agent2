# 🤖 Alhibb Architect Command Center

A production-grade **Autonomous Agent Command Center** built for human operators managing agents on the Superteam Earn platform. Integrating high-performance AI generation via Google Gemini, this GUI streamlines the entire workflow from bounty discovery to submission.

## 🌟 Key Features
- **⚡ Superteam Protocol Native**: Fully compliant with the `skill.md` and `heartbeat.md` protocols for registration, discovery, and submission.
- **🧠 AI Architect**: Integrated with **Gemini 2.5 Flash** to automatically generate technical architectures, proposals, and READMEs for selected bounties.
- **🔍 Discovery Hub**: Real-time filtering of agent-eligible listings with deadline tracking and reward amounts.
- **📁 Integrated Workspace**: Automatic local directory management for files, including an in-app workspace previewer and downloader.
- **💓 Health Heartbeat**: Real-time status signaling and action tracking to keep your agent synced with the Superteam ecosystem.

## 🚀 Quick Start (Local)

### 1. Prerequisites
- Python 3.8+
- Git
- Google Gemini API Key

### 2. Installation
```powershell
# Clone the repository
git clone https://github.com/Alhibb/Agent2.git
cd Agent2

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup
Create a `.env` file or use the Sidebar in the app to configure:
- `GEMINI_API_KEY`
- `AGENT_GITHUB`
- `AGENT_X`
- `AGENT_TELEGRAM`

### 4. Run
```powershell
streamlit run app.py
```

## ☁️ Cloud Deployment
This app is ready for [Streamlit Community Cloud](https://share.streamlit.io/).
1. Fork/Clone the repo to your GitHub.
2. Deploy on Streamlit and add your environment variables to the **Secrets** section in TOML format:
   ```toml
   GEMINI_API_KEY = "your-key"
   # ... add other required keys
   ```

## 🛠️ Built With
- **Streamlit**: Modern UI Framework
- **Google Gemini**: AI Reasoning and Generation
- **Superteam Earn API**: Protocol-driven Earn Infrastructure
- **Python-dotenv**: Secure environment management

## 📄 License
MIT License - see [LICENSE](LICENSE) for details.

---
*Built by Alhibb for the Superteam Ecosystem*
