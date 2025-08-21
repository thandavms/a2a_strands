#!/usr/bin/env python3
"""
Custom Agent Registry for A2A Protocol
Simple HTTP-based registry for agent discovery and management
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import argparse
import sys
import time
from typing import Dict, List, Optional

class AgentInfo(BaseModel):
    """Agent registration information"""
    name: str
    description: str
    url: str
    capabilities: List[str] = []
    registered_at: float = None

class AgentRegistry:
    """Simple agent registry implementation"""
    
    def __init__(self):
        self.agents: Dict[str, AgentInfo] = {}
        self.app = FastAPI(title="A2A Agent Registry", version="1.0.0")
        self.setup_routes()
    
    def setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.post("/register")
        async def register_agent(agent: AgentInfo):
            """Register a new agent"""
            agent.registered_at = time.time()
            self.agents[agent.name] = agent
            print(f"✅ Registered agent: {agent.name} at {agent.url}")
            return {"status": "registered", "agent": agent.name}
        
        @self.app.delete("/unregister/{agent_name}")
        async def unregister_agent(agent_name: str):
            """Unregister an agent"""
            if agent_name in self.agents:
                del self.agents[agent_name]
                print(f"❌ Unregistered agent: {agent_name}")
                return {"status": "unregistered", "agent": agent_name}
            raise HTTPException(status_code=404, detail="Agent not found")
        
        @self.app.get("/agents")
        async def list_agents():
            """List all registered agents"""
            return {"agents": list(self.agents.values())}
        
        @self.app.get("/agents/{agent_name}")
        async def get_agent(agent_name: str):
            """Get specific agent info"""
            if agent_name in self.agents:
                return self.agents[agent_name]
            raise HTTPException(status_code=404, detail="Agent not found")
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy", 
                "agents_count": len(self.agents),
                "timestamp": time.time()
            }
        
        @self.app.get("/")
        async def root():
            """Registry info"""
            return {
                "service": "A2A Agent Registry",
                "version": "1.0.0",
                "agents_registered": len(self.agents),
                "endpoints": {
                    "register": "POST /register",
                    "unregister": "DELETE /unregister/{agent_name}",
                    "list_agents": "GET /agents",
                    "get_agent": "GET /agents/{agent_name}",
                    "health": "GET /health"
                }
            }

class AgentRegistryServer:
    """Agent Registry Server wrapper"""
    
    def __init__(self):
        self.registry = AgentRegistry()
    
    def start_registry(self, port=8000, host="localhost"):
        """Start the agent registry server"""
        print(f"📋 Starting Custom Agent Registry Server...")
        print(f"📡 Host: {host}")
        print(f"🔌 Port: {port}")
        print(f"🌐 URL: http://{host}:{port}")
        print("="*50)
        
        try:
            print("✅ Agent Registry is ready!")
            print("🔍 Agents can register and discover each other")
            print("📊 Registry endpoints:")
            print("   - POST /register - Register an agent")
            print("   - GET /agents - List all agents")
            print("   - GET /health - Health check")
            print("🛑 Press Ctrl+C to stop the registry")
            print()
            
            # Start serving (this blocks)
            uvicorn.run(self.registry.app, host=host, port=port, log_level="warning")
            
        except KeyboardInterrupt:
            print("\n🛑 Shutting down Agent Registry...")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error starting registry: {e}")
            sys.exit(1)

def main():
    """Main entry point with CLI arguments"""
    parser = argparse.ArgumentParser(description="Custom A2A Agent Registry Server")
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to run the registry on (default: 8000)"
    )
    parser.add_argument(
        "--host", 
        type=str, 
        default="localhost", 
        help="Host to bind the registry to (default: localhost)"
    )
    
    args = parser.parse_args()
    
    # Create and start registry server
    registry_server = AgentRegistryServer()
    registry_server.start_registry(port=args.port, host=args.host)

if __name__ == "__main__":
    main()