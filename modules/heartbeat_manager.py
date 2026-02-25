from datetime import datetime
import json

class HeartbeatManager:
    def __init__(self, agent_name, version="earn-agent-mvp"):
        self.agent_name = agent_name
        self.version = version
        self.status = "ok"
        self.last_action = "Initialized"
        self.next_action = "Awaiting mission"
        self.capabilities = [
            "register",
            "listings",
            "submit",
            "claim"
        ]

    def set_status(self, status, last_action=None, next_action=None):
        """Updates the agent's current state."""
        self.status = status
        if last_action:
            self.last_action = last_action
        if next_action:
            self.next_action = next_action

    def generate_heartbeat(self):
        """
        Generates a compact JSON object following the Superteam heartbeat spec.
        """
        heartbeat = {
            "status": self.status,
            "agentName": self.agent_name,
            "time": datetime.utcnow().isoformat() + "Z",
            "version": self.version,
            "capabilities": self.capabilities,
            "lastAction": self.last_action,
            "nextAction": self.next_action
        }
        return heartbeat
