import os
import requests
from dotenv import load_dotenv, set_key

def load_env():
    """Loads environment variables from .env file."""
    load_dotenv()

def get_env_var(key, default=None):
    """Retrieves an environment variable, checking Streamlit secrets as fallback."""
    val = os.getenv(key)
    if val:
        return val
    
    # Fallback for Streamlit Cloud
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except:
        pass
        
    return default

def update_env(key, value, env_path=".env"):
    """
    Safely updates or appends a key-value pair to the .env file.
    Uses set_key from python-dotenv to preserve existing content.
    """
    if not os.path.exists(env_path):
        with open(env_path, 'w') as f:
            pass
    set_key(env_path, key, value)
    load_dotenv(override=True)

def register_agent(agent_name):
    """
    Registers a new agent with the Superteam API.
    Returns: dict with apiKey, claimCode, agentId, username or None on failure.
    """
    url = "https://superteam.fun/api/agents"
    payload = {"name": agent_name}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Values predicted based on prompt description
        auth_data = {
            "SUPERTEAM_AGENT_KEY": data.get("apiKey"),
            "AGENT_CLAIM_CODE": data.get("claimCode"),
            "AGENT_ID": data.get("agentId"),
            "AGENT_NAME": data.get("username") or agent_name
        }
        
        # Update .env with new values
        for key, val in auth_data.items():
            if val:
                update_env(key, val)
        
        return auth_data
    except Exception as e:
        print(f"Registration failed: {e}")
        return None
