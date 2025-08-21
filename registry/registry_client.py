#!/usr/bin/env python3
"""
Registry Client Helper
Helper functions for agents to register with the custom registry
"""

import requests
import time
from typing import List, Optional

class RegistryClient:
    """Client for interacting with the custom agent registry"""
    
    def __init__(self, registry_url: str = "http://localhost:8000"):
        self.registry_url = registry_url.rstrip('/')
    
    def register_agent(self, name: str, description: str, url: str, capabilities: List[str] = None):
        """Register an agent with the registry"""
        agent_data = {
            "name": name,
            "description": description,
            "url": url,
            "capabilities": capabilities or []
        }
        
        try:
            response = requests.post(f"{self.registry_url}/register", json=agent_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to register with registry: {e}")
            return None
    
    def unregister_agent(self, name: str):
        """Unregister an agent from the registry"""
        try:
            response = requests.delete(f"{self.registry_url}/unregister/{name}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to unregister from registry: {e}")
            return None
    
    def list_agents(self):
        """Get list of all registered agents"""
        try:
            response = requests.get(f"{self.registry_url}/agents")
            response.raise_for_status()
            return response.json()["agents"]
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get agents from registry: {e}")
            return []
    
    def get_agent_urls(self):
        """Get list of agent URLs for A2A client"""
        agents = self.list_agents()
        return [agent["url"] for agent in agents]
    
    def health_check(self):
        """Check if registry is healthy"""
        try:
            response = requests.get(f"{self.registry_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None