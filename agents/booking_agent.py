#!/usr/bin/env python3
"""
Booking Agent A2A Server
A standalone booking agent that can handle reservations and bookings
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

class BookingAgent:
    """Booking Agent with reservation capabilities"""
    
    def __init__(self):
        self.agent = Agent(
            system_prompt="""You are a professional booking and reservation specialist.
            
            You can help with various types of bookings and reservations:
            - Hotel and accommodation bookings
            - Restaurant reservations
            - Flight and travel bookings
            - Event and venue reservations
            - Car rental bookings
            - Activity and tour bookings
            
            Provide helpful information about:
            - Availability checking
            - Pricing and options
            - Booking procedures and requirements
            - Cancellation policies
            - Special requests and accommodations
            - Best practices for securing reservations
            
            Always be professional, detail-oriented, and provide actionable booking advice.""",
            name="booking_agent",
            description="Professional booking specialist handling hotel, restaurant, travel, and event reservations with expertise in availability, pricing, and booking procedures."
        )
    
    def start_server(self, port=8081, host="localhost", registry_url=None):
        """Start the booking agent as an A2A server"""
        print(f"🏨 Starting Booking Agent A2A Server...")
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
                    name="booking_agent",
                    description="Professional booking specialist for hotels, restaurants, travel, and events",
                    url=agent_url,
                    capabilities=["hotel_booking", "restaurant_reservations", "travel_booking", "event_booking"]
                )
                if result:
                    print("📋 Registered with custom registry")
                    # Setup cleanup on exit
                    atexit.register(lambda: registry_client.unregister_agent("booking_agent"))
            
            # Create A2A server with the booking agent
            server = A2AServer(agent=self.agent, port=port, host=host)
            
            print("✅ Booking Agent server is ready!")
            print("💼 Ready to handle booking requests from other agents...")
            print("🛑 Press Ctrl+C to stop the server")
            print()
            
            # Start serving (this blocks)
            server.serve()
            
        except KeyboardInterrupt:
            print("\n🛑 Shutting down Booking Agent server...")
            if registry_client:
                registry_client.unregister_agent("booking_agent")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            if registry_client:
                registry_client.unregister_agent("booking_agent")
            sys.exit(1)

def main():
    """Main entry point with CLI arguments"""
    parser = argparse.ArgumentParser(description="Booking Agent A2A Server")
    parser.add_argument(
        "--port", 
        type=int, 
        default=8081, 
        help="Port to run the server on (default: 8081)"
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
    
    # Create and start booking agent server
    booking_agent = BookingAgent()
    booking_agent.start_server(port=args.port, host=args.host, registry_url=args.registry)

if __name__ == "__main__":
    main()