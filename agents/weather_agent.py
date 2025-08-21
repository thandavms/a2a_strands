#!/usr/bin/env python3
"""
Weather Agent A2A Server
A standalone weather agent that can be started as an A2A server
"""

from strands import Agent
from strands.multiagent.a2a import A2AServer
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from registry.registry_client import RegistryClient
import argparse
import sys
import atexit

class WeatherAgent:
    """Weather Agent with enhanced capabilities"""
    
    def __init__(self):
        self.agent = Agent(
            system_prompt="""You are a professional weather expert and meteorologist. 
            
            Provide accurate, detailed weather information for any location requested. Include:
            - Current conditions (temperature, humidity, wind, precipitation)
            - Weather description and outlook
            - Practical advice (clothing recommendations, travel considerations)
            - Any weather warnings or alerts if applicable
            
            Always be helpful and provide actionable weather insights.""",
            name="weather_agent",
            description="Professional weather expert providing current weather information, forecasts, and practical weather advice for any location worldwide."
        )
    
    def start_server(self, port=8080, host="localhost", registry_url=None):
        """Start the weather agent as an A2A server"""
        print(f"🌤️  Starting Weather Agent A2A Server...")
        print(f"📡 Host: {host}")
        print(f"🔌 Port: {port}")
        print(f"🌐 URL: http://{host}:{port}")
        if registry_url:
            print(f"📋 Registry: {registry_url}")
        print("="*50)
        
        registry_client = None
        
        try:
            # Register with custom registry if provided
            if registry_url:
                registry_client = RegistryClient(registry_url)
                agent_url = f"http://{host}:{port}"
                result = registry_client.register_agent(
                    name="weather_agent",
                    description="Professional weather expert providing current weather information and forecasts",
                    url=agent_url,
                    capabilities=["weather_info", "forecasts", "weather_advice"]
                )
                if result:
                    print("📋 Registered with custom registry")
                    # Setup cleanup on exit
                    atexit.register(lambda: registry_client.unregister_agent("weather_agent"))
            
            # Create A2A server with the weather agent
            server = A2AServer(agent=self.agent, port=port, host=host)
            
            print("✅ Weather Agent server is ready!")
            print("💬 Ready to receive weather requests from other agents...")
            print("🛑 Press Ctrl+C to stop the server")
            print()
            
            # Start serving (this blocks)
            server.serve()
            
        except KeyboardInterrupt:
            print("\n🛑 Shutting down Weather Agent server...")
            if registry_client:
                registry_client.unregister_agent("weather_agent")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            if registry_client:
                registry_client.unregister_agent("weather_agent")
            sys.exit(1)

def main():
    """Main entry point with CLI arguments"""
    parser = argparse.ArgumentParser(description="Weather Agent A2A Server")
    parser.add_argument(
        "--port", 
        type=int, 
        default=8080, 
        help="Port to run the server on (default: 8080)"
    )
    parser.add_argument(
        "--host", 
        type=str, 
        default="localhost", 
        help="Host to bind the server to (default: localhost)"
    )
    parser.add_argument(
        "--registry",
        type=str,
        default="http://localhost:8000",
        help="Agent registry URL (default: http://localhost:8000)"
    )
    
    args = parser.parse_args()
    
    # Create and start weather agent server
    weather_agent = WeatherAgent()
    weather_agent.start_server(port=args.port, host=args.host, registry_url=args.registry)

if __name__ == "__main__":
    main()