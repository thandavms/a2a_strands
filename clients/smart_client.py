#!/usr/bin/env python3
"""
Smart A2A Client
A client that can automatically route questions to the appropriate A2A agent
"""

from strands import Agent
from strands_tools.a2a_client import A2AClientToolProvider
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from registry.registry_client import RegistryClient
import argparse

class SmartA2AClient:
    """Smart client that routes questions to appropriate A2A agents"""
    
    def __init__(self, agent_urls=None, registry_url=None):
        """Initialize with agent URLs or registry for service discovery"""
        self.agent_urls = agent_urls or []
        self.registry_url = registry_url
        
        # Create a smart routing agent
        self.client_agent = Agent(
            system_prompt="""You are a smart assistant that can route questions to specialized agents.
            
            You have access to multiple specialized agents via A2A tools:
            - Weather agents for weather-related questions
            - Booking agents for reservation and booking questions
            - Other specialized agents as available
            
            When a user asks a question:
            1. Analyze what type of question it is
            2. Use the appropriate A2A tool to get the answer from the right specialist
            3. Provide a clear, helpful response based on the specialist's answer
            
            Always route to the most appropriate specialist for the best answer.""",
            name="smart_client",
            description="Smart routing client that connects users to appropriate specialized agents"
        )
        
        # Connect to agents via registry or direct URLs
        if registry_url:
            registry_client = RegistryClient(registry_url)
            agent_urls = registry_client.get_agent_urls()
            if agent_urls:
                a2a_client = A2AClientToolProvider(known_agent_urls=agent_urls)
                print(f"🤖 Smart A2A Client initialized")
                print(f"📋 Using registry: {registry_url}")
                print(f"🔍 Discovered {len(agent_urls)} agents:")
                for url in agent_urls:
                    print(f"   - {url}")
            else:
                print(f"❌ No agents found in registry: {registry_url}")
                return
        else:
            a2a_client = A2AClientToolProvider(known_agent_urls=self.agent_urls)
            print(f"🤖 Smart A2A Client initialized")
            print(f"🔗 Connected to {len(self.agent_urls)} agents:")
            for url in self.agent_urls:
                print(f"   - {url}")
        
        self.client_agent.tools = a2a_client.tools
        print()
    
    def ask(self, question):
        """Ask a question and get routed to the right agent"""
        print(f"❓ Question: {question}")
        print("🔄 Routing to appropriate agent...")
        print()
        
        try:
            response = self.client_agent(question)
            return response
        except Exception as e:
            return f"❌ Error: {e}"

def interactive_mode(client):
    """Run in interactive mode"""
    print("🎯 Smart A2A Client - Interactive Mode")
    print("="*40)
    print("Ask any question and I'll route it to the right agent!")
    print("Type 'quit' or 'exit' to stop")
    print()
    
    while True:
        try:
            question = input("💬 You: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not question:
                continue
                
            print()
            response = client.ask(question)
            print(f"🤖 Assistant: {response}")
            print("\n" + "="*40 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def demo_mode(client):
    """Run demo with sample questions"""
    print("🎯 Smart A2A Client - Demo Mode")
    print("="*40)
    
    demo_questions = [
        "What's the weather like in Paris?",
        "Can you help me book a hotel in New York?",
        "Should I bring an umbrella to London?",
        "I need to make a restaurant reservation for tonight",
        "What's the temperature in Tokyo?",
        "How do I cancel a flight booking?"
    ]
    
    for question in demo_questions:
        print()
        response = client.ask(question)
        print(f"🤖 Assistant: {response}")
        print("\n" + "-"*40)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Smart A2A Client")
    parser.add_argument(
        "--agents",
        nargs="*",
        help="URLs of A2A agents to connect to directly"
    )
    parser.add_argument(
        "--registry",
        type=str,
        default="http://localhost:8000",
        help="Agent registry URL for service discovery (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--mode",
        choices=["interactive", "demo"],
        default="interactive",
        help="Run mode: interactive or demo"
    )
    
    args = parser.parse_args()
    
    try:
        # Create smart client - prefer registry over direct URLs
        if args.registry and not args.agents:
            client = SmartA2AClient(registry_url=args.registry)
        else:
            client = SmartA2AClient(agent_urls=args.agents or ["http://localhost:8080", "http://localhost:8081"])
        
        # Run in selected mode
        if args.mode == "demo":
            demo_mode(client)
        else:
            interactive_mode(client)
            
    except Exception as e:
        print(f"❌ Failed to start client: {e}")
        print("💡 Make sure the agent registry and agents are running:")
        print(f"   Registry: {args.registry}")
        if args.agents:
            for url in args.agents:
                print(f"   Agent: {url}")

if __name__ == "__main__":
    main()