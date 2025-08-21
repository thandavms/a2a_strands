# A2A Multi-Agent System

A complete Agent-to-Agent (A2A) communication system with custom registry, specialized agents, and web interface.

## Project Structure

```
├── agents/                    # Specialized A2A agents
│   ├── weather_agent.py      # Weather information specialist
│   └── booking_agent.py      # Booking and reservation specialist
├── clients/                   # A2A client implementations
│   └── smart_client.py       # Smart routing client
├── registry/                  # Agent registry system
│   ├── agent_registry.py     # Custom registry server
│   └── registry_client.py    # Registry helper functions
├── ui/                       # User interfaces
│   └── streamlit_app.py      # Web-based chat interface
├── scripts/                  # Utility scripts
│   └── start_a2a_system.sh   # System startup script
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the complete system:**
   ```bash
   chmod +x scripts/start_a2a_system.sh
   ./scripts/start_a2a_system.sh
   ```

3. **Access the web interface:**
   - Open http://localhost:8501 in your browser
   - Start asking questions!

## System Components

### Registry (Port 8000)
- **Agent Registry**: Service discovery and registration
- **API Endpoints**: 
  - `GET /agents` - List registered agents
  - `POST /register` - Register new agent
  - `DELETE /unregister/{name}` - Remove agent

### Agents
- **Weather Agent** (Port 8080): Weather information and forecasts
- **Booking Agent** (Port 8081): Hotel, restaurant, travel bookings

### Clients
- **Smart Client**: Automatically routes questions to appropriate agents
- **Streamlit UI**: Web-based chat interface

## Manual Usage

### Start individual components:

```bash
# Start registry
python3 registry/agent_registry.py

# Start agents
python3 agents/weather_agent.py --registry http://localhost:8000
python3 agents/booking_agent.py --registry http://localhost:8000

# Start web UI
streamlit run ui/streamlit_app.py

# Use command-line client
python3 clients/smart_client.py --registry http://localhost:8000
```

## Example Questions

- "What's the weather like in Paris?"
- "Can you help me book a hotel in New York?"
- "Should I bring an umbrella to London?"
- "I need to make a restaurant reservation for tonight"

## Architecture

The system uses the A2A (Agent-to-Agent) protocol for communication:

1. **Agents register** with the central registry on startup
2. **Smart client discovers** available agents from registry
3. **Questions are routed** to appropriate specialists automatically
4. **Responses are unified** and presented to the user

## Dependencies

- `strands` - Core agent framework
- `strands-tools` - A2A client tools
- `streamlit` - Web interface
- `fastapi` - Registry API server
- `uvicorn` - ASGI server
- `requests` - HTTP client