#!/usr/bin/env python3
"""
Simple Streamlit App for Smart A2A Client
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from clients.smart_client import SmartA2AClient

# Page config
st.set_page_config(
    page_title="Smart A2A Assistant",
    page_icon="🤖",
    layout="centered"
)

# Initialize session state
if "client" not in st.session_state:
    st.session_state.client = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.title("🤖 Smart A2A Assistant")
st.markdown("Ask questions and get routed to the right specialist agent!")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    agent_urls = st.text_area(
        "Agent URLs (one per line)", 
        value="http://localhost:8080\nhttp://localhost:8081",
        help="URLs of A2A agents"
    )
    
    if st.button("Connect to Agents"):
        try:
            urls = [url.strip() for url in agent_urls.split('\n') if url.strip()]
            with st.spinner("Connecting to agents..."):
                st.session_state.client = SmartA2AClient(agent_urls=urls)
            st.success(f"✅ Connected to {len(urls)} agents!")
        except Exception as e:
            st.error(f"❌ Connection failed: {e}")
    
    # Auto-connect on first load
    if st.session_state.client is None:
        try:
            urls = ["http://localhost:8080", "http://localhost:8081"]
            st.session_state.client = SmartA2AClient(agent_urls=urls)
            st.success("🟢 Auto-connected to agents")
        except:
            st.warning("🟡 Not Connected")
    
    # Status
    if st.session_state.client:
        st.success("🟢 Client Ready")
    else:
        st.warning("🟡 Not Connected")

# Main chat interface
if st.session_state.client:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response from smart client
        with st.chat_message("assistant"):
            with st.spinner("Routing to appropriate agent..."):
                try:
                    response = st.session_state.client.ask(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"❌ Error: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

else:
    st.info("👈 Please connect to agents first using the sidebar")
    
    # Sample questions
    st.subheader("Sample Questions")
    st.markdown("""
    - What's the weather like in Paris?
    - Can you help me book a hotel in New York?
    - Should I bring an umbrella to London?
    - I need to make a restaurant reservation
    """)

# Footer
st.markdown("---")
st.markdown("*Powered by Smart A2A Client*")